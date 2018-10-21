#!/bin/sh
SHELL=/bin/bash

# Only required if you do not use a full Kali Linux installation or a partial installation
# Otherwise, the distro should have the prerequisite apt packages installed

sudo pip install -r requirements.txt
sudo apt-get update
sudo apt-get install -y parprouted mitmf bdfproxy mitmproxy hamster-sidejack responder

