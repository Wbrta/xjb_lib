var key = [];
var value_type = [];
var db_url = "mongodb://localhost:27017/test";
var mongo_client = require('mongodb').MongoClient;

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
var Insert = function(db, isIndex) {
  var len = get_rand_int(1, 5);
  for (var i = 0; i < len; ++i) {
    key[i] = get_rand_string(get_rand_int(2, 30));
    value_type[i] = get_rand_int((i == 0 ? 1 : 0), 5);
    console.log(key[i]);
  }
  var datas = [];
  len = get_rand_int(1, 5);
  for (var cur = 0; cur < len; ++cur) {
    var data = {};
    for (var i = 0; i < key.length; ++i) {
      var rand = value_type[i];
      if (rand == 0) data[key[i]] = get_rand_object();
      else if (rand == 1) data[key[i]] = get_rand_int(0, 1e9 + 7);
      else if (rand == 2) data[key[i]] = get_rand_float(1e9 + 7);
      else if (rand == 3) data[key[i]] = get_rand_string(get_rand_int(16, 240));
      else data[key[i]] = get_date();
    }
    datas[cur] = data;
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
var Query = function(db, callback, key = null) {
  var collection = db.collection('test');
  collection.find(key).toArray(function(err, result) {
    if (err) {
      console.log("Error: " + err);
      return;
    }
    callback(result);
  });
}
var Delete = function(db, key = null) {
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
  }, key);
}
var Update = function(db, key = null, value = null) {
  var collection = db.collection('test');
  Query(db, function(result) {
    if (value == null) value = [];
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
      value[i] = tmp;
      collection.update(result[i], value[i], function(err, res) {
        if (err) {
          console.log("Error: " + err);
          return;
        }
      });
    }
    console.log("更新完成！");
    db.close();
  }, key);
}

var main = function(type, index = false, key = null) {
  mongo_client.connect(db_url, function(err, db) {
    if (!err) console.log("连接成功");
    if (type == "insert") {
      Insert(db, index);
    } else if (type == "query") {
      Query(db, function(result) {
        for (var i = 0; i < result.length; ++i) {
          console.log(result[i]);
        }
        db.close();
      }, key);
    } else if (type == "delete") {
      Delete(db, key);
    } else if (type == "update") {
      Update(db);
    } else {
      console.log("function argument wrong");
    }
  });
};

var argc = 0;
var argv = [];
var type = "query";

process.argv.forEach(function (val, index, array) {
  argv[argc] = val;
  argc += 1;
});

if (argc != 3) {
  console.log("Usage: node " + argv[1] + " [options]");
  console.log("query   use this options to make program query data in mongodb");
  console.log("insert  use this options to make program insert data into mongodb");
  console.log("update  use this options to make program update data in mongodb");
  console.log("delete  use this options to delete data from mongodb");
  process.exit(1);
}

type = argv[2];

main(type);
