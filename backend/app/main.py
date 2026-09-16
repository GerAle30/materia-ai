"""
main.py - Application entry point for materia-AI.

Creates the FastAPI app, wires in the menu router, and exposes
a simple health-check route. Run with:

    uvicorn app.main:app --reload
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import menu, inventory

# Create the FastAPI application instance.
app = FastAPI(
    title="materia-AI",
    description="Bilingual AI-powered menu description generator.",
    version="0.1.0",
)

# Allow the frontend (running on a different port) to call this API.
# During development we allow all origins; tighten this in production.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Plug in the menu router — this activates /menu/generate.
app.include_router(menu.router)
app.include_router(inventory.router)


@app.get("/")
def health_check() -> dict:
    """A simple route to confirm the API is alive."""
    return {"status": "ok", "service": "materia-AI"}
