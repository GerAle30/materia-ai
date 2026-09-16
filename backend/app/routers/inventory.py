"""
inventory.py - API routes for ingredient and stock management.

Defines the endpoints clients call to register ingredients and check
current stock levels. Keeps routing separate from the database
session handling and the models themselves.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Ingredient
from app.schemas import IngredientCreate, IngredientResponse

router = APIRouter(prefix="/inventory", tags=["inventory"])


@router.post("/ingredients", response_model=IngredientResponse)
def create_ingredient(
    ingredient: IngredientCreate,
    db: Session = Depends(get_db),
) -> Ingredient:
    """Registers a new ingredient in the inventory."""
    db_ingredient = Ingredient(
        name=ingredient.name,
        quantity=ingredient.quantity,
        unit=ingredient.unit,
        minimum_threshold=ingredient.minimum_threshold,
    )
    db.add(db_ingredient)
    db.commit()
    db.refresh(db_ingredient)
    return db_ingredient


@router.get("/ingredients", response_model=list[IngredientResponse])
def list_ingredients(db: Session = Depends(get_db)) -> list[Ingredient]:
    """Returns every ingredient currently tracked."""
    return db.query(Ingredient).all()
