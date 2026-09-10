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
    automatically. We distinguish two failure modes so clients (and
    our own logs) know what actually went wrong.
    """
    try:
        return generate_description(item)
    except ConnectionError as error:
        # The AI provider itself was unreachable — network, quota, auth.
        raise HTTPException(status_code=503, detail=str(error))
    except ValueError as error:
        # The AI responded, but not in the format we expected.
        raise HTTPException(status_code=502, detail=str(error))
