from scapy.all import *
from scapy.layers.inet import UDP, IP

# Server IP and port
server_ip = '127.0.0.1'  # Replace with the actual server IP
server_port = 12345  # Replace with the actual server port

# List of source IP addresses to use
source_ips = ['192.168.1.100', '192.168.1.101', '192.168.1.102']  # Replace with actual source IPs

while True:
    # Choose a random source IP address
    source_ip = random.choice(source_ips)

    # Input message from the user
    message = input("Enter a message to send (or 'exit' to quit): ")

    if message.lower() == 'exit':
        break

    # Create a UDP packet with a randomized source IP
    udp_packet = IP(src=source_ip, dst=server_ip) / UDP(dport=server_port) / message

    # Send the packet
    send(udp_packet)

# Close the socket