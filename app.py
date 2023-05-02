import json
from flask import Flask, render_template, session, url_for, request, redirect, abort
from src.models import db, Rating, Users, Comments, Rating_votes, Comment_votes
from dotenv import load_dotenv
from security import bcrypt
import os

load_dotenv()
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

app.secret_key = os.getenv('APP_SECRET')

db.init_app(app)
api_key = os.getenv('API_KEY')

bcrypt.init_app(app)

# os.remove(filename) to remove from static folder

# Index page
@app.get('/')
def index():
    # Default sort is most recent
    ratings = Rating.query.order_by(Rating.rating_id.desc()).all()
    return render_template('index.html', index_active=True, ratings=ratings)


# Sort index page by
@app.post('/')
def sortby():
    sort_by = request.form.get('sort-by', 'Most Recent')
    if sort_by == 'Most Recent':
        ratings = Rating.query.order_by(Rating.rating_id.desc()).all()
    elif sort_by == 'Cleanliness':
        ratings = Rating.query.order_by(Rating.cleanliness.desc()).all()
    elif sort_by == 'Handicap':
        ratings = Rating.query.filter(Rating.accessibility.ilike('%handicap%')).all()
    elif sort_by == 'Functionality':
        ratings = Rating.query.filter(Rating.functionality == True).all()
    elif sort_by == 'Faculty Only':
        ratings = Rating.query.filter(Rating.accessibility.ilike('%faculty%'), ~Rating.accessibility.ilike('%student%')).all()
    elif sort_by == 'Overall':
        ratings = Rating.query.order_by(Rating.overall.desc()).all()
    else:
        ratings = Rating.query.all()
    
    return render_template('index.html', index_active=True, ratings=ratings)


# Shorthand create rating
@app.post('/leaverating')
def indexrating():
    if 'user' not in session:
        session['message'] = "You must be logged in to leave a rating!"
        
        return redirect(url_for('login'))
    
    location = request.form.get('location')
    rating_body = request.form.get('rating_body')
    cleanliness = request.form.get('cleanliness')
    overall = request.form.get('overall')

    new_rating = Rating(restroom_name=location, cleanliness=cleanliness, overall=overall, rating_body=rating_body)
    db.session.add(new_rating)
    db.session.commit()

    return redirect('/')


# NUTT Map
@app.get('/maps')
def load_maps():
    # Carousel for cards
    return render_template('maps.html', maps_active=True, api_key=api_key)


# View new detailed rating page
@app.get('/new')
def create_restroom_form():
    return render_template('create_restroom.html', create_restroom_active=True)


# Create detailed rating
@app.post('/create')
def create_restroom():
    if 'user' not in session:
        session['message'] = "You must be logged in to leave a rating!"
        
        return redirect(url_for('login'))
    
    restroom_name = request.form.get('restroom')
    cleanliness = request.form.get('clean_rating')
    accessibility = request.form.getlist('accessibility')
    functionality = request.form.get('func')
    overall = request.form.get('overall_rating')
    rating_body = request.form.get('rating_body')

    if functionality == 'Open':
        functionality = True
    else:
        functionality = False

    new_restroom = Rating(restroom_name=restroom_name, cleanliness=cleanliness, accessibility=accessibility, functionality=functionality, overall=overall, rating_body=rating_body)
    db.session.add(new_restroom)
    db.session.commit()
    return redirect('/')


# View single rating
@app.get('/restroom/<int:rating_id>')
def view_single_restroom(rating_id):
    rating = Rating.query.get(rating_id)
    comments = Comments.query.filter(Comments.comment_id.in_(rating.comments)).all()
    return render_template('single_restroom.html', rating=rating, comments=comments)


# View edit rating page
@app.get('/restroom/<int:rating_id>/edit')
def get_edit_restroom_page(rating_id: int):
    rating = Rating.query.get(rating_id)
    return render_template('edit_restroom.html', rating=rating)


# Edit rating info
@app.post('/restroom/<int:rating_id>')
def update_restroom(rating_id: int):
    rating = Rating.query.get(rating_id)
    restroom_name = request.form.get('restroom')
    cleanliness = request.form.get('clean_rating')
    accessibility = request.form.getlist('accessibility')
    functionality = request.form.get('func')
    overall = request.form.get('overall_rating')
    rating_body = request.form.get('rating_body')

    if functionality == 'Open':
        functionality = True
    else:
        functionality = False

    rating.restroom_name = restroom_name
    rating.cleanliness = cleanliness
    rating.accessibility = accessibility
    rating.functionality = functionality
    rating.overall = overall
    rating.rating_body = rating_body

    db.session.commit()

    return redirect(url_for('view_single_restroom', rating_id=rating_id))


