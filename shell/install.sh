#!/bin/bash

# install some library
read systemInfo < /etc/issue
systemInfo=${systemInfo%% *}
if [ "$systemInfo" = "Ubuntu" ]; then
  sudo apt-get -y upgrade
  sudo apt-get install -y g++ cmake libbz2-dev libaio-dev bison zlib1g-dev libsnappy-dev
  sudo apt-get install -y libgflags-dev libreadline6-dev libncurses5-dev libssl-dev liblz4-dev gdb git
  sudo apt-get install -y build-essential python-pip python-dev python3-dev
  sudo apt-get install -y openjdk-8-jdk
else
  sudo yum -y upgrade
  sudo yum install -y gcc-g++ cmake gdb libssl-devel git
  sudo yum install -y python-pip python-devel
fi

# install shadowsocks
if [ ! -f "/etc/shadowsocks.json" ]; then
  pip install --upgrade pip
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
  echo -e "{\n \
  \"server\":\"$shadowsocks_server\",\n \
  \"server_port\":$shadowsocks_port,\n \
  \"local_address\":\"127.0.0.1\",\n \
  \"local_port\":1080,\n \
  \"password\":\"$shadowsocks_password\",\n \
  \"timeout\":600,\n \
  \"method\":\"aes-256-cfb\",\n \
  \"fast-open\":false,\n \
  \"workers\":1\n \
}" > /etc/shadowsocks.json
fi

# install ubuntu themes and clean
if [ "$systemInfo" = "Ubuntu" -a ! -f "/usr/share/doc/ultra-flat-icons" ]; then
  sudo apt-get -y update
  sudo apt-get -y upgrade
  sudo apt-get -y remove libreoffice-common
  sudo apt-get -y remove unity-webapps-common
  sudo apt-get -y install unity-tweak-tool
  sudo add-apt-repository ppa:noobslab/themes
  sudo apt-get -y update
  sudo apt-get install -y flatabulous-theme
  sudo add-apt-repository ppa:noobslab/icons
  sudo apt-get update
  sudo apt-get install -y ultra-flat-icons
fi

# install chrome in ubuntu and remove firefox
if [ "$systemInfo" = "Ubuntu" -a ! -f "/usr/bin/google-chrome" ]; then
  sudo wget http://www.linuxidc.com/files/repo/google-chrome.list -P /etc/apt/sources.list.d/
  wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
  sudo apt-get update -y
  sudo apt-get install -y google-chrome-stable
  sudo apt-get remove -y firefox
  sudo apt-get -y autoremove
fi

# install typora
if [ "$systemInfo" = "Ubuntu" -a ! -f "/usr/bin/typora" ]; then
  sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys BA300B7755AFCFAE
  sudo add-apt-repository 'deb https://typora.io linux/'
  sudo apt-get update -y
  sudo apt-get install -y typora
fi

# install boost
if [ ! -f boost_1_64_0.tar.bz2 ]; then
  wget https://dl.bintray.com/boostorg/release/1.64.0/source/boost_1_64_0.tar.bz2
fi
tar jxvf boost_1_64_0.tar.bz2
cd boost_1_64_0
./bootstrap.sh
./b2 install
cd ..

# emmm...

echo "Okay! All your need has been installed."
