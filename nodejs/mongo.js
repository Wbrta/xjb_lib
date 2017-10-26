var key = [];
var value_type = [];
var fs = require('fs');
var db_url = "mongodb://localhost:27017/test";
var mongo_client = require('mongodb').MongoClient;

var argc = 0;
var argv = [];
var key_num = 2;
var data_num = 5;
var type = "query";
var isIndex = false;
var file_path = null;

process.argv.forEach(function (val, index, array) {
  argv[argc] = val;
  argc += 1;
});

for (var i = 2; i < argc; ++i) {
  if (argv[i] == "query") type = "query";
  else if (argv[i] == "help") type = "help";
  else if (argv[i] == "insert") type = "insert";
  else if (argv[i] == "update") type = "update";
  else if (argv[i] == "delete") type = "delete";
  else if (argv[i] == "with_index") isIndex = true;
  else if (argv[i].substring(0, 11) == "key_number=") key_num = paserInt(argv[i].substring(11));
  else if (argv[i].substring(0, 12) == "data_number=") data_num = paserInt(argv[i].substring(12));
  else if (argv[i].substring(0, 5) == "from=") file_path = argv[i].substring(5);
}

var byte_range = function(first, last) {
  var cur = 0;
  var list = [];
  for (var i = first; i <= last; ++i) 
    list[cur++] = i;
  return list;
}

var tmp = byte_range(0xC2, 0xF4);
var first_values = byte_range(0x00, 0x7F);
first_values.push.apply(first_values, tmp);
var trailing_values = byte_range(0x80, 0xBF);

var get_rand_int = function(min, base) {
  return min + Math.ceil(Math.random() * base);
}
var get_rand_float = function(base) {
  return Math.random() * base;
}
var random_choice = function(array) {
  var index = Math.floor((Math.random() * array.length));
  return array[index];
}
var random_utf8_seq = function() {
  var first = random_choice(first_values);
  if (first <= 0x7F) {
    return [first];
  } else if (first <= 0xDF) {
    return [first, random_choice(trailing_values)];
  } else if (first == 0xE0) {
    return [first, random_choice(byte_range(0xA0, 0xBF)), random_choice(trailing_values)];
  } else if (first == 0xED) {
    return [first, random_choice(byte_range(0x80, 0x9F)), random_choice(trailing_values)];
  } else if (first <= 0xEF) {
    return [first, random_choice(trailing_values), random_choice(trailing_values)];
  } else if (first == 0xF0) {
    return [first, random_choice(byte_range(0x90, 0xBF)), random_choice(trailing_values), random_choice(trailing_values)];
  } else if (first <= 0xF3) {
    return [first, random_choice(trailing_values), random_choice(trailing_values), random_choice(trailing_values)];
  } else if (first == 0xF4) {
    return [first, random_choice(byte_range(0x80, 0x8F)), random_choice(trailing_values), random_choice(trailing_values)];
  }
}
var get_rand_string = function(len) {
  var string = "";
  for (var i = 0; i < len; ++i) {
    var str = '';
    var a = random_utf8_seq();
    for (var j = 0; j < a.length; ++j) {
      str += '%' + ('0' + a[j].toString(16)).slice(-2);
    }
    try {
      str = decodeURIComponent(str);
      if (str == null) str = "null";
      else if (str == undefined) str = "undefined";
      else if (str == "") str = "empty";
      else if (str == ".") str = "point";
      else if (str == " ") str = "blank";
      else if (str == "$") str = "doller";
      else if (str == "/") str = "left";
      else if (str == "\\") str = "right";
      else if (str == '\0') str = "0";
    } catch(err) {
      str = "error";
    }
    string += str;
  }
  return string;
}
var get_rand_object = function() {
  var ret = {};
  var len = get_rand_int(5, 10);
  for (var i = 0; i < len; ++i) 
    ret[get_rand_string(get_rand_int(8, 120))] = get_rand_string(get_rand_int(16, 240));
  return ret;
}
var get_date = function() {
  var time = new Date().toLocaleString();
  return time;
}
var get_rand_data = function(knum, dnum) {
  for (var i = 0; i < knum; ++i) {
    key[i] = get_rand_string(get_rand_int(2, 30));
    value_type[i] = get_rand_int((i == 0 ? 1 : 0), 5);
  }
  var datas = [];
  for (var cur = 0; cur < dnum; ++cur) {
    var data = {};
    for (var i = 0; i < knum; ++i) {
      var rand = value_type[i];
      if (rand == 0) data[key[i]] = get_rand_object();
      else if (rand == 1) data[key[i]] = get_rand_int(0, 1e9 + 7);
      else if (rand == 2) data[key[i]] = get_rand_float(1e9 + 7);
      else if (rand == 3) data[key[i]] = get_rand_string(get_rand_int(16, 240));
      else data[key[i]] = get_date();
    }
    datas[cur] = data;
  }
  return datas;
}
var get_data_from_json = function(knum, dnum) {
  var data = null;
  try {
    data = fs.readFileSync(file_path);
  } catch(err) {
    throw err;
  }
  var cur = 0;
  var datas = [];
  var json = JSON.parse(data.toString());
  return json;
  for (var i in json) {
    datas[cur++] = json[i];
    if (cur >= dnum) break;
  }
  return datas;
}
var Insert = function(db, isIndex, knum, dnum, get_data) {
  try {
    datas = get_data(knum, dnum);
  } catch(err) {
    console.log(err);
    return;
  }
  var collection = db.collection('test');
  collection.insert(datas, function(err, result) {
    if (err) {
      console.log('Error: ' + err);
      db.close();
      return;
    }
    if (!isIndex) {
      console.log("数据插入完成！");
      db.close();
    }
  });
  if (isIndex) {
    console.log("建立索引...");
    collection.ensureIndex(key[0], function(err, result) {
      if (err) {
        console.log('Error: ' + err);
        return;
      }
      console.log("索引建立完毕！");
      db.close();
    });
  }
}
var Query = function(db, callback) {
  var collection = db.collection('test');
  collection.find().toArray(function(err, result) {
    if (err) {
      console.log("Error: " + err);
      return;
    }
    callback(result);
  });
}
var Delete = function(db) {
  var collection = db.collection('test');
  Query(db, function(result) {
    for (var i = 0; i < result.length; ++i) {
      collection.remove(result[i], function(err, res) {
        if (err) {
          console.log("Error: " + err);
          return;
        }
      });
    }
    console.log("删除完成！");
    db.close();
  });
}
var Update = function(db) {
  var collection = db.collection('test');
  Query(db, function(result) {
    for (var i = 0; i < result.length; ++i) {
      var tmp = {};
      for (var k in result[i]) {
        if (k == "_id") continue;
        var type = typeof result[i][k];
        if (type == "number") tmp[k] = get_rand_float(1e9 + 7);
        else if (type == "string") tmp[k] = get_rand_string(get_rand_int(16, 240));
        else if (type == "object") tmp[k] = get_rand_object();
        else tmp[k] = get_date();
      }
      collection.update(result[i], tmp, function(err, res) {
        if (err) {
          console.log("Error: " + err);
          return;
        }
      });
    }
    console.log("更新完成！");
    db.close();
  });
}

