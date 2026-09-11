"""
database.py - Database connection setup.

Configures SQLAlchemy to talk to a local SQLite file. This gives us a real, persistent database with zero serversetup - perfect for development, and easy to swap for PostgreSQL later without touching the models themselves.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# The database lives as a single file inside backend/. SQLite needs
#this special connect_args because, by default, it only allows the 
# thread that created a connection to use it - FastAPI serves each
# request potentially on a different thread.
DATABASE_URL = "sqlite:///./materia.db"

engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        )

#EAch request gets its own SessionLocal instance - a temporary
#"conversation" with the database that opens and closes per request.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# All our model classes (Ingredient, Dish, etc.) will inherit from
# this Base, which is how SQLAlchemy knows they represent tables.
Base = declarative_base()

def get_db():
    """Dependency that provides a database session to route handlers.
    FastAPI calls this before each request, injects the session into 
    the route function, and this generator makes sure the session
    always close afterward - even if the request raises an error.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

