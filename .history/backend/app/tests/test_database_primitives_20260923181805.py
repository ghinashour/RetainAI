import socket

import pytest
from sqlalchemy import text

import app.db.domain  # noqa: F401
from app.db.base import Base
from app.db.session import engine


def _postgres_available() -> bool:
    try:
        with socket.create_connection(("localhost", 5432), timeout=0.5):
            return True
    except OSError:
        return False


def test_database_metadata_is_configured() -> None:
    assert Base.metadata is not None
    assert len(Base.metadata.tables) >= 2


@pytest.mark.skipif(
    not _postgres_available(),
    reason="Local PostgreSQL is not running in this environment. Docker is unavailable here.",
)
def test_database_engine_is_available() -> None:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        assert result.scalar() == 1
