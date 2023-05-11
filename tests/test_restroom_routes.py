import html
from src.models import Rating, Users, Comments, Rating_votes, Comment_votes
from app import db
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()

def test_login(test_client):

    # Creating a test user
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

    # Login with wrong password
    resp1 = test_client.post('/login', data={
        'username': 'testuser',
        'password': 'wrongpassword'
    }, follow_redirects=True)

    resp_data1 = resp1.data.decode('utf-8')
    assert resp1.status_code == 200

    assert "Incorrect username or password!" in resp_data1
    assert '<h1 class="d-flex justify-content-center fw-bold">Login</h1>' in resp_data1

    # Login with wrong user
    resp2 = test_client.post('/login', data={
        'username': 'wronguser',
        'password': 'testpassword'
        }, follow_redirects=True)

    resp_data2 = resp2.data.decode('utf-8')
    assert resp2.status_code == 200

    assert "Incorrect username or password!" in resp_data2
    assert '<h1 class="d-flex justify-content-center fw-bold">Login</h1>' in resp_data2

    # Successful login
    resp3 = test_client.post('/login', data={
        'username': 'testuser',
        'password': 'testpassword'
    }, follow_redirects=True)

    resp_data3 = resp3.data.decode('utf-8')
    assert resp3.status_code == 200
    #print(resp_data3)
    assert 'Success! You are logged in.' in resp_data3
    assert '''<ul class="dropdown-menu dropdown-menu-dark dropdown-menu-end">
                <li><a class="dropdown-item" href="/profile">View your profile</a></li>
                <li><a class="dropdown-item" href="/profile/edit">Edit your profile</a></li>
                <li><a class="dropdown-item" href="/changePassword">Change your password</a></li>
                <hr class="my-2">
                <li>              
                  <!-- Button trigger modal -->
                  <button type="button" class="dropdown-item" data-bs-toggle="modal" data-bs-target="#logout">
                    <i class="fa-solid fa-right-from-bracket me-2" style="color: #ffffff;"></i>Logout
                  </button>
                </li>
              </ul>''' in resp_data3 
    
    # Clear database
    Rating.query.delete()
    Users.query.delete()
    db.session.commit()

def test_logout(test_client):
    
    # Creating a test user
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
    assert resp1.status_code == 200
    #print(resp_data)
    assert "You've been logged out!" in resp_data
    assert '<h1 class="d-flex justify-content-center fw-bold">Login</h1>' in resp_data

    # Clear database
    # Clear database
    Rating.query.delete()
    Users.query.delete()
    db.session.commit()

def test_search_rating(test_client):

    Rating.query.delete()
    db.session.commit()

    pass_data = bcrypt.generate_password_hash('testpassword')
    hash_password = pass_data.decode('utf-8')
    test_user = Users( 
                        username='testuser', 
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

    temp_rating1 = Rating(rater_id=test_user.user_id, restroom_name="Testroom1", cleanliness=3.0, overall=3.5)
    temp_rating2 = Rating(rater_id=test_user.user_id, restroom_name="Testroom 2", cleanliness=2.0, overall=2.5)
    db.session.add(temp_rating1)
    db.session.add(temp_rating2)
    db.session.commit()

    res = test_client.get('/search?searchbox=Test')
    data = res.data.decode()

    #assert res.status_code == 200
    assert '<h5 class="card-title">Testroom1</h5>' in data
    assert '<h5 class="card-title">Testroom 2</h5>' in data
    assert '<div class="alert alert-danger" role="alert">No restrooms found!</div>' not in data

    res = test_client.get('/search?searchbox=NotInDB')
    data = res.data.decode()

    assert '<h5 class="card-title">Testroom1</h5>' not in data
    assert '<h5 class="card-title">Testroom 2</h5>' not in data
    assert '<div class="alert alert-danger" role="alert">No restrooms found!</div>' in data
    Rating.query.delete()
    db.session.commit()



    Users.query.delete()
    db.session.commit()
