import time
from collections import defaultdict
from alerts.alert_manager import create_alert

class RateTracker:
    def __init__(self, time_window=30, threshold=100):
        """
        Tracks packet rates per IP over a sliding time window.
        :param time_window: The time window in seconds (e.g., 30)
        :param threshold: Number of packets allowed within the window before triggering an alert
        """
        self.time_window = time_window
        self.threshold = threshold
        # Dictionary storing a list of packet timestamps for each IP
        self.ip_history = defaultdict(list)
        # Prevent spamming the dashboard with alerts from the same IP
        self.alerted_ips = set()

    def check_rate(self, source_ip, protocol, destination_port):
        """
        Called every time a packet arrives. Cleans up old packets and checks the current count.
        """
        current_time = time.time()
        
        # Log this packet's timestamp
        self.ip_history[source_ip].append(current_time)
        
        # Calculate the cutoff time for our sliding window (e.g., exactly 30 seconds ago)
        cutoff_time = current_time - self.time_window
        
        # Filter out all packet timestamps that happened BEFORE the cutoff time
        self.ip_history[source_ip] = [t for t in self.ip_history[source_ip] if t > cutoff_time]
        
        # How many packets happened within the current window?
        packet_count = len(self.ip_history[source_ip])
        
        # If the count breaks our limit, trigger an anomaly alert!
        if packet_count > self.threshold and source_ip not in self.alerted_ips:
            self.alerted_ips.add(source_ip)
            
            # THIS IS THE EXACT RECRUITER-FRIENDLY DESCRIPTION!
            desc = f"{source_ip} generated {packet_count} {protocol} requests within {self.time_window} seconds. Possible DDoS or Port Scan attack."
            
            create_alert(
                alert_type="High-Velocity Packet Flood",
                severity="HIGH",
                source_ip=source_ip,
                description=desc,
                packet_size=0,
                protocol=protocol,
                destination_port=destination_port
            )
