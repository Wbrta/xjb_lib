#!/bin/bash

test_name=
threads_num=1
mysql_storage_engine=rocksdb
time_long=60
table_size=10000
operation=run
mysql_port=3331

echo -n "Please input what test you want to use: "
read test_name
echo -n "Please input how many threads you want to use[default 1]: "
read threads_num
echo -n "Please input what storage engine of mysql you want to use[rocksdb or terarkdb, default rocksdb]: "
read mysql_storage_engine
echo -n "Please input how long you want to excute[default 60]: "
read time_long
echo -n "Please input the row of table[default 10000]: "
read table_size
echo -n "Please input the what kind of operation you want to excute[default run]: "
read operation

if [ "$mysql_storage_engine" = "rocksdb" ]; then
  mysql_port=3331
elif [ "$mysql_storage_engine" = "terarkdb" ]; then
  mysql_port=3330
else
  echo -e "Invalid Input of MySQL Storage Engine. Only rocksdb and terarkdb can be choose."
  exit 1
fi

sysbench \
  --test=/home/wuxueyang/sysbench/share/sysbench/$test_name \
  --db-driver=mysql \
  --mysql-host=127.0.0.1 \
  --mysql-port=$mysql_port \
  --mysql-user=root \
  --mysql-db=test \
  --threads=$threads_num \
  --mysql_storage_engine=rocksdb \
  --time=$time_long \
  --table_size=$table_size \
  $operation > /home/wuxueyang/log_sysbench/result_of_$test_name\_$mysql_storage_engine.log
