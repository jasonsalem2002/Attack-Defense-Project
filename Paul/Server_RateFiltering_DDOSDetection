
import socket
import time
import threading


# Server IP and port
server_ip = '0.0.0.0'  # Listen on all available network interfaces
server_port = 12345  # Choose an available port


# Define UDP server settings
UDP_IP = "0.0.0.0"  # Listen on all available network interfaces
UDP_PORT = 12345  # port to be agreed on with attack team

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

# Rate limiting parameters
tokens = 10  # Initial number of tokens in the bucket
token_rate = 5  # Tokens replenished per second
token_bucket_capacity = 10  # Maximum number of tokens in the bucket

# Lock for thread safety
token_lock = threading.Lock()


# Token bucket replenishment thread
def replenish_tokens():
    global tokens
    while True:
        time.sleep(1.0 / token_rate)
        with token_lock:
            if tokens < token_bucket_capacity:
                tokens += 1


# Start the token replenishment thread
token_thread = threading.Thread(target=replenish_tokens)
token_thread.daemon = True
token_thread.start()

while True:
    data, addr = sock.recvfrom(1024)  # Adjust buffer size as needed

    with token_lock:
        if tokens > 0:
            # Process the received message here (e.g., print or store it)
            print(f"Received message from {addr}: {data.decode('utf-8')}")
            tokens -= 1
        else:
            # Rate limit exceeded, drop the message or take appropriate action
            print(f"Rate limit exceeded for {addr}. Dropping message. POSSIBLE DDOS ATTACK ONGOING from {addr}")
            # You can implement actions like logging, alerting, or dropping here.

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

