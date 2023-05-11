import html
from src.models import db, Rating, Users, Comments, Rating_votes, Comment_votes
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()

def test_delete_rating(test_client):

    # Add test users
    temp_user1 = Users(username='testuser1', password='testpassword1', first_name='John1', last_name='Doe1', email='test1@example.com', commented_on=[])
    temp_user2 = Users(username='testuser2', password='testpassword2', first_name='John2', last_name='Doe2', email='test2@example.com', commented_on=[])
    db.session.add(temp_user1)
    db.session.add(temp_user2)

    # Add test rating
    temp_rating1 = Rating(rater_id=temp_user1.user_id, restroom_name="Testroom1", cleanliness=3.0, overall=3.5)
    temp_rating2 = Rating(rater_id=temp_user2.user_id, restroom_name="Testroom 2", cleanliness=2.0, overall=2.5)
    db.session.add(temp_rating1)
    db.session.add(temp_rating2)
    db.session.commit()

    # Get the rating's ID
    rating_id1 = temp_rating1.rating_id
    rating_id2 = temp_rating2.rating_id
    # Delete the test rating
    response = test_client.post(f'/restroom/{rating_id1}/delete')

    assert response.status_code == 302

    # Check that the rating was deleted from the database
    rating1 = Rating.query.get( rating_id1)
    assert rating1 is None
    # Check that the rating was not deleted from the database
    rating2 = Rating.query.get( rating_id2)
    assert rating2 is not None
    
    # Clear database
    Rating.query.delete()
    db.session.commit()

def test_login(test_client):

    # Creating a test user
    pass_data = bcrypt.generate_password_hash('testpassword')
    hash_password = pass_data.decode('utf-8')
    test_user = Users(username='testuser', password=hash_password,
                       first_name='John', last_name='Doe', email='test@example.com',
                       commented_on=None)
    db.session.add(test_user)
    db.session.commit()

    # Login with wrong password
    resp1 = test_client.post('/login', data={
        'username': 'testuser',
        'password': 'wrongpassword'
    }, follow_redirects=True)

    resp_data1 = resp1.data.decode('utf-8')

    assert "Incorrect username or password!" in resp_data1
    assert '<h1 class="d-flex justify-content-center fw-bold">Login</h1>' in resp_data1

    # Login with wrong user
    resp2 = test_client.post('/login', data={
        'username': 'wronguser',
        'password': 'testpassword'
        }, follow_redirects=True)

    resp_data2 = resp2.data.decode('utf-8')


    assert "Incorrect username or password!" in resp_data2
    assert '<h1 class="d-flex justify-content-center fw-bold">Login</h1>' in resp_data2

    # Successful login
    resp3 = test_client.post('/login', data={
        'username': 'testuser',
        'password': 'testpassword'
    }, follow_redirects=True)

    resp_data3 = resp3.data.decode('utf-8')
    #print(resp_data3)
    assert "Success! You are logged in." in resp_data3
    assert '<ul class="navbar-nav ms-auto mb-2 mb-lg-0">' in resp_data3

def test_logout(test_client):
    
    # Creating a test user
    pass_data = bcrypt.generate_password_hash('testpassword')
    hash_password = pass_data.decode('utf-8')
    test_user = Users(username='testuser', password=hash_password,
                       first_name='John', last_name='Doe', email='test@example.com',
                       commented_on=None)
    db.session.add(test_user)
    db.session.commit()

    # Login
    test_client.post('/login', data={
        'username': 'testuser',
        'password': 'testpassword'
    }, follow_redirects=True)

    # Logout
    resp1 = test_client.post('/logout', follow_redirects=True)
    resp_data = resp1.data.decode('utf-8')
    #Decode &#39;
    resp_data = html.unescape(resp_data)
    #print(resp_data)
    assert "You've been logged out!" in resp_data
    assert '<h1 class="d-flex justify-content-center fw-bold">Login</h1>' in resp_data

    # Clear database
    Users.query.delete()
    db.session.commit()