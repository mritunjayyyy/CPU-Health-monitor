# **System Monitor API**

This is a FastAPI-based application that monitors system health in real-time. It provides metrics such as CPU usage, memory usage, disk space, and network latency. It also supports configurable alert thresholds and notifies users when critical limits are exceeded.

## **Features**

- **Real-time system monitoring**: Tracks CPU, memory, disk, and network latency metrics.
- **Alert notifications**: Configurable thresholds for CPU and memory usage with notifications when limits are breached.
- **Secure access**: Basic authentication implemented for all API endpoints.
- **Dockerized**: The application can be easily deployed using Docker.

---

## **API Endpoints**

### **1. `/health` [GET]**
- **Description**: Fetches the current system health metrics.
- **Response**:
  ```json
  {
    "cpu": 15.5,
    "memory": 45.2,
    "disk": 70.1,
    "latency": 5.4
  }
2. /config-alerts [POST]
Description: Configures the alert thresholds for CPU and memory usage.
Authentication Required: Yes
Request:
json
{
  "cpu": 80.0,
  "memory": 90.0
}
Response:
json
{
  "message": "Alert thresholds updated successfully.",
  "thresholds": {
    "cpu": 80.0,
    "memory": 90.0
  }
}
Setup Instructions
1. Prerequisites
Python 3.8 or higher
Git installed (download here)
Docker installed (download here)

2. Clone the Repository
bash
git clone https://github.com/your-username/system-monitor-api.git
cd system-monitor-api

3. Install Dependencies
Create and activate a virtual environment:
bash
python -m venv venv
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
Install dependencies:
bash
pip install -r requirements.txt

4. Run the Application
To start the application locally:
bash
uvicorn main:app --reload
The API will be available at: http://127.0.0.1:8000.

5. Run with Docker
Build the Docker image:
bash
docker build -t system-monitor-api .

# Run the container:
bash
docker run -p 8000:8000 system-monitor-api
Access the API at: http://127.0.0.1:8000.

# Authentication:
All endpoints require basic authentication.
Default credentials:
Username: admin
Password: password

# Alerting Functionality:
Alerts trigger notifications when system metrics exceed defined thresholds:
Example thresholds:
CPU usage > 80%
Memory usage > 90%

# Testing the API:
You can test the API using curl, Postman, or any REST client.

# Example POST /config-alerts request using curl:
bash
curl -u admin:password -X POST http://127.0.0.1:8000/config-alerts \
-H "Content-Type: application/json" \
-d '{"cpu": 80.0, "memory": 90.0}'

# Contributing:
Contributions are welcome! Feel free to fork the repository and submit pull requests.

# License
This project is licensed under the MIT License. See the LICENSE file for details.
