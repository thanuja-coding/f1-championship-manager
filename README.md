# 🏎️ F1 Championship Manager

### *Because even Formula 1 needs someone to manage the chaos!*

**GitHub Repository:** [https://github.com/thanuja-coding/f1-championship-manager](https://github.com/thanuja-coding/f1-championship-manager)

---

## 1. Problem Statement

Imagine organizing a Formula 1 championship without a proper management system. Drivers are looking for teams, teams are searching for drivers, organizers are scheduling races, and everyone is asking the same question: **"Who is actually leading the championship?"**

Managing all of this manually can quickly turn into a bigger disaster than a last-lap tyre strategy!

The F1 Championship Manager solves this problem by providing a centralized platform to manage drivers, racing teams, championships, race schedules, results, and standings.

Instead of handling everything through spreadsheets, messages, and last-minute confusion, the system brings the entire championship under one roof — so the only chaos left is on the racetrack!

## 2. Project Overview

F1 Championship Manager is a web-based application developed using FastAPI, React, and SQLite. It provides role-based access, secure authentication, team and driver management, championship creation, race scheduling, result submission, and automatic points calculation.

The application also provides interactive API documentation through Swagger UI and is containerized using Docker for deployment on AWS EC2.

## 3. Main User Roles

| Role          | Responsibilities                                                                      |
| ------------- | ------------------------------------------------------------------------------------- |
| **Admin**     | Creates organizer accounts and manages platform-level activities.                     |
| **Organizer** | Creates championships, schedules races, and submits race results.                     |
| **Driver**    | Registers a driver profile, applies to join teams, and participates in championships. |

### Additional Role: Team Manager

A Team Manager is responsible for managing a racing team. The manager can review driver applications, accept or reject applications, and register their team for championships.

## 4. API Endpoints and Team Contributions

The project contains 18 API endpoints: 3 authentication endpoints and 15 application endpoints.

### Authentication APIs

| ID | Method | Endpoint         | Functionality                         | Responsible Member |
| -- | ------ | ---------------- | ------------------------------------- | ------------------ |
| A1 | POST   | `/auth/register` | Register a user                       | Tanuja             |
| A2 | POST   | `/auth/login`    | Authenticate user and generate tokens | Sanghavi           |
| A3 | POST   | `/auth/refresh`  | Generate a new access token           | Ayushman           |

### Application APIs

| ID  | Method | Endpoint                                     | Functionality                   | Responsible Member |
| --- | ------ | -------------------------------------------- | ------------------------------- | ------------------ |
| E1  | POST   | `/admin/organizers`                          | Create organizer                | Tanuja             |
| E2  | POST   | `/teams`                                     | Create racing team              | Tanuja             |
| E3  | GET    | `/teams`                                     | Retrieve all teams              | Tanuja             |
| E4  | GET    | `/teams/{team_id}`                           | Retrieve team details           | Tanuja             |
| E5  | POST   | `/championships`                             | Create championship             | Sanghavi           |
| E6  | GET    | `/championships`                             | Retrieve all championships      | Sanghavi           |
| E7  | POST   | `/drivers`                                   | Register driver profile         | Sanghavi           |
| E8  | POST   | `/teams/{team_id}/apply`                     | Apply to join a team            | Ayushman           |
| E9  | PUT    | `/applications/{application_id}`             | Accept or reject application    | Ayushman           |
| E10 | POST   | `/championships/{championship_id}/teams`     | Register team for championship  | Tanuja             |
| E11 | POST   | `/championships/{championship_id}/races`     | Schedule a race                 | Sanghavi           |
| E12 | GET    | `/championships/{championship_id}/races`     | Retrieve championship races     | Sanghavi           |
| E13 | POST   | `/races/{race_id}/results`                   | Submit race results             | Ayushman           |
| E14 | GET    | `/championships/{championship_id}/standings` | Retrieve championship standings | Ayushman           |
| E15 | GET    | `/drivers/{username}/performance`            | Retrieve driver performance     | Ayushman           |

## 5. Championship Scoring System

The application awards points based on each driver's finishing position.

| Position | Points |
| -------- | -----: |
| 1st      |     25 |
| 2nd      |     18 |
| 3rd      |     15 |
| 4th      |     12 |
| 5th      |     10 |
| 6th      |      8 |
| 7th      |      6 |
| 8th      |      4 |
| 9th      |      2 |
| 10th     |      1 |

The points earned by drivers are used to calculate championship standings.

## 6. Technology Stack

| Area              | Technologies               |
| ----------------- | -------------------------- |
| Backend           | Python, FastAPI            |
| Frontend          | React, JavaScript          |
| Database          | SQLite, SQLAlchemy         |
| Authentication    | JWT, Argon2                |
| API Documentation | Swagger UI                 |
| Containerization  | Docker                     |
| Cloud Deployment  | AWS EC2                    |
| CI/CD             | GitHub Actions, Docker Hub |

## 7. Project Structure

```text
f1-championship-manager/
│
├── backend/
│   ├── main.py
│   ├── functions.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── f1_championship.db
│
├── frontend/
│   ├── src/
│   └── package.json
│
├── .github/
│   └── workflows/
│       └── deploy.yml
│
└── README.md
```

## 8. Setup and Installation

### Backend Setup

```bash
cd backend
python -m venv .venv
```

Activate the environment and install dependencies:

```bash
# Windows
.venv\Scripts\activate

pip install -r requirements.txt
```

Start the backend:

```bash
uvicorn main:app --reload
```

Local API: `http://127.0.0.1:8000`

Swagger documentation: `http://127.0.0.1:8000/docs`

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Open the local URL displayed in the terminal.

## 9. Docker and AWS EC2 Deployment

The backend is containerized using Docker and deployed on an AWS EC2 instance.

The deployment uses Docker Hub to obtain the application image and a volume mount to preserve the SQLite database outside the container.

```bash
# Create persistent database file
touch /home/ec2-user/f1_championship.db

# Run application container
docker run -d --name f1-app --restart unless-stopped \
-p 8001:8001 \
-v /home/ec2-user/f1_championship.db:/app/f1_championship.db \
gthanuja/f1-championship

# Check running container
docker ps
```

**EC2 API Documentation:** `http://54.91.102.153:8001/docs`

*The EC2 address depends on the instance remaining active and retaining the same public IP.*

## 10. CI/CD Pipeline

GitHub Actions is used for automating the deployment workflow.

The intended pipeline includes:

1. Code changes are pushed to GitHub.
2. GitHub Actions triggers the deployment workflow.
3. The Docker image is built.
4. The image is pushed to Docker Hub.
5. The updated image is deployed to the EC2 instance.
6. The application container is restarted with the latest version.

GitHub Secrets are used to store deployment credentials securely.

### API Error Status Codes

The API also uses HTTP status codes to communicate request outcomes.

| Status Code | Meaning                                           |
| ----------- | ------------------------------------------------- |
| 400         | Bad Request                                       |
| 401         | Unauthorized – invalid or expired token           |
| 403         | Forbidden – insufficient permissions              |
| 404         | Resource Not Found                                |
| 409         | Conflict – duplicate or already-existing resource |
| 422         | Unprocessable Entity – request validation error   |

## 13. Conclusion

F1 Championship Manager brings drivers, teams, organizers, and championships together in one centralized application.

From driver registration to championship standings, the system simplifies the management of racing activities while demonstrating practical implementation of backend development, frontend integration, database management, authentication, Docker, and cloud deployment.

**Less paperwork. Fewer arguments. More racing! 🏁**


