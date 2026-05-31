# ☁️ CLF-C02 Practice Exam Portal — Containerized Edition

A fully containerized online exam portal for AWS CLF-C02 certification practice.
This is a migration of an AWS-native serverless architecture to a container-based
deployment using Docker, making it infrastructure-portable and self-hosted.

---

## 🔄 Architecture Evolution

| Component     | AWS Native (v1)         | Containerized (v2)       |
|---------------|-------------------------|--------------------------|
| Frontend      | Static HTML on S3       | Nginx container          |
| Backend       | AWS Lambda (Python)     | Flask container          |
| Database      | Amazon DynamoDB         | PostgreSQL container     |
| API Layer     | AWS API Gateway         | Flask routes             |
| Deployment    | Fully managed by AWS    | Docker Compose on EC2    |
| Portability   | AWS only                | Any server or cloud      |

---

## 🏗️ Architecture

```
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
```

---

## 📁 Project Structure

```
examproject/
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
```

---

## ✨ Features

### Student Side
- 700+ question bank
- 100 random questions per session
- 90 minute countdown timer
- Mark questions for review
- Session preserved on page refresh
- Instant score and result on submission

### Admin Side
- View all exam results in a table
- Filter by name, batch, date, pass/fail status
- Summary stats — total appeared, passed, failed, average score
- Export results to CSV

---

## 🚀 Quick Start

### Prerequisites
- Docker
- Docker Compose

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/clf-c02-exam-portal.git
cd clf-c02-exam-portal
```

### 2. Update the server IP
In `frontend/index.html` update:
```javascript
DYNAMO_API_ENDPOINT: 'http://YOUR_SERVER_IP:5000/exam-results'
```

In `frontend/admin.html` update:
```javascript
const BACKEND = 'http://YOUR_SERVER_IP:5000'
```

### 3. Start all containers
```bash
docker compose up -d
```

### 4. Access the application
| Page         | URL                              |
|--------------|----------------------------------|
| Exam Portal  | http://YOUR_SERVER_IP            |
| Admin Panel  | http://YOUR_SERVER_IP/admin.html |
| Health Check | http://YOUR_SERVER_IP:5000/health|
| Results API  | http://YOUR_SERVER_IP:5000/results|

---

## 🐳 Docker Details

### Images Used
| Service   | Base Image        | Purpose              |
|-----------|-------------------|----------------------|
| frontend  | nginx:alpine      | Serve static HTML    |
| backend   | python:3.12-slim  | Run Flask API        |
| db        | postgres:16-alpine| Store exam results   |

### Container Communication
```
frontend  → depends on → backend
backend   → depends on → db
db        → no dependencies
```

All containers communicate via Docker internal network.
Only frontend (port 80) and backend (port 5000) are exposed externally.
Database is internal only — not accessible from outside.

---

## 🔌 API Endpoints

| Method | Endpoint        | Description              |
|--------|-----------------|--------------------------|
| GET    | /health         | Check backend status     |
| POST   | /exam-results   | Save exam result         |
| GET    | /results        | Get all results          |
| GET    | /results?name=  | Filter by student name   |
| GET    | /results?batch= | Filter by batch          |
| GET    | /results?date=  | Filter by date           |
| GET    | /results?passed=| Filter by pass/fail      |

---

## 🗄️ Database Schema

```sql
CREATE TABLE exam_results (
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
```

---

## 🛠️ Useful Commands

```bash
# Start all containers
docker compose up -d

# Stop all containers
docker compose down

# View logs
docker compose logs -f

# View logs of specific service
docker compose logs -f backend

# Rebuild after code changes
docker compose build
docker compose up -d

# Access database
docker exec -it examproject-db-1 psql -U postgres -d examdb

# Check running containers
docker compose ps
```

---

## 🔒 Security Notes

- Database is not exposed to the public internet
- CORS enabled on Flask backend
- For production — use environment variables for passwords via `.env` file
- Admin panel currently accessible via URL — add authentication before production use

---

## 📌 Roadmap

- [ ] Student registration and login system
- [ ] Admin login with authentication
- [ ] Question bank management via CSV/Excel upload
- [ ] Exam-ID and passkey system
- [ ] Multiple exam support
- [ ] Leaderboard per batch
- [ ] CI/CD pipeline with GitHub Actions

---

## 🧑‍💻 Tech Stack

- **Frontend** — HTML, CSS, JavaScript, Nginx
- **Backend** — Python, Flask, Flask-CORS
- **Database** — PostgreSQL
- **Containerization** — Docker, Docker Compose
- **Infrastructure** — AWS EC2

---

## 📝 License

MIT License — free to use and modify.
