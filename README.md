<div align="center">

# 🚀 CI/CD Pipeline Demo

### Production-ready FastAPI application with fully automated DevOps pipeline

[![CI/CD Pipeline](https://github.com/devcarlosfigueiredo/Cicd-pipeline/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/devcarlosfigueiredo/Cicd-pipeline/actions/workflows/ci-cd.yml)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Containerised-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Pipeline Architecture](#-pipeline-architecture)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Local Development](#local-development)
  - [Docker](#docker)
- [Running Tests](#-running-tests)
- [API Reference](#-api-reference)
- [CI/CD Workflow](#-cicd-workflow)
- [Security Practices](#-security-practices)
- [Cloud Deployment](#-cloud-deployment)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Overview

This project demonstrates a **production-grade CI/CD pipeline** built with modern DevOps tooling. It showcases industry best practices for automating the entire software delivery lifecycle — from a developer's commit all the way through to a deployed container.

**What this project proves:**

| Skill | Implementation |
|---|---|
| CI/CD Automation | GitHub Actions with 4-stage pipeline |
| Containerisation | Multi-stage Docker build with non-root user |
| Automated Testing | pytest with coverage enforcement (≥ 80%) |
| Code Quality | black + flake8 enforced in pipeline |
| Security | Non-root container, secrets via env vars |
| Observability | Health check endpoints + Docker HEALTHCHECK |
| Reproducibility | Pinned dependencies, cached layers |

---

## 🏗 Pipeline Architecture

```
  Developer Push / Pull Request
           │
           ▼
  ┌─────────────────┐
  │  1. 🔍 Lint     │  black (formatting) + flake8 (style)
  └────────┬────────┘
           │ passes
           ▼
  ┌─────────────────┐
  │  2. 🧪 Test     │  pytest + coverage report (≥ 80%)
  └────────┬────────┘
           │ passes
           ▼
  ┌─────────────────┐    Only on push to
  │  3. 🐳 Build    │ ◄─ main / develop
  │  & Push Image   │
  └────────┬────────┘
           │ success
           ▼
  ┌─────────────────┐    Only on push to
  │  4. 🚀 Deploy   │ ◄─ main
  └─────────────────┘
```

**Key design decisions:**
- **Fail fast**: linting runs before tests to catch obvious issues cheaply
- **Branch strategy**: images are built on both `main` and `develop`; deploy only triggers from `main`
- **Layer caching**: GitHub Actions cache (GHA) is used for Docker layer caching, cutting build time significantly
- **Least privilege**: the container runs as a non-root system user

---

## 🛠 Tech Stack

| Layer | Technology | Version |
|---|---|---|
| Language | Python | 3.12 |
| Web Framework | FastAPI | 0.115 |
| ASGI Server | Uvicorn | 0.32 |
| Containerisation | Docker (multi-stage) | — |
| Orchestration (local) | Docker Compose | — |
| CI/CD | GitHub Actions | — |
| Testing | pytest + pytest-cov | 8.x |
| Code Quality | black + flake8 | — |
| Image Registry | GitHub Container Registry (GHCR) | — |

---

## 📁 Project Structure

```
devops-cicd-pipeline/
│
├── .github/
│   └── workflows/
│       └── ci-cd.yml          # GitHub Actions pipeline definition
│
├── src/
│   ├── __init__.py
│   └── main.py                # FastAPI application
│
├── tests/
│   ├── __init__.py
│   └── test_main.py           # pytest test suite
│
├── Dockerfile                 # Multi-stage, optimised Docker build
├── docker-compose.yml         # Local development environment
├── requirements.txt           # Pinned Python dependencies
├── pyproject.toml             # pytest & coverage configuration
├── .env.example               # Environment variable template
├── .dockerignore              # Reduces Docker build context
├── .gitignore
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

| Tool | Minimum Version | Install |
|---|---|---|
| Git | 2.x | [git-scm.com](https://git-scm.com/) |
| Python | 3.12 | [python.org](https://www.python.org/) |
| Docker | 24.x | [docs.docker.com](https://docs.docker.com/get-docker/) |
| Docker Compose | v2 | bundled with Docker Desktop |

---

### Local Development

```bash
# 1. Clone the repository
git clone https://github.com/devcarlosfigueiredo/Cicd-pipeline.git
cd devops-cicd-pipeline

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # Linux / macOS
# .venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Copy the environment template
cp .env.example .env

# 5. Start the development server
uvicorn src.main:app --reload --port 8000
```

The API will be available at:
- **Application**: http://localhost:8000
- **Interactive Docs (Swagger)**: http://localhost:8000/docs
- **Alternative Docs (ReDoc)**: http://localhost:8000/redoc

---

### Docker

#### Build and run manually

```bash
# Build the image
docker build -t cicd-pipeline-demo:latest .

# Run the container
docker run -d \
  --name cicd-demo \
  -p 8000:8000 \
  -e APP_ENV=production \
  cicd-pipeline-demo:latest

# Check container health
docker ps
docker logs cicd-demo
```

#### Using Docker Compose (recommended for local development)

```bash
# Start the stack
docker compose up --build

# Start in detached mode
docker compose up -d --build

# View logs
docker compose logs -f

# Stop and remove containers
docker compose down
```

---

## 🧪 Running Tests

```bash
# Run all tests with verbose output
pytest tests/ -v

# Run tests with coverage report
pytest tests/ -v --cov=src --cov-report=term-missing

# Generate an HTML coverage report
pytest tests/ --cov=src --cov-report=html
open htmlcov/index.html

# Run a specific test class
pytest tests/test_main.py::TestHealthEndpoint -v
```

> ℹ️ The pipeline enforces a minimum coverage of **80%**. The build fails if this threshold is not met.

---

## 📡 API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Welcome message and links |
| `GET` | `/health` | Health check (used by load balancers) |
| `GET` | `/status` | Runtime and system information |
| `GET` | `/info` | Project metadata |
| `GET` | `/docs` | Interactive Swagger UI |
| `GET` | `/redoc` | ReDoc documentation |

### Example responses

<details>
<summary><code>GET /health</code></summary>

```json
{
  "status": "healthy",
  "version": "1.0.0",
  "environment": "production",
  "uptime_seconds": 42.17,
  "timestamp": "2024-11-01T10:30:00+00:00"
}
```
</details>

<details>
<summary><code>GET /status</code></summary>

```json
{
  "api": "operational",
  "version": "1.0.0",
  "environment": "production",
  "python_version": "3.12.0",
  "platform": "Linux",
  "timestamp": "2024-11-01T10:30:00+00:00"
}
```
</details>

---

## ⚙️ CI/CD Workflow

The pipeline is defined in [`.github/workflows/ci-cd.yml`](.github/workflows/ci-cd.yml) and runs on every push and pull request.

### Stages

| Stage | Trigger | Description |
|---|---|---|
| **Lint** | All pushes & PRs | Checks code formatting (black) and style (flake8) |
| **Test** | After lint passes | Runs pytest; uploads coverage artifact |
| **Build** | After tests; push only | Builds Docker image; pushes to GHCR with SHA + branch tags |
| **Deploy** | After build; `main` only | Runs deployment script (simulated; replace with real cloud deploy) |

### Image tagging strategy

| Event | Tags applied |
|---|---|
| Push to `main` | `latest`, `sha-<short-sha>`, `main` |
| Push to `develop` | `develop`, `sha-<short-sha>` |

### Secrets required

| Secret | Description |
|---|---|
| `GITHUB_TOKEN` | Automatically provided by GitHub Actions (no setup required) |

> For real cloud deploys, add `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, or equivalent secrets in **Settings → Secrets → Actions**.

---

## 🔐 Security Practices

- **Non-root container**: the application runs as a dedicated system user (`appuser`), never as root
- **Multi-stage build**: build tools and source files are not present in the final image
- **No secrets in code**: all configuration is injected via environment variables
- **`.env` excluded from git**: the `.gitignore` and `.dockerignore` both exclude environment files
- **Pinned dependencies**: exact versions in `requirements.txt` prevent supply-chain surprises
- **GITHUB_TOKEN scoped permissions**: the workflow only requests `read` on `contents` and `write` on `packages`

---

## ☁️ Cloud Deployment

This project is cloud-agnostic. Below are example deployment targets with estimated costs:

### AWS — Elastic Container Service (ECS Fargate)

```bash
# Push image to Amazon ECR
aws ecr get-login-password --region eu-west-1 | \
  docker login --username AWS --password-stdin <account-id>.dkr.ecr.eu-west-1.amazonaws.com

docker tag cicd-pipeline-demo:latest <ecr-uri>:latest
docker push <ecr-uri>:latest

# Update ECS service
aws ecs update-service \
  --cluster my-cluster \
  --service my-service \
  --force-new-deployment
```

| Resource | Estimated Cost |
|---|---|
| ECS Fargate (0.25 vCPU / 0.5 GB) | ~$8–12 / month |
| ECR image storage | ~$0.10 / GB / month |
| ALB (optional) | ~$16 / month |

### Azure — Container Apps

```bash
az containerapp update \
  --name my-app \
  --resource-group my-rg \
  --image ghcr.io/devcarlosfigueiredo/Cicd-pipeline:latest
```

> 💡 For a zero-cost demo, the deploy step can simply run the container locally or on a free-tier VM.

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/your-feature`
3. Commit your changes: `git commit -m 'feat: add your feature'`
4. Push to the branch: `git push origin feat/your-feature`
5. Open a Pull Request against `main`

Please ensure all tests pass and coverage does not drop below 80% before submitting.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

<div align="center">

Made with ❤️ as a DevOps portfolio project

</div>
