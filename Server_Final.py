import socket
import time
import threading
from collections import defaultdict
from scapy.all import *

# Define server IP and ports for UDP and TCP
udp_server_ip = '0.0.0.0'  # Listen on all available network interfaces for UDP
udp_server_port = 12345  # Choose an available UDP port

tcp_server_ip = '0.0.0.0'  # Listen on all available network interfaces for TCP
tcp_server_port = 54321  # Choose an available TCP port

# Define rate limiting parameters for UDP
udp_packet_limit = 1  # Maximum packets per IP
udp_time_period = 20  # Time period in seconds
udp_lockout_duration = 300  # Lockout duration in seconds

# Threshold for UDP packet rate (packets per second)
udp_attack_threshold = 1000  # Adjust this value based on your traffic patterns

# Dictionary to store UDP packet counts per second
udp_packet_counts = {}

# Function to detect and respond to UDP attacks
def detect_udp_attack():
    while True:
        current_time = time.time()
        total_packets = sum(udp_packet_counts.values())

        if total_packets > udp_attack_threshold:
            print(f"Possible UDP DDoS attack detected with {total_packets} packets/s")

        udp_packet_counts.clear()

        time.sleep(1)

# Create a UDP socket
udp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the UDP socket to the server address
udp_server_socket.bind((udp_server_ip, udp_server_port))

print(f"Listening for UDP packets on {udp_server_ip}:{udp_server_port}")

# Start the UDP detection thread
udp_detection_thread = threading.Thread(target=detect_udp_attack)
udp_detection_thread.daemon = True
udp_detection_thread.start()

# Dictionary to keep track of UDP packet counts and lockout times for each IP
udp_ip_packet_counts = defaultdict(int)
udp_ip_lockout_times = {}

# Global variable for tracking detected UDP Tear Drop attack
udp_tear_drop_detected = False

# Define the maximum packet payload size threshold for UDP
udp_max_packet_payload_size = 1472  # Set this to the desired threshold

def detect_udp_teardrop(fragments):
    global udp_tear_drop_detected
    # Check if the fragments form a Tear Drop pattern for UDP
    if len(fragments) >= 2:
        for i in range(len(fragments) - 1):
            current_frag = fragments[i]
            next_frag = fragments[i + 1]

            # Check for overlapping offsets or incorrect ordering for UDP
            if (current_frag.frag <= next_frag.frag and current_frag.frag + len(current_frag) > next_frag.frag) or \
                    (current_frag.frag >= next_frag.frag and current_frag.frag < next_frag.frag + len(next_frag)):
                udp_tear_drop_detected = True

# Function to process incoming UDP packets
def process_udp_packets():
    while True:
        # Receive data from the UDP client
        data, client_address = udp_server_socket.recvfrom(2048)
        client_ip = client_address[0]

        # Check if the UDP client IP is locked out
        if client_ip in udp_ip_lockout_times and time.time() < udp_ip_lockout_times[client_ip]:
            print(f"UDP IP {client_ip} is locked out. Ignoring packet.")
            continue

        # Check if the UDP client has exceeded the packet limit for the time period
        elif udp_ip_packet_counts[client_ip] >= udp_packet_limit:
            print(f"UDP IP {client_ip} has exceeded the packet limit. Locking out for {udp_lockout_duration} seconds.")
            udp_ip_lockout_times[client_ip] = time.time() + udp_lockout_duration
            udp_ip_packet_counts[client_ip] = 0  # Reset packet count

        # Update UDP packet count for the current second
        current_second = int(time.time())
        udp_packet_counts[current_second] = udp_packet_counts.get(current_second, 0) + 1

        # Decode and process the received UDP data
        message = data.decode()
        print(f"Received UDP from {client_address}: {message}")

        # Update the UDP packet count for the client
        udp_ip_packet_counts[client_ip] += 1

        packet = IP(data)

        # Detect UDP Tear Drop attack by analyzing fragment patterns
        if packet.haslayer(IP) and packet[IP].frag > 0:
            fragments = packet[IP].payload  # Get the payload of the IP layer for UDP
            detect_udp_teardrop([fragments])  # Pass the payload as a single fragment to the detection function for UDP

        # Check if a UDP Tear Drop attack is detected
        if udp_tear_drop_detected:
            print("UDP Tear Drop attack detected!")

        # Define the maximum packet payload size threshold for UDP
        if len(packet) >= udp_max_packet_payload_size:
            print(f"Maximum-sized UDP packet received from {client_ip}!")

