'''
run with at server root in commandline python -m pytest tests 
'''

import pytest

from main import app as flask_app  # or wherever your Flask app is created

@pytest.fixture
def app():
    yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()
