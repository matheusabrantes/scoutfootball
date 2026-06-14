from pathlib import Path

from app.core import config
from app.db import connection


def test_database_url_sqlite_relative_path(monkeypatch) -> None:
    monkeypatch.setenv("DATABASE_URL", "sqlite:///backend/data/test.db")
    config.get_settings.cache_clear()

    try:
        assert connection.database_path() == connection.project_root() / "backend/data/test.db"
    finally:
        config.get_settings.cache_clear()


def test_statsbomb_data_dir_can_be_configured(monkeypatch, tmp_path) -> None:
    from app.services.providers.statsbomb_open import StatsBombOpenDataProvider

    data_dir = tmp_path / "statsbomb"
    monkeypatch.setenv("STATSBOMB_DATA_DIR", str(data_dir))
    config.get_settings.cache_clear()

    try:
        provider = StatsBombOpenDataProvider()
        assert provider.data_dir == Path(data_dir)
    finally:
        config.get_settings.cache_clear()
