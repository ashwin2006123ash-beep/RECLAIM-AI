"""
Pytest configuration and fixtures for RECLAIM AI
"""
import pytest
import os
import tempfile
from app import create_app
from database.db import init_db
from config import Config

@pytest.fixture
def app():
    # Use temporary database for test isolation
    temp_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    temp_db.close()
    Config.DATABASE_PATH = temp_db.name
    
    app_instance = create_app()
    app_instance.config.update({
        "TESTING": True,
    })
    
    yield app_instance
    
    # Cleanup temp db
    try:
        os.remove(temp_db.name)
    except Exception:
        pass

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()
