"""
FastAPI Application - CI/CD Pipeline Demo
==========================================
A production-ready REST API demonstrating DevOps best practices,
including containerisation, automated testing, and CI/CD pipelines.

Author: Portfolio Project
License: MIT
"""

import os
import time
import platform
from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# ---------------------------------------------------------------------------
# App Initialisation
# ---------------------------------------------------------------------------

APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
APP_ENV = os.getenv("APP_ENV", "development")
START_TIME = time.time()

app = FastAPI(
    title="CI/CD Pipeline Demo API",
    description=(
        "A production-ready REST API showcasing modern DevOps practices: "
        "CI/CD with GitHub Actions, Docker containerisation, and automated testing."
    ),
    version=APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
)

# ---------------------------------------------------------------------------
# CORS Middleware
# ---------------------------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Response Models
# ---------------------------------------------------------------------------


class HealthResponse(BaseModel):
    status: str
    version: str
    environment: str
    uptime_seconds: float
    timestamp: str


class StatusResponse(BaseModel):
    api: str
    version: str
    environment: str
    python_version: str
    platform: str
    timestamp: str


class InfoResponse(BaseModel):
    name: str
    description: str
    version: str
    author: str
    repository: str
    technologies: list[str]


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------


@app.get(
    "/health",
    response_model=HealthResponse,
    summary="Health Check",
    tags=["Monitoring"],
)
def health_check() -> HealthResponse:
    """
    Returns the health status of the API.

    Used by load balancers, orchestrators (e.g. Kubernetes), and monitoring
    tools to verify the service is alive and ready to accept traffic.
    """
    return HealthResponse(
        status="healthy",
        version=APP_VERSION,
        environment=APP_ENV,
        uptime_seconds=round(time.time() - START_TIME, 2),
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


@app.get(
    "/status",
    response_model=StatusResponse,
    summary="System Status",
    tags=["Monitoring"],
)
def system_status() -> StatusResponse:
    """
    Returns detailed system and runtime information.

    Useful for debugging, environment verification, and
    confirming which version is deployed.
    """
    return StatusResponse(
        api="operational",
        version=APP_VERSION,
        environment=APP_ENV,
        python_version=platform.python_version(),
        platform=platform.system(),
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


@app.get(
    "/info",
    response_model=InfoResponse,
    summary="Project Information",
    tags=["General"],
)
def project_info() -> InfoResponse:
    """
    Returns metadata about this project.

    Demonstrates environment-driven configuration and clean API design.
    """
    return InfoResponse(
        name="CI/CD Pipeline Demo",
        description=(
            "A production-ready FastAPI application fully integrated with a "
            "GitHub Actions CI/CD pipeline, Docker containerisation, and pytest."
        ),
        version=APP_VERSION,
        author="Portfolio Project",
        repository="https://github.com/devcarlosfigueiredo/Cicd-pipeline",
        technologies=["Python", "FastAPI", "Docker", "GitHub Actions", "pytest"],
    )


@app.get(
    "/",
    summary="Root",
    tags=["General"],
    include_in_schema=False,
)
def root() -> dict:
    """Redirects to interactive API documentation."""
    return {
        "message": "Welcome to the CI/CD Pipeline Demo API",
        "docs": "/docs",
        "health": "/health",
        "status": "/status",
    }
