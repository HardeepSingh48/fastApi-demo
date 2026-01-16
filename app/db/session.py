from sqlmodel import Session
from app.db.engine import engine
from typing import Generator


def get_session() -> Generator[Session, None, None]:
    """
    Database session dependency.
    
    Yields:
        Session: SQLModel session for database operations
    """
    with Session(engine) as session: 
        yield session