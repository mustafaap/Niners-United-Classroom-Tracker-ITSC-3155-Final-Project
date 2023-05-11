import pytest
from app import app
from src.models import db, Users, Rating

@pytest.fixture(scope='module')
def test_client():
    with app.app_context():

        Rating.query.delete()
        db.session.commit()
        yield app.test_client()