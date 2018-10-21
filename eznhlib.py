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

def readUserInput(inputFile):
    f = open(inputFile, 'r')
    r = f.read()
    s = str(r.encode('utf-8')).strip().rstrip()
    string = s
    return string

def menu_parser(menu):
    options_list = {}
    menu = str(menu)
    menu = menu.splitlines()
    counter = 1
    for item in menu:
        option = str(item.encode('utf-8')).rstrip().strip()
        print '\t\t',str(counter),'\t\t\t',option
        options_list[counter] = option
        counter += 1
    print options_list
    return options_list
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
