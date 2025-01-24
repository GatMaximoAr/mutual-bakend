from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.model import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./dev.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency


def get_db():
    """Intance of database."""

    try:
        with SessionLocal() as db:
            Base.metadata.create_all(bind=db.get_bind())
            yield db
    finally:
        db.close()
