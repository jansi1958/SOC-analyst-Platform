@echo off
echo Starting AI-Powered Network Anomaly Detection System...

:: Start the FastAPI backend in a new terminal window
start cmd /k "cd backend && uvicorn main:app --reload"

:: Start the packet sniffer in this terminal window
echo Starting packet sniffer...
set PYTHONIOENCODING=utf-8
python backend/packet_capture/sniffer.py
