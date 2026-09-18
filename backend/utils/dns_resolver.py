import socket
import threading

# In-memory dictionary to store IP -> Domain translations
dns_cache = {}

def async_resolve(ip):
    """
    Background worker that contacts the internet's DNS servers
    to translate a raw IP into a human-readable domain name.
    """
    try:
        # gethostbyaddr returns a tuple: (hostname, aliaslist, ipaddrlist)
        hostname = socket.gethostbyaddr(ip)[0]
        dns_cache[ip] = hostname
    except Exception:
        # If the IP doesn't have a registered domain (or request times out),
        # map it to itself so we don't keep retrying it forever.
        dns_cache[ip] = ip

def get_hostname(ip):
    """
    Returns the domain name for an IP if known.
    If not known, returns the IP instantly and spawns a background thread to look it up.
    """
    if not ip or type(ip) != str:
        return ip
        
    # Ignore internal local network addresses
    if ip.startswith("192.168.") or ip.startswith("10.") or ip.startswith("172.") or ip == "127.0.0.1":
        return ip
        
    # If we already resolved it, return the clean domain name!
    if ip in dns_cache:
        return dns_cache[ip]
        
    # Mark it as 'in progress' so we don't spawn 500 threads for the same IP
    dns_cache[ip] = ip 
    
    # Spawn the background worker. This ensures the API response has ZERO lag!
    threading.Thread(target=async_resolve, args=(ip,), daemon=True).start()
    
    return ip
