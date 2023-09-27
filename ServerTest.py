import socket

# Server IP and port
server_ip = '0.0.0.0'  # Listen on all available network interfaces
server_port = 12345  # Choose an available port

# Create a UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the server address
server_socket.bind((server_ip, server_port))

print(f"Listening for UDP packets on {server_ip}:{server_port}")

while True:
    # Receive data from the client
    data, client_address = server_socket.recvfrom(1024)

    # Decode and print the received data
    message = data.decode()
    print(f"Received from {client_address}: {message}")