# Create a TCP socket
tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the TCP socket to the server address
tcp_server_socket.bind((tcp_server_ip, tcp_server_port))

print(f"Listening for TCP packets on {tcp_server_ip}:{tcp_server_port}")

# Function to process incoming TCP packets
def process_tcp_packets():
    # Constants for TCP
    tcp_threshold_per_5_minutes = 50  # Maximum number of packets allowed per 5 minutes
    tcp_block_duration = 30 * 60  # 30 minutes
    tcp_blocked_ips = {}  # Dictionary to track blocked IPs
    tcp_packet_count = {}  # Dictionary to track packet counts per IP
    tcp_time_interval = 5 * 60  # 5 minutes in seconds

    def tcp_block_ip(ip):
        tcp_blocked_ips[ip] = time.time() + tcp_block_duration

    def tcp_is_blocked(ip):
        return ip in tcp_blocked_ips and time.time() < tcp_blocked_ips[ip]

    def tcp_reset_packet_count(ip):
        tcp_packet_count[ip] = {"SYN": 0, "SYN-ACK": 0, "FIN": 0, "timestamp": 0}

    def tcp_packet_handler(pkt):
        if IP in pkt and TCP in pkt:
            src_ip = pkt[IP].src
            current_time = time.time()
            if not tcp_is_blocked(src_ip):
                if src_ip not in tcp_packet_count:
                    tcp_reset_packet_count(src_ip)

                # Check if the time interval has passed (5 minutes)
                if current_time - tcp_packet_count[src_ip]["timestamp"] > tcp_time_interval:
                    tcp_reset_packet_count(src_ip)

                if pkt[TCP].flags & 0x02:  # SYN flag set
                    tcp_packet_count[src_ip]["SYN"] += 1

                if pkt[TCP].flags & 0x12:  # SYN-ACK flag set
                    tcp_packet_count[src_ip]["SYN-ACK"] += 1

                if pkt[TCP].flags & 0x01:  # FIN flag set
                    tcp_packet_count[src_ip]["FIN"] += 1

                if tcp_packet_count[src_ip]["SYN"] > tcp_threshold_per_5_minutes:
                    print(f"Potential TCP SYN flood attack from {src_ip}")
                    tcp_block_ip(src_ip)
                    print(f"Blocked {src_ip} for {tcp_block_duration} seconds")
                    tcp_reset_packet_count(src_ip)

                if tcp_packet_count[src_ip]["SYN-ACK"] > tcp_threshold_per_5_minutes:
                    print(f"Potential TCP SYN-ACK flood attack from {src_ip}")
                    tcp_block_ip(src_ip)
                    print(f"Blocked {src_ip} for {tcp_block_duration} seconds")
                    tcp_reset_packet_count(src_ip)

                if tcp_packet_count[src_ip]["FIN"] > tcp_threshold_per_5_minutes:
                    print(f"Potential TCP FIN flood attack from {src_ip}")
                    tcp_block_ip(src_ip)
                    print(f"Blocked {src_ip} for {tcp_block_duration} seconds")
                    tcp_reset_packet_count(src_ip)

                tcp_packet_count[src_ip]["timestamp"] = current_time

    # Start packet capture for TCP
    sniff(filter="tcp", prn=tcp_packet_handler)

# Start processing UDP and TCP packets concurrently using threads
udp_thread = threading.Thread(target=process_udp_packets)
tcp_thread = threading.Thread(target=process_tcp_packets)

udp_thread.start()
tcp_thread.start()

# Wait for both threads to finish
udp_thread.join()
tcp_thread.join()
