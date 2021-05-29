# TODO complete writing tests, probably won't finish since I'm not paid enough for this industry-standard crap
import pytest
import uuid
import os
from initialize_database import initialize_temp_database
from main import app

@pytest.fixture
def client():
    temp_db = initialize_temp_database()
    print(temp_db.name)

    with app.test_client() as client:
        yield client

    os.close(temp_db)

def test_dummy(client):
    assert True