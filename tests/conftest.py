import pytest
from app import app
from src.models import db, Users, Rating

@pytest.fixture(scope='module')
def test_client():
    with app.app_context():

        Rating.query.delete()
        db.session.commit()
        # Add a test user
        test_user = Users(username='testuser', email='test@example.com', first_name='John', last_name='Doe', password='testpassword')
        db.session.add(test_user)
        db.session.commit()
        yield app.test_client()