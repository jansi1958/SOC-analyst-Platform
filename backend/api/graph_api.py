from fastapi import APIRouter
from database.connection import SessionLocal
from database.models import TrafficLog
from sqlalchemy import func

router = APIRouter()

@router.get("/graph-data")
def get_graph_data():
    """
    Returns nodes and links for the 3D Network Graph visualization.
    """
    db = SessionLocal()
    try:
        # Query database for all unique source-destination pairs and count their packets
        connections = db.query(
            TrafficLog.source_ip, 
            TrafficLog.destination_ip, 
            func.count(TrafficLog.id).label('weight')
        ).group_by(TrafficLog.source_ip, TrafficLog.destination_ip).all()
        
        nodes_set = set()
        links = []
        
        for src, dst, weight in connections:
            nodes_set.add(src)
            nodes_set.add(dst)
            # Add the link connecting source to destination
            links.append({"source": src, "target": dst, "weight": weight})
            
        # Build node list. Group 1 = Internal (Local), Group 2 = External
        nodes = []
        for ip in nodes_set:
            group = 1 if ip.startswith("192.168") or ip == "127.0.0.1" else 2
            nodes.append({"id": ip, "group": group})
        
        return {"nodes": nodes, "links": links}
    finally:
        db.close()
