import subprocess
import os

# Keep track of IPs we've already tried to block to prevent spamming rules
blocked_ips = set()

def block_ip(ip_address):
    """
    Actively blocks an attacking IP address using Windows Firewall.
    Requires the Python process to be running with Administrator privileges.
    """
    # Don't block local loopback or already blocked IPs
    if ip_address in blocked_ips or ip_address in ["127.0.0.1", "localhost", "0.0.0.0"]:
        return
        
    print(f"\n[IPS] 🛡️ ACTIVE DEFENSE ENGAGED! Attempting to block malicious IP: {ip_address}")
    
    # Windows netsh command to add an inbound block rule
    cmd = f'netsh advfirewall firewall add rule name="Sentinel_Block_{ip_address}" dir=in action=block remoteip={ip_address}'
    
    try:
        # Execute the command
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"[IPS] ✅ SUCCESS: Permanently blocked {ip_address} at the firewall layer.")
        else:
            # If it fails, it's almost certainly because the terminal is not running as Admin
            print(f"[IPS] ⚠️ WARNING: Failed to write firewall rule. Ensure you are running this terminal as Administrator.")
            
        # Add to set so we don't try blocking the same IP 100 times per second
        blocked_ips.add(ip_address)
            
    except Exception as e:
        print(f"[IPS] ❌ Error executing firewall command: {e}")
