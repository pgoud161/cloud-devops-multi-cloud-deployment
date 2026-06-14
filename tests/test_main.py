"""
Unit Tests - Cloud DevOps Multi-Cloud Deployment API
Tests cover health check, items CRUD, and error handling.
"""

import pytest
from fastapi.testclient import TestClient
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.main import app, ITEMS_DB, Item

client = TestClient(app)


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture(autouse=True)
def reset_db():
    """Reset in-memory DB to known state before each test."""
    ITEMS_DB.clear()
    ITEMS_DB.update({
        1: Item(id=1, name="Widget Alpha",    description="A high-quality widget", price=9.99,  in_stock=True),
        2: Item(id=2, name="Gadget Beta",     description="A premium gadget",      price=49.99, in_stock=True),
        3: Item(id=3, name="Doohickey Gamma", description="An essential doohickey", price=19.99, in_stock=False),
    })
    yield


# ── Health Check ──────────────────────────────────────────────────────────────

class TestHealthCheck:
    def test_health_returns_200(self):
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_returns_healthy_status(self):
        response = client.get("/health")
        data = response.json()
        assert data["status"] == "healthy"

    def test_health_contains_required_fields(self):
        response = client.get("/health")
        data = response.json()
        assert "status" in data
        assert "environment" in data
        assert "version" in data
        assert "uptime_seconds" in data

    def test_health_version_is_correct(self):
        response = client.get("/health")
        assert response.json()["version"] == "1.0.0"

    def test_health_uptime_is_non_negative(self):
        response = client.get("/health")
        assert response.json()["uptime_seconds"] >= 0


# ── Root ──────────────────────────────────────────────────────────────────────

class TestRoot:
    def test_root_returns_200(self):
        response = client.get("/")
        assert response.status_code == 200

    def test_root_contains_service_info(self):
        data = client.get("/").json()
        assert "service" in data
        assert "version" in data
        assert "docs" in data


# ── List Items ────────────────────────────────────────────────────────────────

class TestListItems:
    def test_list_items_returns_200(self):
        response = client.get("/items")
        assert response.status_code == 200

    def test_list_items_returns_correct_count(self):
        data = client.get("/items").json()
        assert data["count"] == 3

    def test_list_items_returns_items_array(self):
        data = client.get("/items").json()
        assert isinstance(data["items"], list)
        assert len(data["items"]) == 3


# ── Get Item ──────────────────────────────────────────────────────────────────

class TestGetItem:
    def test_get_existing_item_returns_200(self):
        response = client.get("/items/1")
        assert response.status_code == 200

    def test_get_item_returns_correct_data(self):
        data = client.get("/items/1").json()
        assert data["item"]["id"] == 1
        assert data["item"]["name"] == "Widget Alpha"
        assert data["item"]["price"] == 9.99

    def test_get_nonexistent_item_returns_404(self):
        response = client.get("/items/999")
        assert response.status_code == 404

    def test_get_item_404_contains_detail(self):
        data = client.get("/items/999").json()
        assert "detail" in data


# ── Create Item ───────────────────────────────────────────────────────────────

class TestCreateItem:
    def test_create_new_item_returns_201(self):
        payload = {"id": 10, "name": "New Item", "description": "Test item", "price": 5.00, "in_stock": True}
        response = client.post("/items", json=payload)
        assert response.status_code == 201

    def test_create_item_persists_in_list(self):
        payload = {"id": 10, "name": "New Item", "description": "Test item", "price": 5.00, "in_stock": True}
        client.post("/items", json=payload)
        data = client.get("/items").json()
        assert data["count"] == 4

    def test_create_duplicate_item_returns_400(self):
        payload = {"id": 1, "name": "Duplicate", "description": "Dupe", "price": 1.00, "in_stock": True}
        response = client.post("/items", json=payload)
        assert response.status_code == 400

    def test_create_item_returns_item_data(self):
        payload = {"id": 10, "name": "New Item", "description": "Test", "price": 5.00, "in_stock": True}
        data = client.post("/items", json=payload).json()
        assert data["item"]["name"] == "New Item"
        assert data["message"] == "Item created successfully"


# ── Delete Item ───────────────────────────────────────────────────────────────

class TestDeleteItem:
    def test_delete_existing_item_returns_200(self):
        response = client.delete("/items/1")
        assert response.status_code == 200

    def test_delete_item_removes_from_list(self):
        client.delete("/items/1")
        data = client.get("/items").json()
        assert data["count"] == 2

    def test_delete_nonexistent_item_returns_404(self):
        response = client.delete("/items/999")
        assert response.status_code == 404
