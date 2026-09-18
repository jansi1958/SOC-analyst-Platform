import os
import time
from fastapi import APIRouter
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

try:
    from google import genai
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False

router = APIRouter()

class AlertRequest(BaseModel):
    alert_type: str
    severity: str
    source_ip: str
    description: str
    protocol: str
    packet_size: int
    destination_port: int

@router.post("/generate-report")
def generate_report(alert: AlertRequest):
    api_key = os.getenv("GEMINI_API_KEY")
    
    prompt = f"""
You are an expert Cybersecurity SOC Analyst. An anomaly was detected on our network.
Write a concise Incident Response Plan for the following alert:

Alert Type: {alert.alert_type}
Severity: {alert.severity}
Source IP: {alert.source_ip}
Protocol: {alert.protocol}
Destination Port: {alert.destination_port}
Packet Size: {alert.packet_size} bytes
Description: {alert.description}

Please provide:
1. Threat Analysis (What is likely happening)
2. Immediate Actions (What to block or investigate)
3. Mitigation Strategy (How to prevent it in the future)
    """

    # If the user has the SDK and an API key in their environment
    if HAS_GENAI and api_key:
        try:
            client = genai.Client(api_key=api_key)
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt
            )
            return {"report": response.text}
        except Exception as e:
            print(f"GenAI Error in generate_report: {e}")
            pass # Fall back to mock on error
            
    # Mock Fallback Response (For Demos without an API Key)
    time.sleep(1.5) # Simulate AI thinking
    
    mock_report = f"""
### 1. Threat Analysis
The system has detected a **{alert.alert_type}** originating from `{alert.source_ip}` over **{alert.protocol}**. 
Given the packet size of {alert.packet_size} bytes and destination port {alert.destination_port}, this pattern strongly resembles automated reconnaissance, lateral movement, or an exploit attempt typical of a compromised host. The behavior matches: *{alert.description}*.

### 2. Immediate Actions
*   **Isolate the Host:** Temporarily quarantine IP `{alert.source_ip}` at the network firewall layer.
*   **Inspect Traffic:** Review full PCAP logs for port {alert.destination_port} to identify if any malicious payload was successfully executed.
*   **Check Endpoints:** Verify if the source device has up-to-date endpoint protection (EDR) active.

### 3. Mitigation Strategy
*   Implement strict Rate Limiting for {alert.protocol} traffic on this subnet.
*   Review your Zero-Trust architecture policies regarding lateral movement.
*   *Note: This is an AI-generated mock response since no GEMINI_API_KEY was found in the environment.*
    """
    
    return {"report": mock_report.strip()}

class ChatRequest(BaseModel):
    message: str

@router.post("/chat")
def chat_with_agent(request: ChatRequest):
    api_key = os.getenv("GEMINI_API_KEY")
    
    # Context
    try:
        from database.crud import get_recent_alerts
        alerts = get_recent_alerts(5)
        context = "Recent network anomalies:\n" + "\n".join([f"- {a['alert_type']} from {a['source_ip']} (Risk: {a['risk_level']})" for a in alerts])
    except:
        context = "No recent anomalies."
        
    prompt = f"""
You are 'Sentinel', an advanced AI Cybersecurity Agent built into a SOC Dashboard.
You speak concisely and professionally like JARVIS. Use this context if relevant:
{context}

User: {request.message}
Response:"""

    if HAS_GENAI and api_key:
        try:
            client = genai.Client(api_key=api_key)
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt
            )
            return {"reply": response.text}
        except Exception as e:
            print(f"GenAI Error in chat_with_agent: {e}")
            pass
            
    time.sleep(1)
    mock = f"I am Sentinel. In this limited simulation mode (no API key detected), I am observing {len(alerts) if 'alerts' in locals() else 0} recent anomalies. My Active Defense systems are online."
    return {"reply": mock}
