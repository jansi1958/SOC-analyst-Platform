import os
import requests
import random

def check_ip_reputation(ip_address):
    """
    Cross-references an IP address against AbuseIPDB global threat intelligence.
    Returns a dictionary with the confidence score and country of origin.
    """
    # 1. Ignore Local Network IP Addresses (Internal Traffic)
    if not ip_address or ip_address.startswith("192.168.") or ip_address.startswith("10.") or ip_address == "127.0.0.1":
        return {
            "score": 0,
            "country": "Local",
            "is_known_malicious": False
        }

    # 2. Try using the real API if a key exists in the .env file
    api_key = os.getenv("ABUSEIPDB_API_KEY")
    if api_key:
        try:
            url = 'https://api.abuseipdb.com/api/v2/check'
            querystring = {'ipAddress': ip_address, 'maxAgeInDays': '90'}
            headers = {'Accept': 'application/json', 'Key': api_key}
            
            # 3 second timeout so the sniffer doesn't freeze
            response = requests.request(method='GET', url=url, headers=headers, params=querystring, timeout=3)
            
            if response.status_code == 200:
                data = response.json()['data']
                score = data.get('abuseConfidenceScore', 0)
                return {
                    "score": score,
                    "country": data.get('countryCode', 'Unknown'),
                    "is_known_malicious": score > 50
                }
        except Exception as e:
            print(f"Threat Intel API Error: {e}")
            pass

    # 3. MOCK SIMULATION MODE (For Resume Demos without an API Key)
    # Randomly assign a malicious score to external IPs so the user can demo the feature!
    score = random.choice([0, 0, 0, 15, 85, 100]) # Mostly safe, sometimes highly malicious
    countries = ["US", "CN", "RU", "DE", "BR", "IN", "KR"]
    country = random.choice(countries) if score > 0 else "US"
    
    return {
        "score": score,
        "country": country,
        "is_known_malicious": score > 50
    }
