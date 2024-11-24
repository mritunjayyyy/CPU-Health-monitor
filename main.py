import time
import psutil
import threading
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.status import HTTP_401_UNAUTHORIZED
import smtplib
from email.message import EmailMessage

# Initialize the app
app = FastAPI()

# Security setup
security = HTTPBasic()
VALID_USERNAME = "admin"
VALID_PASSWORD = "password"

def authenticate(credentials: HTTPBasicCredentials):
    if credentials.username != VALID_USERNAME or credentials.password != VALID_PASSWORD:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

# Alert thresholds
alert_thresholds = {
    "cpu": 80.0,  # Default CPU threshold
    "memory": 96.0  # Default memory threshold
}

# Current system status
system_status = {
    "cpu_usage": 0.0,
    "mem_usage": 0.0
}

# Monitoring thread
def monitor_system(interval=1):
    while True:
        system_status["cpu_usage"] = psutil.cpu_percent(interval=interval)
        system_status["mem_usage"] = psutil.virtual_memory().percent
        check_alerts()

def check_alerts():
    """
    Checks if the current metrics exceed thresholds and triggers alerts.
    """
    if system_status["cpu_usage"] > alert_thresholds["cpu"]:
        notify(f"High CPU Usage Alert: {system_status['cpu_usage']}%")
    if system_status["mem_usage"] > alert_thresholds["memory"]:
        notify(f"High Memory Usage Alert: {system_status['mem_usage']}%")

def notify(message: str):
    """
    Logs the alert to the console and sends an email notification.
    """
    print(f"ALERT: {message}")

    # Sending email
    try:
        sender_email = "nakulsharma1503@gmail.com"
        recipient_email = "mritunjsharma@gmail.com"
        subject = "System Alert"
        email_body = message

        msg = EmailMessage()
        msg.set_content(email_body)
        msg["Subject"] = subject
        msg["From"] = sender_email
        msg["To"] = recipient_email

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, "shfr ipwn iypr qwqi")
            server.send_message(msg)

        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

# Background thread for monitoring
threading.Thread(target=monitor_system, daemon=True).start()

# API Endpoints
@app.get("/health")
def get_health(credentials: HTTPBasicCredentials = Depends(security)):
    """
    Returns the current health of the system.
    """
    authenticate(credentials)
    return {
        "cpu_usage": system_status["cpu_usage"],
        "memory_usage": system_status["mem_usage"]
    }

@app.get("/alert")
def get_alert(credentials: HTTPBasicCredentials = Depends(security)):
    """
    Returns an alert if a metric exceeds the configured threshold.
    """
    authenticate(credentials)
    alerts = {}
    if system_status["cpu_usage"] > alert_thresholds["cpu"]:
        alerts["cpu_alert"] = f"High CPU usage: {system_status['cpu_usage']}%"
    if system_status["mem_usage"] > alert_thresholds["memory"]:
        alerts["memory_alert"] = f"High Memory usage: {system_status['mem_usage']}%"
    return alerts or {"status": "System is healthy."}

class AlertConfig(BaseModel):
    cpu: float = 80.0
    memory: float = 96.0

@app.post("/config-alerts")
def set_alerts(config: AlertConfig, credentials: HTTPBasicCredentials = Depends(security)):
    """
    Configures alert thresholds for CPU and memory usage.
    """
    authenticate(credentials)
    alert_thresholds["cpu"] = config.cpu
    alert_thresholds["memory"] = config.memory
    return {"message": "Alert thresholds updated successfully.", "thresholds": alert_thresholds}
