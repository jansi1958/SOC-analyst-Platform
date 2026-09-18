from database.connection import SessionLocal
from database.models import TrafficLog, Alert


def save_packet(
    source_ip,
    destination_ip,
    protocol,
    source_port,
    destination_port,
    packet_size
):
    db = SessionLocal()

    try:
        packet = TrafficLog(
            source_ip=source_ip,
            destination_ip=destination_ip,
            protocol=protocol,
            source_port=0 if source_port == "N/A" else source_port,
            destination_port=0 if destination_port == "N/A" else destination_port,
            packet_size=packet_size
        )

        db.add(packet)
        db.commit()

    finally:
        db.close()


def save_alert(
    alert_type,
    severity,
    source_ip,
    description,
    threat_score,
    risk_level
):
    db = SessionLocal()

    try:
        alert = Alert(
    alert_type=alert_type,
    severity=severity,
    source_ip=source_ip,
    description=description,
    threat_score=threat_score,
    risk_level=risk_level
)

        db.add(alert)
        db.commit()

    finally:
        db.close()

def get_recent_alerts(limit=50):
    db = SessionLocal()
    try:
        # Get overall latest
        recent = db.query(Alert).order_by(Alert.timestamp.desc()).limit(limit).all()
        # Get latest HIGH
        high = db.query(Alert).filter(Alert.risk_level == "HIGH").order_by(Alert.timestamp.desc()).limit(20).all()
        # Get latest MEDIUM
        med = db.query(Alert).filter(Alert.risk_level == "MEDIUM").order_by(Alert.timestamp.desc()).limit(20).all()
        # Get latest LOW
        low = db.query(Alert).filter(Alert.risk_level == "LOW").order_by(Alert.timestamp.desc()).limit(20).all()
        
        # Merge unique alerts
        all_alerts = {a.id: a for a in recent + high + med + low}.values()
        
        # Sort them by timestamp descending again
        sorted_alerts = sorted(all_alerts, key=lambda a: a.timestamp, reverse=True)
        
        return [
            {
                "id": a.id,
                "timestamp": str(a.timestamp),
                "alert_type": a.alert_type,
                "severity": a.severity,
                "source_ip": a.source_ip,
                "description": a.description,
                "threat_score": a.threat_score,
                "risk_level": a.risk_level
            }
            for a in sorted_alerts
        ]
    finally:
        db.close()