from sqlalchemy import text

from app.db.base import Base
from app.db.session import engine


def test_database_metadata_is_configured() -> None:
    assert Base.metadata is not None
    assert len(Base.metadata.tables) >= 2


def test_database_engine_is_available() -> None:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        assert result.scalar() == 1
