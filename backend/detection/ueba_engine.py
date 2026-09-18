import time
from alerts.alert_manager import create_alert

class UEBAEngine:
    def __init__(self):
        """
        Initializes the User Entity Behavior Analytics (UEBA) Engine.
        Profiles are stored in memory to track baseline behavior per IP address.
        """
        self.ip_profiles = {}
        self.WINDOW_SIZE = 5  # Analyze behavior in 5-second windows

    def analyze_behavior(self, source_ip, packet_size, protocol, destination_port):
        current_time = time.time()
        
        # 1. Initialize profile if new IP
        if source_ip not in self.ip_profiles:
            self.ip_profiles[source_ip] = {
                "baseline_bytes_per_sec": 0,
                "window_bytes": 0,
                "window_start": current_time,
                "last_alert_time": 0,
                "windows_processed": 0
            }
            
        profile = self.ip_profiles[source_ip]
        profile["window_bytes"] += packet_size
        
        duration = current_time - profile["window_start"]
        
        # 2. Process window if time is up
        if duration >= self.WINDOW_SIZE:
            current_rate = profile["window_bytes"] / duration
            
            # 3. Check for Anomalous Spikes (if baseline is established)
            if profile["windows_processed"] >= 2:
                # Anomaly: > 300% of baseline AND minimum 5000 bytes/sec 
                # (to avoid alerting on trivial spikes like 10 bytes to 40 bytes)
                if current_rate > (profile["baseline_bytes_per_sec"] * 3) and current_rate > 5000:
                    
                    # Prevent alert spam (only 1 alert per IP every 15 seconds)
                    if current_time - profile["last_alert_time"] > 15:
                        profile["last_alert_time"] = current_time
                        
                        create_alert(
                            alert_type="UEBA Behavioral Spike Detected",
                            severity="HIGH",
                            source_ip=source_ip,
                            description=f"Insider Threat Warning! IP traffic spiked by >300% from its baseline to {int(current_rate)} bytes/sec.",
                            packet_size=packet_size,
                            protocol=protocol,
                            destination_port=destination_port
                        )
            
            # 4. Update the Moving Average Baseline
            if profile["windows_processed"] == 0:
                profile["baseline_bytes_per_sec"] = current_rate
            else:
                # Exponential moving average (80% history, 20% new)
                profile["baseline_bytes_per_sec"] = (profile["baseline_bytes_per_sec"] * 0.8) + (current_rate * 0.2)
                
            # 5. Reset window for the next batch
            profile["window_bytes"] = 0
            profile["window_start"] = current_time
            profile["windows_processed"] += 1
