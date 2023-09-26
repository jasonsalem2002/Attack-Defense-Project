from scapy.all import IP, UDP, Raw, send

# Create a custom IP packet
custom_ip_packet = IP(src="192.168.1.100", dst="192.168.1.200") 
custom_udp_packet = UDP(sport=12345, dport=80)  
custom_data = b"Custom payload data goes here"  

# Combine the IP, UDP, and payload layers
packet = custom_ip_packet / custom_udp_packet / Raw(load=custom_data)

# Send the packet
send(packet, verbose=0)


# use scapy to create a custom packet
# use iptables to block incoming traffic

