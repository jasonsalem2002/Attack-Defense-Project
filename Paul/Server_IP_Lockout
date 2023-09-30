import socket
import time
from collections import defaultdict

# Define server IP and port
server_ip = '0.0.0.0'  # Listen on all available network interfaces
server_port = 12345  # Choose an available port

# Define rate limiting parameters
packet_limit = 1  # Maximum packets per IP
time_period = 20  # Time period in seconds
lockout_duration = 300  # Lockout duration in seconds

# Create a UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the server address
server_socket.bind((server_ip, server_port))

print(f"Listening for UDP packets on {server_ip}:{server_port}")

# Dictionary to keep track of packet counts and lockout times for each IP
ip_packet_counts = defaultdict(int)
ip_lockout_times = {}

while True:
    # Receive data from the client
    data, client_address = server_socket.recvfrom(1024)
    client_ip = client_address[0]

    # Check if the client IP is locked out
    if client_ip in ip_lockout_times and time.time() < ip_lockout_times[client_ip]:
        print(f"IP {client_ip} is locked out. Ignoring packet.")
        continue

    # Check if the client has exceeded the packet limit for the time period
    elif ip_packet_counts[client_ip] >= packet_limit:
        print(f"IP {client_ip} has exceeded the packet limit. Locking out for {lockout_duration} seconds.")
        ip_lockout_times[client_ip] = time.time() + lockout_duration
        ip_packet_counts[client_ip] = 0  # Reset packet count

    # Decode and process the received data
    message = data.decode()
    print(f"Received from {client_address}: {message}")

    # Update the packet count for the client
    ip_packet_counts[client_ip] += 1
