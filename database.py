from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import os

# read DATABASE_URL environment variable, with fallback
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password499@localhost/cicddemodb")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass
