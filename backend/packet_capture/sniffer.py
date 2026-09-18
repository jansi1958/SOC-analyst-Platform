from scapy.all import sniff, IP, TCP, UDP, ICMP

from datetime import datetime

import sys
import os
import csv

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            '..'
        )
    )
)

from detection.rule_based_detector import detect_anomaly
from detection.ml_detector import NetworkMLDetector
from detection.ueba_engine import UEBAEngine
from detection.rate_tracker import RateTracker
from database.crud import save_packet

# CSV FILE PATH
csv_file = os.path.join(os.path.dirname(__file__), "..", "logs", "network_traffic.csv")

# CREATE CSV FILE IF NOT EXISTS
os.makedirs(os.path.dirname(csv_file), exist_ok=True)
if not os.path.exists(csv_file):

    with open(csv_file, mode="w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            "Timestamp",
            "Source_IP",
            "Destination_IP",
            "Protocol",
            "Source_Port",
            "Destination_Port",
            "Packet_Size"
        ])

# INITIALIZE AI DETECTOR
ai_detector = NetworkMLDetector(csv_file)

# INITIALIZE UEBA ENGINE
ueba_detector = UEBAEngine()

# INITIALIZE RATE TRACKER
rate_detector = RateTracker(time_window=30, threshold=100)

def process_packet(packet):

    if packet.haslayer(IP):

        # TIMESTAMP
        timestamp = datetime.now()

        # IP INFO
        source_ip = packet[IP].src
        destination_ip = packet[IP].dst

        # PACKET SIZE
        packet_size = len(packet)

        # DEFAULT VALUES
        protocol_name = "OTHER"
        source_port = "N/A"
        destination_port = "N/A"

        # TCP
        if packet.haslayer(TCP):

            protocol_name = "TCP"

            source_port = packet[TCP].sport
            destination_port = packet[TCP].dport

        # UDP
        elif packet.haslayer(UDP):

            protocol_name = "UDP"

            source_port = packet[UDP].sport
            destination_port = packet[UDP].dport

        # ICMP
        elif packet.haslayer(ICMP):

            protocol_name = "ICMP"

        # DISPLAY PACKET
        print("\n========== PACKET DETECTED ==========")

        print(f"Timestamp        : {timestamp}")
        print(f"Source IP        : {source_ip}")
        print(f"Destination IP   : {destination_ip}")
        print(f"Protocol         : {protocol_name}")
        print(f"Source Port      : {source_port}")
        print(f"Destination Port : {destination_port}")
        print(f"Packet Size      : {packet_size} bytes")

        print("=====================================")

        # RUN RULE-BASED ANOMALY DETECTION
        detect_anomaly(
            source_ip,
            destination_ip,
            protocol_name,
            source_port,
            destination_port,
            packet_size
        )

        # RUN AI ANOMALY DETECTION
        ai_detector.predict_packet(
            source_ip,
            destination_ip,
            protocol_name,
            source_port,
            destination_port,
            packet_size
        )

        # RUN UEBA BEHAVIORAL DETECTION
        ueba_detector.analyze_behavior(
            source_ip,
            packet_size,
            protocol_name,
            destination_port
        )

        # RUN RATE TRACKER (DDOS/PORT SCAN)
        rate_detector.check_rate(
            source_ip,
            protocol_name,
            destination_port
        )

        # SAVE TO POSTGRESQL
        save_packet(
            source_ip,
            destination_ip,
            protocol_name,
            source_port,
            destination_port,
            packet_size
        )

        # SAVE TO CSV
        with open(csv_file, mode="a", newline="") as file:

            writer = csv.writer(file)

            writer.writerow([
                timestamp,
                source_ip,
                destination_ip,
                protocol_name,
                source_port,
                destination_port,
                packet_size
            ])


print("Starting packet capture and logging...\n")

sniff(
    prn=process_packet,
    store=False
)