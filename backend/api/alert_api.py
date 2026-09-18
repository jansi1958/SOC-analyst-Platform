from fastapi import APIRouter
from alerts.alert_manager import get_alerts

router = APIRouter()

@router.get("/alerts")
def fetch_alerts():

    return {
        "alerts":
        get_alerts()
    }