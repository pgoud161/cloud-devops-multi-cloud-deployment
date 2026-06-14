"""
FastAPI Application - Cloud DevOps Multi-Cloud Deployment
Author: Parnika Goud Bingi
Description: A sample FastAPI microservice demonstrating containerized deployment
             across AWS EKS and Azure AKS with full CI/CD pipeline.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Cloud DevOps Multi-Cloud API",
    description="FastAPI microservice deployed via CI/CD to AWS EKS and Azure AKS",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Models ────────────────────────────────────────────────────────────────────

class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    in_stock: bool = True


class HealthResponse(BaseModel):
    status: str
    environment: str
    version: str
    uptime_seconds: float


class ItemResponse(BaseModel):
    message: str
    item: Item


# ── In-memory store (demo purposes) ──────────────────────────────────────────

START_TIME = time.time()

ITEMS_DB: dict[int, Item] = {
    1: Item(id=1, name="Widget Alpha",  description="A high-quality widget",  price=9.99,  in_stock=True),
    2: Item(id=2, name="Gadget Beta",   description="A premium gadget",        price=49.99, in_stock=True),
    3: Item(id=3, name="Doohickey Gamma", description="An essential doohickey", price=19.99, in_stock=False),
}

# ── Routes ────────────────────────────────────────────────────────────────────

@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """
    Health check endpoint used by Kubernetes liveness and readiness probes.
    Returns service status, environment, version, and uptime.
    """
    return HealthResponse(
        status="healthy",
        environment=os.getenv("ENVIRONMENT", "development"),
        version="1.0.0",
        uptime_seconds=round(time.time() - START_TIME, 2),
    )


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with service information."""
    return {
        "service": "Cloud DevOps Multi-Cloud API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
        "endpoints": ["/items", "/items/{item_id}"],
    }


@app.get("/items", tags=["Items"])
async def list_items():
    """Retrieve all available items."""
    logger.info("Fetching all items")
    return {
        "count": len(ITEMS_DB),
        "items": list(ITEMS_DB.values()),
    }


@app.get("/items/{item_id}", response_model=ItemResponse, tags=["Items"])
async def get_item(item_id: int):
    """
    Retrieve a specific item by ID.
    Returns 404 if the item does not exist.
    """
    logger.info(f"Fetching item with id={item_id}")
    if item_id not in ITEMS_DB:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
    return ItemResponse(message="Item retrieved successfully", item=ITEMS_DB[item_id])


@app.post("/items", response_model=ItemResponse, status_code=201, tags=["Items"])
async def create_item(item: Item):
    """Create a new item."""
    if item.id in ITEMS_DB:
        raise HTTPException(status_code=400, detail=f"Item {item.id} already exists")
    ITEMS_DB[item.id] = item
    logger.info(f"Created item with id={item.id}")
    return ItemResponse(message="Item created successfully", item=item)


@app.delete("/items/{item_id}", tags=["Items"])
async def delete_item(item_id: int):
    """Delete an item by ID."""
    if item_id not in ITEMS_DB:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
    del ITEMS_DB[item_id]
    logger.info(f"Deleted item with id={item_id}")
    return {"message": f"Item {item_id} deleted successfully"}
