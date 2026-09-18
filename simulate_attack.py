import time
from scapy.all import IP, TCP, UDP, send

# Fake Attacker IPs to trigger different alarms
HACKER_IP_1 = "185.15.59.22"   # DDoS Attacker
HACKER_IP_2 = "91.240.118.68"  # Exfiltration Attacker
HACKER_IP_3 = "45.14.224.19"   # Malformed Protocol Attacker

# We send packets out to a random internet IP so the local Wi-Fi interface catches them!
TARGET_IP = "8.8.8.8" 

def simulate_ddos():
    print(f"\n[!] Simulating High-Velocity UDP Flood from {HACKER_IP_1}...")
    # Send 110 packets instantly to trip the 100-packet Rate Limit threshold
    for i in range(110):
        pkt = IP(src=HACKER_IP_1, dst=TARGET_IP)/UDP(dport=80)/b"DDoS_PAYLOAD"
        send(pkt, verbose=False)
    print("[-] Flood complete.")

def simulate_exfiltration():
    print(f"\n[!] Simulating Massive Data Exfiltration from {HACKER_IP_2}...")
    # Send a massive payload to trip the UEBA and Rule-Based large packet detectors
    payload = b"X" * 1600
    pkt = IP(src=HACKER_IP_2, dst=TARGET_IP)/UDP(dport=443)/payload
    send(pkt, verbose=False)
    print("[-] Exfiltration complete.")

def simulate_malformed():
    print(f"\n[!] Simulating Malformed ML Anomaly from {HACKER_IP_3}...")
    # Send traffic on dangerous Telnet port with weird TCP flags
    pkt = IP(src=HACKER_IP_3, dst=TARGET_IP)/TCP(sport=23, dport=445, flags="FPU")
    send(pkt, verbose=False)
    print("[-] Malformed packet complete.")

if __name__ == "__main__":
    print("=== SOC PLATFORM ATTACK SIMULATOR ===")
    print("Ensure the backend (.\\start.bat) is running.")
    print("Starting in 3 seconds...")
    time.sleep(3)
    
    simulate_ddos()
    time.sleep(1)
    
    simulate_exfiltration()
    time.sleep(1)
    
    simulate_malformed()
    
    print("\n[✔] All simulated attacks finished! Check your SOC Dashboard!")
