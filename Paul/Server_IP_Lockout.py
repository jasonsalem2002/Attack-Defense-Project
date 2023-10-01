import socket
import time
from collections import defaultdict
from scapy.all import *

# Define server IP and port
server_ip = '0.0.0.0'  # Listen on all available network interfaces
server_port = 12345  # Choose an available port

# Define rate limiting parameters
packet_limit = 1  # Maximum packets per IP
time_period = 20  # Time period in seconds
lockout_duration = 300  # Lockout duration in seconds

# Create a UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((server_ip, server_port))

print(f"Listening for UDP packets on {server_ip}:{server_port}")

# Dictionary to keep track of packet counts and lockout times for each IP
ip_packet_counts = defaultdict(int)
ip_lockout_times = {}

# Global variable for tracking detected Tear Drop attack
tear_drop_detected = False

# Define the maximum packet payload size threshold
max_packet_payload_size = 1472  # Set this to the desired threshold


def detect_teardrop(fragments):
    global tear_drop_detected
    # Check if the fragments form a Tear Drop pattern
    if len(fragments) >= 2:
        for i in range(len(fragments) - 1):
            current_frag = fragments[i]
            next_frag = fragments[i + 1]

            # Check for overlapping offsets or incorrect ordering
            if (current_frag.frag <= next_frag.frag and current_frag.frag + len(current_frag) > next_frag.frag) or \
                    (current_frag.frag >= next_frag.frag and current_frag.frag < next_frag.frag + len(next_frag)):
                tear_drop_detected = True


while True:
    # Receive data from the client
    data, client_address = server_socket.recvfrom(2048)
    client_ip = client_address[0]

    # Check if the client IP is locked out
    if client_ip in ip_lockout_times and time.time() < ip_lockout_times[client_ip]:
        print(f"IP {client_ip} is locked out. Ignoring packet.")
        continue

    # Check if the client has exceeded the packet limit for the time period
    if ip_packet_counts[client_ip] >= packet_limit:
        print(f"IP {client_ip} has exceeded the packet limit. Locking out for {lockout_duration} seconds.")
        ip_lockout_times[client_ip] = time.time() + lockout_duration
        ip_packet_counts[client_ip] = 0  # Reset packet count

    # Decode and process the received data
    message = data.decode()
    print(f"Received from {client_address}: {message}")

    # Create a packet object for further analysis
    packet = IP(data)

    # Detect Tear Drop attack by analyzing fragment patterns
    if packet.haslayer(IP) and packet[IP].frag > 0:
        fragments = packet[IP].payload  # Get the payload of the IP layer
        detect_teardrop([fragments])  # Pass the payload as a single fragment to the detection function

        # Print the fragmented packets received
        print(f"Fragmented packet received from {client_ip}:\n{packet.summary()}")

    # Check if a Tear Drop attack is detected
    if tear_drop_detected:
        print("Tear Drop attack detected!")

    # Define the maximum packet payload size threshold
    if len(packet) >= max_packet_payload_size:
        print(f"Maximum-sized packet received from {client_ip}!\n")
