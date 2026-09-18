from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database.connection import Base

class TrafficLog(Base):
    __tablename__ = "traffic_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    source_ip = Column(String)
    destination_ip = Column(String)
    protocol = Column(String)
    source_port = Column(Integer)
    destination_port = Column(Integer)
    packet_size = Column(Integer)


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)

    timestamp = Column(DateTime, default=datetime.utcnow)

    alert_type = Column(String)

    severity = Column(String)

    source_ip = Column(String)

    description = Column(String)

    threat_score = Column(Integer)

    risk_level = Column(String)