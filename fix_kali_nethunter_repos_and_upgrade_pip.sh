# This will fix your repos on your fresh nethunter installation and then upgrade pip to allow you to install the latest required packages
cp -r /etc/apt/sources.list /etc/apt/sources.list.save
cp -r ./sources.list /etc/apt
apt-get update
apt-get install -y python-pip
/bin/sh prerequisite_setup.sh
