☁️ CLF-C02 Practice Exam Portal — Containerized
A fully containerized online exam portal for AWS CLF-C02 certification practice. This is a migration of an AWS-native serverless architecture to a container-based deployment using Docker, making it infrastructure-portable and self-hosted.

🔄 Architecture Evolution
ComponentAWS Native (v1)Containerized (v2)FrontendStatic HTML on S3Nginx containerBackendAWS Lambda (Python)Flask containerDatabaseAmazon DynamoDBPostgreSQL containerAPI LayerAWS API GatewayFlask routesDeploymentFully managed by AWSDocker Compose on EC2CI/CDManual deploymentGitHub ActionsPortabilityAWS onlyAny server or cloud

🏗️ Architecture
Student Browser
      │
      ▼
┌─────────────┐
│    Nginx    │  Port 80  (Frontend)
│  Container  │
└──────┬──────┘
       │ API calls
       ▼
┌─────────────┐
│    Flask    │  Port 5000  (Backend)
│  Container  │
└──────┬──────┘
       │ SQL queries
       ▼
┌─────────────┐
│  PostgreSQL │  Internal only  (Database)
│  Container  │
└─────────────┘

📁 Project Structure
examproject/
├── .github/
│   └── workflows/
│       └── ci.yml        # GitHub Actions CI/CD pipeline
├── frontend/
│   ├── index.html        # Exam portal (700+ questions)
│   ├── admin.html        # Admin results dashboard
│   └── Dockerfile        # Nginx image
├── backend/
│   ├── app.py            # Flask API
│   ├── requirements.txt  # Python dependencies
│   └── Dockerfile        # Python image (multi-stage)
├── docker-compose.yml    # Multi-container orchestration
└── README.md

✨ Features
Student Side

700+ question bank
100 random questions per session
90 minute countdown timer
Mark questions for review
Session preserved on page refresh
Instant score and result on submission

Admin Side

View all exam results in a table
Filter by name, batch, date, pass/fail status
Summary stats — total appeared, passed, failed, average score
Export results to CSV


🚀 Quick Start
Prerequisites

Docker
Docker Compose

1. Clone the repository
bashgit clone https://github.com/yourusername/clf-c02-exam-portal.git
cd clf-c02-exam-portal
2. Update the server IP
In frontend/index.html update:
javascriptDYNAMO_API_ENDPOINT: 'http://YOUR_SERVER_IP:5000/exam-results'
In frontend/admin.html update:
javascriptconst BACKEND = 'http://YOUR_SERVER_IP:5000'
3. Start all containers
bashdocker compose up -d
4. Access the application
PageURLExam Portalhttp://YOUR_SERVER_IPAdmin Panelhttp://YOUR_SERVER_IP/admin.htmlHealth Checkhttp://YOUR_SERVER_IP:5000/healthResults APIhttp://YOUR_SERVER_IP:5000/results

🔁 CI/CD Pipeline
This project uses GitHub Actions for automated deployment to AWS EC2 on every push to master.
Pipeline Flow
Push to master
      ↓
GitHub Actions triggered
      ↓
SSH into EC2 (via Appleboy)
      ↓
git pull origin master
      ↓
docker-compose up -d --build
      ↓
✅ Live on EC2
Workflow file: .github/workflows/ci.yml
yamlname: aws-mock-cicd

on:
  push:
    branches: ["master"]
    paths-ignore:
      - "README.md"

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Deploy to EC2
        uses: appleboy/ssh-action@v0.1.10
        with:
          host: ${{ secrets.EC2_HOST }}
          username: ${{ secrets.EC2_USER }}
          key: ${{ secrets.EC2_KEY }}
          script: |
            cd /home/ec2-user/AWS-CLF-C02-Practice-Exam-Portal-Containerized
            git pull origin master
            docker-compose up -d --build
GitHub Secrets Required
Go to Repo → Settings → Secrets → Actions and add:
SecretDescriptionEC2_HOSTYour EC2 public IP addressEC2_USEREC2 username (usually ec2-user)EC2_KEYContents of your .pem private key file

🐳 Docker Details
Images Used
ServiceBase ImagePurposefrontendnginx:alpineServe static HTMLbackendpython:3.12-slimRun Flask APIdbpostgres:16-alpineStore exam results
Container Communication
frontend  → depends on → backend
backend   → depends on → db
db        → no dependencies
All containers communicate via Docker internal network. Only frontend (port 80) and backend (port 5000) are exposed externally. Database is internal only — not accessible from outside.

🔌 API Endpoints
MethodEndpointDescriptionGET/healthCheck backend statusPOST/exam-resultsSave exam resultGET/resultsGet all resultsGET/results?name=Filter by student nameGET/results?batch=Filter by batchGET/results?date=Filter by dateGET/results?passed=Filter by pass/fail

🗄️ Database Schema
sqlCREATE TABLE exam_results (
    id               SERIAL PRIMARY KEY,
    session_id       VARCHAR(100),
    student_name     VARCHAR(200),
    batch            VARCHAR(100),
    score            INTEGER,
    total_questions  INTEGER,
    percentage       INTEGER,
    passed           BOOLEAN,
    exam_start_time  VARCHAR(50),
    exam_end_time    VARCHAR(50),
    date             VARCHAR(20),
    time_elapsed     INTEGER,
    exam_type        VARCHAR(100),
    created_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

🛠️ Useful Commands
bash# Start all containers
docker-compose up -d

# Stop all containers
docker-compose down

# View logs
docker-compose logs -f

# View logs of specific service
docker-compose logs -f backend

# Rebuild after code changes
docker-compose build
docker-compose up -d

# Access database
docker exec -it examproject-db-1 psql -U postgres -d examdb

# Check running containers
docker-compose ps

🔒 Security Notes

Database is not exposed to the public internet
CORS enabled on Flask backend
GitHub Secrets used for EC2 credentials — never hardcoded
For production — use environment variables for passwords via .env file
Admin panel currently accessible via URL — add authentication before production use


📌 Roadmap

 Student registration and login system
 Admin login with authentication
 Question bank management via CSV/Excel upload
 Exam-ID and passkey system
 Multiple exam support
 Leaderboard per batch
 CI/CD pipeline with GitHub Actions ✅


🧑‍💻 Tech Stack

Frontend — HTML, CSS, JavaScript, Nginx
Backend — Python, Flask, Flask-CORS
Database — PostgreSQL
Containerization — Docker, Docker Compose
CI/CD — GitHub Actions
Infrastructure — AWS EC2


📝 License
MIT License — free to use and modify.
