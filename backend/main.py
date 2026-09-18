from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from api.analytics_api import router as analytics_router
from api.traffic_api import router as traffic_router
from api.alert_api import router as alert_router
from api.llm_api import router as llm_router
from api.graph_api import router as graph_router
from api.report_api import router as report_router

app = FastAPI()

# ENABLE CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# INCLUDE ROUTES
app.include_router(traffic_router)
app.include_router(alert_router)
app.include_router(analytics_router)
app.include_router(llm_router)
app.include_router(graph_router)
app.include_router(report_router)


import os
from fastapi.responses import FileResponse

@app.get("/")
def home():
    frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend", "index.html")
    if os.path.exists(frontend_path):
        return FileResponse(frontend_path)
    
    return {
        "message":
        "AI-Powered Network Anomaly Detection System Running"
    }