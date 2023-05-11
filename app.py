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
app.config['SESSION_TYPE'] = 'filesystem'

db.init_app(app)
api_key = os.getenv('API_KEY')

bcrypt.init_app(app)

# os.remove(filename) to remove from static folder

# Index page
@app.get('/')
def index():
    # Default sort is most recent
    ratings = Rating.query.order_by(Rating.rating_id.desc()).all()
    logged_in_message = session.pop('logged_in_message', None)
    voting_message = session.pop('voting_message', None)
    return render_template('index.html', index_active=True, ratings=ratings, logged_in_message=logged_in_message, voting_message=voting_message)


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
    rater_id = session['user']['user_id']

    new_rating = Rating(restroom_name=location, cleanliness=cleanliness, overall=overall, rating_body=rating_body, rater_id=rater_id)
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
    if 'user' not in session:
        session['message'] = "You must be logged in to leave a rating!"
        
        return redirect(url_for('login'))
    
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
    rater_id = session['user']['user_id']

    if functionality == 'Open':
        functionality = True
    else:
        functionality = False

    new_restroom = Rating(restroom_name=restroom_name, cleanliness=cleanliness, accessibility=accessibility, functionality=functionality, overall=overall, rating_body=rating_body, rater_id=rater_id)
    db.session.add(new_restroom)
    db.session.commit()
    return redirect('/')


# View single rating
@app.get('/restroom/<int:rating_id>')
def view_single_restroom(rating_id: int):
    rating = Rating.query.get(rating_id)

    if 'user' in session:
        user_id = session['user']['user_id']
    else:
        user_id = None

    comments = Comments.query.filter(Comments.comment_id.in_(rating.comments)).all()

    already_commented = session.pop('already_commented', None)
    voting_message = session.pop('voting_message', None)

    return render_template('single_restroom.html', rating=rating, comments=comments, user_id=user_id, already_commented=already_commented, voting_message=voting_message)


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

    comments = Comments.query.filter(Comments.rating_id == rating_id).all()
    for comment in comments:
        db.session.delete(comment)
    
    rating_votes = Rating_votes.query.filter(Rating_votes.rating_id_vote == rating_id).all()
    for vote in rating_votes:
        db.session.delete(vote)

    db.session.delete(rating)
    db.session.commit()
    return redirect('/')


# Comment on rating
@app.post('/restroom/<int:rating_id>/comment')
def addcomment(rating_id: int):
    rating = Rating.query.get(rating_id)
    user_id = session['user']['user_id']
    user = Users.query.get(user_id)

    if rating_id not in user.commented_on:
        comment_body = request.form.get('comment')
        new_comment = Comments(comment_body=comment_body, rating_id=rating_id, user_id=user_id)
        db.session.add(new_comment)
        db.session.commit()

        rating.comments.append(new_comment.comment_id)
        db.session.commit()

        user.commented_on.append(rating_id)
        db.session.commit()
    else:
        session['already_commented'] = "You cannot comment on a post you've already commented on!"

    return redirect(url_for('view_single_restroom', rating_id=rating_id))


# Edit comment on rating
@app.post('/restroom/<int:rating_id>/comment/<int:comment_id>/edit')
def editcomment(rating_id, comment_id):
    comment = Comments.query.get(comment_id)
    comment_body = request.form.get('edited_comment')
    comment.comment_body = comment_body
    db.session.commit()

    return redirect(url_for('view_single_restroom', rating_id=rating_id))


# Delete comment on rating
@app.post('/restroom/<int:rating_id>/comment/<int:comment_id>/delete')
def deletecomment(rating_id, comment_id):
    rating = Rating.query.get(rating_id)
    rating.comments.remove(comment_id)
    db.session.commit()
    
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
    return render_template('index.html',index_active=True, ratings=ratings)


# Upvote rating
@app.post('/upvote/<int:rating_id>')
def upvote(rating_id: int):
    rating = Rating.query.get(rating_id)
    if session.get('user') is not None:
        user_id = session['user']['user_id']
        user = Users.query.get(user_id)

        if rating:
            if rating_id not in user.rupvoted_on and rating_id not in user.rdownvoted_on: #user has not voted at all
                setattr(rating, 'votes', int(rating.votes) + 1)
                user.rupvoted_on.append(rating_id)
                db.session.commit()
            elif rating_id in user.rupvoted_on and rating_id not in user.rdownvoted_on: #user clicking upvote again (unvoting)
                setattr(rating, 'votes', int(rating.votes) - 1)
                user.rupvoted_on.remove(rating_id)
                db.session.commit()
            db.session.commit()
    else:
        session['voting_message'] = "You must log in to interact with posts."
    return str(rating.votes)

# Downvote rating
@app.post('/downvote/<int:rating_id>')
def downvote(rating_id: int):
    rating = Rating.query.get(rating_id)
    if session.get('user') is not None:
        user_id = session['user']['user_id']
        user = Users.query.get(user_id)

        if rating:
            if rating_id not in user.rupvoted_on and rating_id not in user.rdownvoted_on:
                setattr(rating, 'votes', int(rating.votes) - 1)
                user.rdownvoted_on.append(rating_id)
                db.session.commit()
            elif rating_id in user.rdownvoted_on and rating_id not in user.rupvoted_on: 
                setattr(rating, 'votes', int(rating.votes) + 1)
                user.rdownvoted_on.remove(rating_id)
                db.session.commit()
            db.session.commit()
    else:
        session['voting_message'] = "You must log in to interact with posts."
    return str(rating.votes)

