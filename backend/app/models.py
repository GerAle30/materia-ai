"""
models.py - Database table definitions.

Each class here is a SQLALchemy model: it maps directly to a table in the database. An instance of Ingredient is a row in the ingredients table, and so on.
"""

from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.database import Base

class Ingredient(Base):
    """A stock item the kitchen tracks - e.g. shrimp, green plantain."""

    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    quantity = Column(Float, default=0.0, nullable=False)
    unit = Column(String, nullable=False) # "kg", "units", "liters"
    minimum_threshold = Column(Float, default=0.0)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # One ingredinets can have any recorded movements (purchase, uses).
    movements = relationship("InventoryMovement", back_populates="ingredient")

    class InventoryMovement(Base):
        """A single change in stock - a purchase, a use in the kitchen , waste."""

        __tablename__ = "inventory_movements"

        id = Column(Integer, primary_key=True, index=True)
        ingredient_id = Column(Integer, ForeignKey("ingredients.id"), nullable=False)
        change = Column(Float, nullable=False) # positive = in, negative = out
        reason = Column(String, nullable=False) # "purchase", "kitchen use", "waste"
        created_at = Column(DateTime, default=datetime.utcnow)

        ingredient = relationship("Ingredient", back_populates="movements")

class Dish(Base):
    """A menu item the restaurant sells."""

    __tablename__ = "dishes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description_es = Column(String, nullable=True)
    description_en = Column(String, nullable=True)
    price = Column(Float, nullable=True)
    is_active = Column(Boolean, default=True)

    # Which ingredients (and how much of each) this dish requires.
    ingredients = relationship("DishIngredient", back_populates="dish")


class DishIngredient(Base):
    """The recipe link: how much of one ingredient a dish requires."""

    __tablename__ = "dish_ingredients"

    id = Column(Integer, primary_key=True, index=True)
    dish_id = Column(Integer, ForeignKey("dishes.id"), nullable=False)
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"), nullable=False)
    quantity_used = Column(Float, nullable=False)  # per single serving

    dish = relationship("Dish", back_populates="ingredients")
    ingredient = relationship("Ingredient")


class MenuGenerationLog(Base):
    """A permanent record of every AI-generated description.

    Lets us reuse a previous generation instead of calling the AI
    again for the same dish, and gives the restaurant a full history
    of what's been generated and when.
    """

    __tablename__ = "menu_generation_logs"

    id = Column(Integer, primary_key=True, index=True)
    dish_name = Column(String, index=True, nullable=False)
    description_es = Column(String, nullable=False)
    description_en = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
