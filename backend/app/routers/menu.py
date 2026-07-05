"""
menu.py - API routes for menu description generation.

Defines the endpoints (doors) that clients call to turn a dish
into bilingual menu descriptions. Keeps routing separate from
the AI logic and the app startup.
"""

from fastapi import APIRouter, HTTPException

from app.schemas import MenuItemRequest, MenuDescriptionResponse
from app.services.ai_service import generate_description

# A router groups related endpoints. main.py will plug this in.
router = APIRouter(prefix="/menu", tags=["menu"])


@router.post("/generate", response_model=MenuDescriptionResponse)
def generate_menu_description(item: MenuItemRequest) -> MenuDescriptionResponse:
    """Takes a dish and returns bilingual menu descriptions.

    FastAPI validates the incoming request against MenuItemRequest
    automatically. If the AI call fails, we return a clean 500 error
    instead of leaking a raw traceback to the client.
    """
    try:
        return generate_description(item)
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate description: {error}",
        )
