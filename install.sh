#!/bin/bash

read systemInfo < /etc/issue
systemInfo=${systemInfo%% *}
if [ "$systemInfo" = "Ubuntu" ]; then
  sudo apt-get upgrade
  sudo apt-get install -y g++ cmake libbz2-dev libaio-dev bison zlib1g-dev libsnappy-dev
  sudo apt-get install -y libgflags-dev libreadline6-dev libncurses5-dev libssl-dev liblz4-dev gdb git
  sudo apt-get install -y build-essential python-pip python-dev python3-dev
else
  sudo yum upgrade
  sudo yum install -y gcc-g++ cmake gdb libssl-devel git
  sudo yum install python-pip python-devel
fi

# install shadowsocks
pip install shadowsocks
shadowsocks_server=
shadowsocks_port=443
shadowsocks_password=
echo -n "Please input shadowsocks server ip: "
read shadowsocks_server
echo -n "Please input shadowsocks server port[default 443]: "
read shadowsocks_port
echo -n "Please input shadowsocks password: "
stty -echo
read shadowsocks_password
stty echo
echo -n "{\n \
\"server\":\"$shadowsocks_server\",\n \
\"server_port\":$shadowsocks_port,\n \
\"local_address\":\"127.0.0.1\",\n \
\"local_port\":1080,\n \
\"password\":\"$shadowsocks_password\", \
\"timeout\":600,\n \
\"method\":\"aes-256-cfb\",\n \
\"fast-open\":false,\n \
\"workers\":1\n \
}" > /etc/shadowsocks.json

# install boost
wget https://dl.bintray.com/boostorg/release/1.64.0/source/boost_1_64_0.tar.bz
cd boost_1_64_0
./bootstrap.sh
./b2 install
cd ..

# emmm...

echo "Okay! All your need has been installed."