var show_help = function() {
  console.log("Usage: node " + argv[1] + " [options]");
  console.log("");
  console.log("query           设定此选项以使程序查询 MongoDB 中的指定数据或所有数据");
  console.log("insert          设定此选项以使程序向 MongoDB 中插入指定数据或随机数据");
  console.log("update          设定此选项以使程序更新 MongoDB 中指定的数据或所有数据");
  console.log("delete          设定此选项以使程序删除 MongoDB 中指定的数据或所有数据");
  console.log("");
  console.log("insert options: ");
  console.log("以下选项仅当设定选项 insert 之后启用，其他时候无效");
  console.log("with_index      设定此选项使插入数据后构造索引（仅当插入的表中没有数据时构建）");
  console.log("key_number=     设定此选项并给出一个整数表示每条数据包含的 key 的数目");
  console.log("data_number=    设定此选项并给出一个整数表示具体插入的数据条数");
  console.log("from=           设定此选项并给出一个路径名表示包含 key-value 的 JSON 文件，设定此选项则key_number选项无效");
}

var main = function(type, index = false) {
  mongo_client.connect(db_url, function(err, db) {
    if (!err) console.log("连接成功");
    if (type == "insert") {
      if (file_path == null) {
        Insert(db, index, key_num, data_num, get_rand_data);
      } else {
        Insert(db, index, key_num, data_num, get_data_from_json);
      }
    } else if (type == "query") {
      Query(db, function(result) {
        for (var i = 0; i < result.length; ++i) {
          console.log(result[i]);
        }
        db.close();
      });
    } else if (type == "delete") {
      Delete(db);
    } else if (type == "update") {
      Update(db);
    } else if (type == "help") {
      show_help();
      db.close();
      process.exit(0);
    } else {
      console.log("function argument wrong");
      db.close();
      process.exit(0);
    }
  });
}

main(type, isIndex);
