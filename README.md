# DDoS Attack Scripts using Scapy

<p align="center">
  <img src="https://img.shields.io/badge/language-python-blue.svg">
  <img src="https://img.shields.io/badge/library-Scapy-green.svg">
</p>

This repository contains Python scripts that demonstrate various DDoS (Distributed Denial of Service) attack techniques implemented using the Scapy library. Scapy is a powerful packet manipulation and network analysis tool. The scripts provide examples of different attack protocols (UDP or TCP) and attack types (Tear Drop, Syn Flood, Syn-Ack Flood, Ack Flood, and Fin Flood). These scripts are **strictly for educational purposes** and should not be used for malicious activities. DDoS attacks are illegal and unethical.

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

## ⚙️ Usage

1. **Clone the repository** to your local machine.
2. **Install dependencies** using `pip install -r requirements.txt`.
3. **Run the desired attack script** by executing `python attack_script.py`.
4. **Enter the following parameters:**
   - Target server IP
   - Target server port
   - Attack protocol (UDP or TCP)
   - Attack type (Tear Drop, UDP Flood, Syn Flood, Syn-Ack Flood, Ack Flood, or Fin Flood)
   - Number of attack iterations
   - Number of source IP addresses to generate
5. **Monitor the attack progress** through the provided progress bar.

**Note:** Always ensure you have the necessary permissions and only use these scripts for ethical and educational purposes. Unauthorized use of these scripts is illegal and unethical.

---

<p align="center">
  <b>Happy Ethical Hacking! 🛡️</b>
</p>
