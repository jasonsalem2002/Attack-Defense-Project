import socket

# Server IP and port
server_ip = '127.0.0.1'  # Replace with the actual server IP
server_port = 12345  # Replace with the actual server port

# Create a UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Message to send
message = "This is the message to send 100 times."

for _ in range(100):
    # Send the message to the server
    client_socket.sendto(message.encode(), (server_ip, server_port))

# Close the socket
client_socket.close()