# Delete rating
@app.post('/restroom/<int:rating_id>/delete')
def delete_rating(rating_id: int):
    rating = Rating.query.get(rating_id)

    # Delete comments
    comments = Comments.query.filter(Comments.rating_id == rating_id).all()
    for comment in comments:
        db.session.delete(comment)

    # Delete rating_votes
    rating_votes = Rating_votes.query.filter(Rating_votes.rating_id_vote == rating_id).all()
    for vote in rating_votes:
        db.session.delete(vote)

    db.session.delete(rating)
    db.session.commit()
    return redirect('/')


# Comment on rating
@app.post('/restroom/<int:rating_id>/comment')
def addcomment(rating_id):
    rating = Rating.query.get(rating_id)
    comment_body = request.form.get('comment')
    new_comment = Comments(comment_body=comment_body, rating_id=rating_id)
    db.session.add(new_comment)
    db.session.commit()

    rating.comments.append(new_comment.comment_id)
    db.session.commit()

    rating = Rating.query.get(rating_id)

    return redirect(url_for('view_single_restroom', rating_id=rating_id))


# Delete comment on rating
@app.post('/restroom/<int:rating_id>/comment/<int:comment_id>/delete')
def deletecomment(rating_id, comment_id):
    comment = Comments.query.get(comment_id)
    db.session.delete(comment)
    db.session.commit()

    return redirect(url_for('view_single_restroom', rating_id=rating_id))


# About page
@app.get('/about')
def about():
    return render_template('about.html', about_active=True)


# Search rating titles by keyword
@app.get('/search')
def search():
    term = request.args.get('searchbox')
    ratings = db.session.query(Rating).filter(Rating.restroom_name.ilike('%' + term + '%')).all()
    return render_template('index.html', ratings=ratings)


# Cat pic (temporary, view_user should actually be this, and then this can be deleted)
@app.get('/profile')
def profile():
    return render_template('profile.html', profile_active = True)


# Upvote rating
@app.post('/upvote/<int:rating_id>')
def upvote(rating_id: int):
    print('upvoting')
    if request.method == 'POST':
        data = json.loads(request.data)
        print(data)
        rating = Rating.query.filter_by(rating_id = data['rating_id']).first()
        print(rating.votes)

        if rating:
            if rating.votes:
                setattr(rating, 'votes', int(rating.votes) + 1)
            else:
                setattr(rating, 'votes', 1)
            db.session.commit()
    return redirect(url_for('index'))


# Downvote rating
@app.post('/downvote/<int:rating_id>')
def downvote(rating_id: int):
    if request.method == 'POST':
        data = json.loads(request.data)
        print(data['rating_id'])
        rating = Rating.query.filter_by(rating_id = data['rating_id']).first()
        print(rating.votes)

        if rating:
            if rating.votes:
                setattr(rating, 'votes', int(rating.votes) - 1)
            else:
                setattr(rating, 'votes', -1)
            db.session.commit()
    return redirect(url_for('index'))


# Login page
@app.get('/login')
def login():
    message = session.pop('message', None)
    return render_template('login.html', login_active=True, message=message)


# Signup page
@app.get('/signup')
def display_sign_up_page():
    return render_template("signup.html", signup_active=True)


# View profile
@app.get('/view_user')
def view_user():
    if 'user' not in session:
        return redirect('/login')
    user = session['user']
    return render_template('view_user.html', user=user)


# Log in to session
@app.post('/login')
def user_login():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        abort(400)

    existing_user = Users.query.filter_by(username=username).first()

    if not existing_user or not bcrypt.check_password_hash(existing_user.password, password):
        message = "Incorrect username or password"
        return render_template('login.html', login_active=True, message=message)

    if bcrypt.check_password_hash(existing_user.password, password):
        session['user'] = { 
        'username': username
        }
        return redirect('/view_user')
    
    return render_template('login.html', login_active=True)


# Sign up for account
@app.post('/register')
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    email = request.form.get('email')

    if not username or not password or not fname or not lname or not email:
        abort(400)

    hashed_password = bcrypt.generate_password_hash(password).decode()

    new_user = Users(username, hashed_password, fname, lname, email)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/login')


# Log out of session
@app.post('/logout')
def logout():
    del session['user']
    return redirect('/login')
