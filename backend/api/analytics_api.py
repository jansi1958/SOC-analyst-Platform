# pyrefly: ignore [missing-import]
from fastapi import APIRouter
# pyrefly: ignore [missing-import]
from sqlalchemy import func

from database.connection import SessionLocal
from database.models import TrafficLog, Alert

router = APIRouter()


@router.get("/stats")
def get_stats():

    db = SessionLocal()

    try:

        total_packets = db.query(TrafficLog).count()

        total_alerts = db.query(Alert).count()

        high_risk_alerts = (
            db.query(Alert)
            .filter(Alert.risk_level == "HIGH")
            .count()
        )

        avg_threat_score = db.query(func.avg(Alert.threat_score)).scalar() or 0.0

        return {
            "total_packets": total_packets,
            "total_alerts": total_alerts,
            "high_risk_alerts": high_risk_alerts,
            "avg_threat_score": round(avg_threat_score, 2)
        }

    finally:
        db.close()


@router.get("/top-attackers")
def top_attackers():

    db = SessionLocal()

    try:

        attackers = (
            db.query(
                Alert.source_ip,
                func.count(Alert.id).label("alert_count")
            )
            .group_by(Alert.source_ip)
            .order_by(func.count(Alert.id).desc())
            .limit(5)
            .all()
        )

        return [
            {
                "source_ip": row.source_ip,
                "alerts": row.alert_count
            }
            for row in attackers
        ]

    finally:
        db.close()


@router.get("/recent-alerts")
def recent_alerts():

    db = SessionLocal()

    try:

        alerts = (
            db.query(Alert)
            .order_by(Alert.id.desc())
            .limit(20)
            .all()
        )

        return [
            {
                "id": alert.id,
                "alert_type": alert.alert_type,
                "severity": alert.severity,
                "source_ip": alert.source_ip,
                "risk_level": alert.risk_level,
                "threat_score": alert.threat_score
            }
            for alert in alerts
        ]

    finally:
        db.close()


@router.get("/threat-summary")
def threat_summary():

    db = SessionLocal()

    try:

        high = (
            db.query(Alert)
            .filter(Alert.risk_level == "HIGH")
            .count()
        )

        medium = (
            db.query(Alert)
            .filter(Alert.risk_level == "MEDIUM")
            .count()
        )

        low = (
            db.query(Alert)
            .filter(Alert.risk_level == "LOW")
            .count()
        )

        return {
            "HIGH": high,
            "MEDIUM": medium,
            "LOW": low
        }

    finally:
        db.close()