# DDoS Attack and Prevention System

<p align="center">
  <img src="https://img.shields.io/badge/language-python-blue.svg">
  <img src="https://img.shields.io/badge/library-Scapy-green.svg">
</p>

This repository contains Python scripts that demonstrate both DDoS (Distributed Denial of Service) attack techniques implemented using the Scapy library, and a DDoS detection and prevention system. Scapy is a powerful packet manipulation and network analysis tool. The scripts provide examples of different attack protocols (UDP or TCP) and attack types (Tear Drop, Syn Flood, Syn-Ack Flood, Ack Flood, and Fin Flood). Additionally, the system includes modules for detecting and mitigating these attacks. These scripts are **strictly for educational purposes** and should not be used for malicious activities. DDoS attacks are illegal and unethical.

## 🎯 Attack Procedures

### 1. Tear Drop Attack
The Tear Drop attack involves sending IP packets with overlapping fragments. This confuses the targeted system, causing it to crash or become unresponsive.

#### **Procedure:**
- Generate random source IP addresses.
- Create two overlapping fragments with randomized payload.
- Send the fragments to the target server.

### 2. UDP Flood Attack
The UDP Flood attack floods the target server with UDP packets. This overwhelms the server's resources and makes it unreachable for legitimate users.

#### **Procedure:**
- Generate random source IP addresses.
- Create UDP packets with randomized source IP and maximum payload size.
- Send the UDP packets to the target server.

### 3. Syn Flood Attack
The Syn Flood attack exploits the TCP protocol's handshake process by sending a flood of SYN packets, overwhelming the server and preventing it from accepting legitimate connections.

#### **Procedure:**
- Send a flood of SYN packets to the target server without completing the TCP handshake.

### 4. Syn-Ack Flood Attack
The Syn-Ack Flood attack involves sending a flood of TCP packets with the SYN-ACK flags set, overwhelming the target server and disrupting its operations.

#### **Procedure:**
- Send a flood of TCP packets with SYN-ACK flags set to the target server.

### 5. Ack Flood Attack
The Ack Flood attack floods the target server with TCP packets containing only the ACK flag. This attack consumes server resources and affects its performance.

#### **Procedure:**
- Send a flood of TCP packets with only the ACK flag set to the target server.

### 6. Fin Flood Attack
The Fin Flood attack sends a large number of TCP packets with the FIN flag set, disrupting the connection and causing the server to spend resources on handling incomplete connections.

#### **Procedure:**
- Send a flood of TCP packets with the FIN flag set to the target server.

## 🛡️ DDoS Detection and Prevention

### Server Configuration

#### UDP Server:
- **IP:** `0.0.0.0` (Listen on all available network interfaces)
- **Port:** `12345`

#### TCP Server:
- **IP:** `0.0.0.0` (Listen on all available network interfaces)
- **Port:** `54321`

### UDP DDoS Detection

#### Threshold-based Detection

1. **Packet Rate Monitoring:**
   - Incoming UDP packets are monitored for packet rate per IP address.
   - If a client IP exceeds the predefined packet rate threshold, it is considered a potential DDoS attack.

2. **Rate Limiting and Lockout:**
   - Exceeding the packet rate threshold results in a lockout of the client IP for `300 seconds` (5 minutes).

#### Tear Drop Attack Detection

1. **Fragment Analysis:**
   - UDP packets with fragments are analyzed for overlapping offsets, indicating a potential Tear Drop attack.
   - Detected Tear Drop attacks are flagged for further action.

### TCP DDoS Detection

#### SYN, SYN-ACK, and FIN Flood Detection

1. **Packet Counting:**
   - Incoming TCP packets are counted separately for SYN, SYN-ACK, and FIN flags per client IP.
   - Counting is done in a rolling window of `5 minutes`.

2. **Threshold-based Detection:**
   - If the number of SYN, SYN-ACK, or FIN packets exceeds the threshold within the rolling window, it is considered a potential flood attack.

3. **Rate Limiting and Lockout:**
   - Client IPs exceeding the threshold are blocked for `30 minutes`.

### Implementation Details

#### Threads and Sniffing

1. **UDP and TCP Processing Threads:**
   - Separate threads are used to process UDP and TCP packets concurrently.
   - Each thread processes packets according to the defined detection logic.

2. **Packet Sniffing:**
   - Scapy is utilized for packet sniffing to capture and analyze incoming TCP packets.
   - Packet handlers identify SYN, SYN-ACK, and FIN packets for counting and analysis.

## ⚙️ Usage and Running the System

### Prerequisites:
- Ensure Python and the required libraries (`socket` and `scapy`) are installed.

### Running the System:
- Execute the provided code to start the UDP and TCP processing threads.
- The system will begin monitoring and detecting DDoS attacks based on the predefined thresholds and logic.

### Monitoring:
- Detected attacks, blocked IPs, and other relevant information are logged in the console output.
- Adjust thresholds, lockout durations, and other parameters as needed based on network conditions and attack patterns.

---

<p align="center">
  <b>Stay Secure! 🛡️ Happy Ethical Hacking! 🛡️</b>
</p>
