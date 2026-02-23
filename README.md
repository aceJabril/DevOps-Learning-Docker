# CoderCo Docker Container Challenge

This project is a multi-container Docker application built to demonstrate how web services communicate with databases, persist data, and sit behind a reverse proxy in a DevOps-style setup.

The system uses **Flask** for the web application, **Redis** for persistent storage, **NGINX** as a reverse proxy, and **Docker Compose** for orchestration.

---

# Architecture Overview

The application consists of three core services:

- Flask Web Application  
- Redis Database  
- NGINX Reverse Proxy  

Traffic flows from the client to NGINX, which forwards requests to the Flask container. Flask stores and retrieves data from Redis using Docker’s internal network.

---

# Project Structure

```
coderco-challenge/
├── flask/
│   ├── app.py
│   └── Dockerfile
├── nginx/
│   └── nginx.conf
├── redis/
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

---

# Features

- Multi-container orchestration using Docker Compose  
- Internal container networking  
- Persistent Redis storage with Docker volumes  
- Reverse proxy routing using NGINX  
- Environment variable-based configuration  
- Real-world service isolation and communication  

---

# Application Behaviour

## Flask Web Application

The Flask application exposes two routes:

- `/` – Displays a simple welcome message  
- `/count` – Increments and displays a visit count stored in Redis  

Each time `/count` is refreshed, Redis updates the counter:

```python
visits = redis_client.incr("visits")
```

---

## Redis Persistence

Redis runs in its own container and acts as a persistent key-value store for the visit counter.

It uses a Docker volume, so:

- The counter does not reset if the container restarts  
- Data persists across application shutdowns  

---

## Environment Variables

The Flask application uses environment variables instead of hardcoding infrastructure values:

- `REDIS_HOST`
- `REDIS_PORT`
- `REDIS_DB`

These are injected via `docker-compose.yml`, keeping the application portable and production-ready.

---

## NGINX Reverse Proxy

NGINX sits in front of the Flask application and:

- Listens externally on port `5002`  
- Forwards requests to the Flask container internally  
- Decouples client traffic from the application  

This mirrors real-world traffic routing in production environments.

---

# Docker Setup

## Flask Dockerfile (Actual File Used)

```dockerfile
# Build stage
FROM python:3.13-alpine AS build

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.13-alpine

WORKDIR /app

COPY --from=build /usr/local/lib/python3.13/site-packages \
                  /usr/local/lib/python3.13/site-packages

COPY app.py .

RUN adduser -D appuser
USER appuser

CMD ["python", "app.py"]
```

---

## Redis Dockerfile

```dockerfile
FROM redis:latest
```

---

# Docker Compose Responsibilities

Docker Compose orchestrates multiple services:

- Builds the Flask and Redis images  
- Creates an internal Docker network  
- Provides persistent storage for Redis  
- Routes traffic through NGINX  
- Injects environment variables cleanly  

---

# How I Built This

1. Created Flask app – two routes `/` and `/count`  
2. Connected Flask to Redis using environment variables  
3. Containerized Flask using a multi-stage Dockerfile  
4. Set up Redis container with a volume for persistence  
5. Configured NGINX as a reverse proxy pointing to Flask  
6. Orchestrated all services using Docker Compose  

### Issues Resolved

- Initially, NGINX failed to start because `events {}` was in the wrong config file  
- Fixed by keeping only the `server {}` block in `conf.d/default.conf`  
- Tested connections to ensure the web page and visit counter worked correctly  

---

# How to Run Locally

From the root directory:

```bash
docker compose up --build
```

Then access the application:

- Welcome Page: http://localhost:5002/  
- Visit Counter: http://localhost:5002/count  

Each refresh of `/count` increments the Redis-backed counter.

---

# What This Project Demonstrates

- Multi-container application design  
- Internal Docker networking  
- Service isolation with controlled communication  
- Persistent state outside application memory  
- Reverse proxy traffic flow  
- Real-world Docker Compose orchestration  

---

# Future Improvements

- Add health checks for all services  
- Introduce logging and monitoring  
- Scale the Flask service horizontally  
- Deploy the application to a cloud environment  
