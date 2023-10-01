# Attack.py

`attack.py` is a Python script that demonstrates a simple network attack implementation using Scapy and multithreading. This script allows you to perform either a Tear Drop or Maximum Packet Size attack on a specified server with randomized source IP addresses.

## Prerequisites

- Python 3.x
- [Scapy](https://scapy.net/) installed (`pip install scapy`)
- tqdm library installed (`pip install tqdm`)

## Usage

1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/jasonsalem2002/Attack-Defense-Project.git
   cd Attack-Defense-Project

2. Run the script
   ```bash
   sudo python3 attack.py

### How It Works

The script employs multithreading to send a specified number of malicious packets to a target server. Users can choose between two attack types:

1. **Tear Drop Attack:**
   - Fragments IP packets to create overlapping fragments, causing the server's operating system to crash.
   - Uses randomized source IP addresses to obfuscate the attacker's identity.
  
2. **Maximum Packet Size Attack:**
   - Creates UDP packets with maximum payload size (1472 bytes) and randomizes source IP addresses.
   - Floods the server with large packets, potentially overwhelming its network interface.


### Code Overview

- **Global Variables:**
  - `sent_packets`: Tracks the number of sent packets.
  - `start_time`: Records the attack start time.
  
- **Functions:**
  - `log_results(attack_type, packets_sent, duration)`: Logs attack results to a file.
  - `generate_random_ip()`: Generates a random IP address.
  - `send_tear_drop_packet(server_ip, server_port, source_ips, count, progress_bar)`: Conducts Tear Drop attack.
  - `send_udp_packet(server_ip, server_port, source_ips, count, progress_bar)`: Conducts Maximum Packet Size attack.
  - `main()`: Main function to handle user input and initiate the attack.

### Note

- Ensure you have permission to test the script against the specified server.
- Use responsibly and ethically; unauthorized DDoS attacks are illegal.
