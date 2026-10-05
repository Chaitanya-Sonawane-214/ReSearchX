from database.base import Base
from database.connection import engine

# Import models so SQLAlchemy knows about them
from models.reviewer import Reviewer

print("Creating database tables...")

Base.metadata.create_all(bind=engine)

print("Database tables created successfully!")