# Upvote comment
@app.post('/commentupvote/<int:rating_id>/<int:comment_id>')
def comment_upvote(rating_id, comment_id):
    rating = Rating.query.get(rating_id)
    comment = Comments.query.get(comment_id)
    if session.get('user') is not None:
        user_id = session['user']['user_id']
        user = Users.query.get(user_id)

        if comment and rating:
            if comment_id not in user.cupvoted_on and comment_id not in user.cdownvoted_on:
                setattr(comment, 'total_votes', int(comment.total_votes) + 1)
                user.cupvoted_on.append(comment_id)
                db.session.commit()
            elif comment_id in user.cupvoted_on and comment_id not in user.cdownvoted_on: 
                setattr(comment, 'total_votes', int(comment.total_votes) - 1)
                user.cupvoted_on.remove(comment_id)
                db.session.commit()
            db.session.commit()
    else:
        session['voting_message'] = "You must log in to interact with posts."
    return str(comment.total_votes)

# Downvote comment
@app.post('/commentdownvote/<int:rating_id>/<int:comment_id>')
def comment_downvote(rating_id, comment_id):
    rating = Rating.query.get(rating_id)
    comment = Comments.query.get(comment_id)
    if session.get('user') is not None:
        user_id = session['user']['user_id']
        user = Users.query.get(user_id)

        if comment and rating:
            if comment_id not in user.cupvoted_on and comment_id not in user.cdownvoted_on:
                setattr(comment, 'total_votes', int(comment.total_votes) - 1)
                user.cdownvoted_on.append(comment_id)
                db.session.commit()
            elif comment_id in user.cdownvoted_on and comment_id not in user.cupvoted_on: 
                setattr(comment, 'total_votes', int(comment.total_votes) + 1)
                user.cdownvoted_on.remove(comment_id)
                db.session.commit()
            db.session.commit()
    else:
        session['voting_message'] = "You must log in to interact with posts."
    return str(comment.total_votes)


# Login page
@app.get('/login')
def login():
    message = session.pop('message', None)
    success_message = session.pop('success_message', None)
    return render_template('login.html', login_active=True, message=message, success_message=success_message)


# Signup page
@app.get('/signup')
def display_sign_up_page():
    return render_template("signup.html", signup_active=True)


# View profile
@app.get('/profile')
def profile():
    if 'user' not in session:
        return redirect('/login')
    user = session['user']
    success_message = session.pop('success_message', None)
    return render_template('view_profile.html', user=user, success_message=success_message)


#Get edit profile page
@app.get('/profile/edit')
def getEditProfile():
    if 'user' not in session:
        return redirect('/login')
    user = session['user']
    return render_template("edit_profile.html", user=user)


#Update profile
@app.post('/profile/<int:user_id>')
def updateProfile(user_id: int):
    if 'user' not in session:
        return redirect('/login')
    
    user = Users.query.get(user_id)
    
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    username = request.form.get('username')
    email = request.form.get('email')

    user.fname = fname
    user.lname = lname
    user.username = username
    user.email = email
    db.session.commit()

    session['user']['fname'] = fname
    session['user']['lname'] = lname
    session['user']['username'] = username
    session['user']['email'] = email
    session.modified = True

    return redirect('/profile')

#Get change password page
@app.get('/changePassword')
def getChangePassword():
    if 'user' not in session:
        return redirect('/login')
    user = session['user']
    message = session.pop('message', None)
    return render_template("change_password.html", user=user, message=message)


#Update password
@app.post('/updatePassword')
def updatePassword():
    if 'user' not in session:
        return redirect('/login')
    
    old_password = request.form.get('oldPassword')
    new_password = request.form.get('password')
    repassword = request.form.get('repassword')

    user_id = session['user']['user_id']
    user = Users.query.get(user_id)

    if not old_password or not new_password or not repassword or not user:
        abort(400)
    
    if not bcrypt.check_password_hash(user.password, old_password):
        session['message'] = "Incorrect old password!"
        return redirect(url_for('getChangePassword'))

    user.password = bcrypt.generate_password_hash(new_password).decode()
    db.session.commit()
    session['success_message'] = "Password changed successfully!"

    return redirect(url_for('profile'))


# Log in to session
@app.post('/login')
def user_login():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        abort(400)

    existing_user = Users.query.filter_by(username=username).first()

    if not existing_user or not bcrypt.check_password_hash(existing_user.password, password):
        session['message'] = "Incorrect username or password!"
        return redirect(url_for('login'))

    if bcrypt.check_password_hash(existing_user.password, password):
        session['user'] = {
        'user_id': existing_user.user_id, 
        'username': existing_user.username,
        'password': existing_user.password,
        'fname': existing_user.first_name,
        'lname': existing_user.last_name,
        'email': existing_user.email
        }
        session['logged_in'] = True
        session['logged_in_message'] = "Success! You are logged in."
        return redirect(url_for('index'))
    
    return redirect(url_for('login'))


# Sign up for account
@app.post('/register')
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    repassword = request.form.get('repassword')
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    email = request.form.get('email')

    if not username or not password or not fname or not lname or not email or not repassword:
        abort(400)

    hashed_password = bcrypt.generate_password_hash(password).decode()

    new_user = Users(username, hashed_password, fname, lname, email, commented_on=[], rupvoted_on=[], rdownvoted_on=[], cupvoted_on=[], cdownvoted_on=[])
    db.session.add(new_user)
    db.session.commit()

    session['success_message'] = "Account created successfully!"

    return redirect(url_for('login'))


# Log out of session
@app.post('/logout')
def logout():
    if 'user' in session:
        del session['user']
    session.pop('logged_in', None)
    session['success_message'] = "You've been logged out!"
    return redirect(url_for('login'))
