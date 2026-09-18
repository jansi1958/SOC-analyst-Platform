from datetime import datetime

from database.crud import save_alert, get_recent_alerts
from detection.threat_score import calculate_threat_score
from detection.threat_intel import check_ip_reputation
from detection.ips_engine import block_ip

def create_alert(
    alert_type,
    severity,
    source_ip,
    description,
    packet_size=0,
    protocol="OTHER",
    destination_port=0
):

    # INITIAL THREAT SCORE CALCULATION
    score, risk_level = calculate_threat_score(
        packet_size, protocol, destination_port
    )

    # EXPLAINABLE AI (XAI) FORMATTING
    xai_bullets = [description]
    if packet_size > 1000:
        xai_bullets.append(f"Packet size unusually high ({packet_size} bytes)")
    if protocol in ["ICMP", "UDP"]:
        xai_bullets.append(f"Uncommon or high-risk protocol used ({protocol})")
    if destination_port in [22, 23, 445, 3389]:
        xai_bullets.append(f"Destination port {destination_port} is frequently targeted")
        
    xai_text = "Reason:<br>" + "<br>".join([f"- {b}" for b in xai_bullets])

    # CHECK GLOBAL THREAT INTELLIGENCE
    intel = check_ip_reputation(source_ip)
    if intel["is_known_malicious"]:
        score = min(100.0, score + 35.0) # Boost score significantly
        xai_text += f"<br><br>[GLOBAL] <b>OSINT:</b> Known Malicious IP! Confidence: {intel['score']}%. Origin: {intel['country']}"

    # RE-EVALUATE RISK LEVEL
    if score >= 75.0:
        risk_level = "HIGH"
    elif score >= 40.0:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    alert = {
        "timestamp": str(datetime.now()),
        "alert_type": alert_type,
        "severity": severity,
        "source_ip": source_ip,
        "description": xai_text,
        "threat_score": score,
        "risk_level": risk_level
    }

    # TRIGGER ACTIVE DEFENSE (IPS)
    if risk_level == "HIGH":
        block_ip(source_ip)

    # SAVE ALERT TO POSTGRESQL/SQLITE
    save_alert(
        alert_type,
        severity,
        source_ip,
        xai_text,
        score,
        risk_level
    )

    print("\n")
    print("*** ALERT GENERATED ***")
    print(alert)
    print("\n")


def get_alerts():
    return get_recent_alerts(1000)