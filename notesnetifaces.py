addresses = netifaces.ifaddresses('eth0')
conn = addresses[2]
ipv4addr = conn[0]['addr']

