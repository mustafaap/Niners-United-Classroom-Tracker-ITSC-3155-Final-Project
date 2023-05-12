import pytest
from app import app, bcrypt
from src.models import db, Users, Rating

@pytest.fixture(scope='module')
def test_client():
    with app.app_context():

        Rating.query.delete()
        db.session.commit()
        yield app.test_client()

@pytest.fixture(scope='module')
def test_login(test_client):
    pass_data = bcrypt.generate_password_hash('testpassword')
    hash_password = pass_data.decode('utf-8')
    test_user = Users(username='testuser', 
                      password=hash_password, 
                      first_name='John', 
                      last_name='Doe', 
                      email='test@example.com', 
                      commented_on=None, 
                      rupvoted_on=None, 
                      rdownvoted_on=None, 
                      cupvoted_on=None, 
                      cdownvoted_on=None)
    db.session.add(test_user)
    db.session.commit()

    return test_client.post('/login', data={
        'username': 'testuser',
        'password': 'testpassword'
    }, follow_redirects=True)