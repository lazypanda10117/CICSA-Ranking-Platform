import os
import pytest
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from app import create_app
from app.db import get_config_obj


@pytest.fixture(scope='session')
def app():
    app = create_app(__name__, get_config_obj())
    return app


@pytest.fixture(scope='session')
def _db(app):
    db = SQLAlchemy(app=app)
    return db
