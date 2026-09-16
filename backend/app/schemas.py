"""
schemas.py — Data shapes (request and response models).

Defines the exact structure of data entering and leaving the API.
Pydantic validates incoming requests automatically and powers
FastAPI's auto-generated interactive docs.
"""

from pydantic import BaseModel, Field


class MenuItemRequest(BaseModel):
    """The data a client sends to generate a menu description."""

    name: str = Field(
        ...,
        min_length=1,
        max_length=120,
        description="Name of the dish, e.g. 'Mofongo con camarones'.",
    )
    ingredients: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="Key ingredients or a short note about the dish.",
    )
    tone: str = Field(
        default="appetizing",
        max_length=50,
        description="Desired tone, e.g. 'elegant', 'casual', 'appetizing'.",
    )


class MenuDescriptionResponse(BaseModel):
    """The bilingual descriptions the API returns."""

    name: str = Field(..., description="Echoes the dish name back.")
    description_es: str = Field(..., description="Menu description in Spanish.")
    description_en: str = Field(..., description="Menu description in English.")


class IngredientCreate(BaseModel):
    """The data a client sends to register a new ingredient."""

    name: str = Field(
        ...,
        min_length=1,
        max_length=120,
        description="Ingredient name, e.g. 'Camarones'.",
    )
    quantity: float = Field(
        default=0.0,
        ge=0,
        description="Current quantity in stock.",
    )
    unit: str = Field(
        ...,
        max_length=20,
        description="Unit of measurement, e.g. 'kg', 'units', 'liters'.",
    )
    minimum_threshold: float = Field(
        default=0.0,
        ge=0,
        description="Alert level — when quantity falls below this, restock.",
    )


class IngredientResponse(BaseModel):
    """An ingredient as stored in the database."""

    id: int
    name: str
    quantity: float
    unit: str
    minimum_threshold: float

    class Config:
        from_attributes = True
