#!/bin/bash

# Use this file to connect the other hosts
# If you want to use it, please specify ~/.CONNECT_HOST like this:
# [GroupName]
# username host_ip
# blank line for the group end
# 
# Examples:
# [spark]
# root 10.198.255.194
# root 10.198.255.195
# root 10.198.255.196
# root 10.198.255.197
# root 10.198.255.198
# root 10.198.255.199
# root 10.198.255.200
# root 10.198.255.201
# root 10.198.255.202
# root 10.198.255.203
#
# [sparkonk8s]
# root 172.21.51.42
# root 10.198.21.134 
#
# EOF

FILE_NOT_EXIST=-1
PARAMETER_LOSS=-2

HOSTS_FILE=~/.CONNECT_HOST

if [ ! -f $HOSTS_FILE ]; then
  echo "Plese use $HOSTS_FILE to specify the hosts group and username and ip."
  exit $FILE_NOT_EXIST
fi

declare -i i=0
declare -i row_num=0
declare -i col_num=0

while read line
do
  if [[ $line =~ \[(.*?)\] ]]; then
    group=$(echo $line | cut -d '[' -f2 | cut -d ']' -f1)
    groups[$i]=$group
    i=$i+1
  else
    if [[ $line =~ ^$ ]]; then
      row_num=$row_num+1
      col_num=0
    else
      arr_line=($line)
      username=${arr_line[0]}
      ip=${arr_line[1]}
      eval host_ip_group_$row_num[$col_num]=$ip
      eval host_username_group_$row_num[$col_num]=$username
      col_num=$col_num+1
    fi
  fi
done < $HOSTS_FILE

# echo ${groups[@]}
# for ((i=0;i<row_num;i++))
# do
#   eval echo \${host_ip_group_$i[@]}
#   eval echo \${host_username_group_$i[@]}
# done

group_info="Please choise a group:"
host_info="Please choise a host:"

for ((i=0;i<row_num;i++))
do
  group_info=$group_info"\n\t"$i." "${groups[$i]}
done
echo -e $group_info
read -p "your choice: " group

eval host_number=\${#host_ip_group_$group[@]}
eval validation=\${#host_username_group_$group[@]}
if [ $host_number -ne $validation ]; then
  echo "You must specify a username or ip for every host in ~/.CONNECT_HOST"
  exit $PARAMETER_LOSS
fi
for ((i=0;i<$host_number;i++))
do
  eval ip=\${host_ip_group_$group[$i]}
  eval username=\${host_username_group_$group[$i]}
  host_info=$host_info"\n\t"$i." "$username"\t"$ip
done
echo -e $host_info
read -p "your choice: " host

eval ip=\${host_ip_group_$group[$host]}
eval username=\${host_username_group_$group[$host]}
ssh $username@$ip
