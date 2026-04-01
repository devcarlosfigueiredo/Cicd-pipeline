"""
Test Suite - CI/CD Pipeline Demo API
======================================
Comprehensive tests for all API endpoints.

Run with:
    pytest tests/ -v --cov=src --cov-report=term-missing
"""

import pytest
from fastapi.testclient import TestClient

from src.main import app

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def client() -> TestClient:
    """Provide a reusable TestClient for all tests in this module."""
    return TestClient(app)


# ---------------------------------------------------------------------------
# Root
# ---------------------------------------------------------------------------


class TestRoot:
    def test_root_returns_200(self, client: TestClient) -> None:
        response = client.get("/")
        assert response.status_code == 200

    def test_root_contains_docs_link(self, client: TestClient) -> None:
        data = response = client.get("/")
        data = response.json()
        assert "docs" in data
        assert data["docs"] == "/docs"

    def test_root_contains_health_link(self, client: TestClient) -> None:
        data = client.get("/").json()
        assert "health" in data


# ---------------------------------------------------------------------------
# Health Check
# ---------------------------------------------------------------------------


class TestHealthEndpoint:
    def test_health_returns_200(self, client: TestClient) -> None:
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_status_is_healthy(self, client: TestClient) -> None:
        data = client.get("/health").json()
        assert data["status"] == "healthy"

    def test_health_contains_version(self, client: TestClient) -> None:
        data = client.get("/health").json()
        assert "version" in data
        assert isinstance(data["version"], str)

    def test_health_contains_environment(self, client: TestClient) -> None:
        data = client.get("/health").json()
        assert "environment" in data

    def test_health_contains_uptime(self, client: TestClient) -> None:
        data = client.get("/health").json()
        assert "uptime_seconds" in data
        assert data["uptime_seconds"] >= 0

    def test_health_contains_timestamp(self, client: TestClient) -> None:
        data = client.get("/health").json()
        assert "timestamp" in data
        # Timestamp must be a non-empty string
        assert len(data["timestamp"]) > 0

    def test_health_response_schema(self, client: TestClient) -> None:
        """Validate all expected keys are present in the response."""
        data = client.get("/health").json()
        required_keys = {"status", "version", "environment", "uptime_seconds", "timestamp"}
        assert required_keys.issubset(data.keys())


# ---------------------------------------------------------------------------
# System Status
# ---------------------------------------------------------------------------


class TestStatusEndpoint:
    def test_status_returns_200(self, client: TestClient) -> None:
        response = client.get("/status")
        assert response.status_code == 200

    def test_status_api_is_operational(self, client: TestClient) -> None:
        data = client.get("/status").json()
        assert data["api"] == "operational"

    def test_status_contains_python_version(self, client: TestClient) -> None:
        data = client.get("/status").json()
        assert "python_version" in data
        assert data["python_version"].startswith("3.")

    def test_status_contains_platform(self, client: TestClient) -> None:
        data = client.get("/status").json()
        assert "platform" in data
        assert isinstance(data["platform"], str)

    def test_status_response_schema(self, client: TestClient) -> None:
        data = client.get("/status").json()
        required_keys = {"api", "version", "environment", "python_version", "platform", "timestamp"}
        assert required_keys.issubset(data.keys())


# ---------------------------------------------------------------------------
# Project Info
# ---------------------------------------------------------------------------


class TestInfoEndpoint:
    def test_info_returns_200(self, client: TestClient) -> None:
        response = client.get("/info")
        assert response.status_code == 200

    def test_info_contains_technologies(self, client: TestClient) -> None:
        data = client.get("/info").json()
        assert "technologies" in data
        assert isinstance(data["technologies"], list)
        assert len(data["technologies"]) > 0

    def test_info_technologies_include_python(self, client: TestClient) -> None:
        data = client.get("/info").json()
        assert "Python" in data["technologies"]

    def test_info_contains_name(self, client: TestClient) -> None:
        data = client.get("/info").json()
        assert "name" in data
        assert len(data["name"]) > 0

    def test_info_response_schema(self, client: TestClient) -> None:
        data = client.get("/info").json()
        required_keys = {"name", "description", "version", "author", "repository", "technologies"}
        assert required_keys.issubset(data.keys())


# ---------------------------------------------------------------------------
# Non-existent routes
# ---------------------------------------------------------------------------


class TestNotFound:
    def test_unknown_route_returns_404(self, client: TestClient) -> None:
        response = client.get("/this-route-does-not-exist")
        assert response.status_code == 404
