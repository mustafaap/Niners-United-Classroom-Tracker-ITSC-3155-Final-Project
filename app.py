from flask import Flask, render_template, url_for, request, redirect
from src.models import db, Rating
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)

db_user = os.getenv('DB_USER')
db_pass = os.getenv('DB_PASS')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'
db.init_app(app)
api_key = os.getenv('API_KEY')


@app.get('/')
def index():
    # Default sort is most recent
    ratings = Rating.query.order_by(Rating.rating_id.desc()).all()
    return render_template('index.html', index_active=True, ratings=ratings)


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


@app.post('/leaverating')
def indexrating():
    location = request.form.get('location')
    comments = request.form.get('comments')
    cleanliness = request.form.get('cleanliness')
    overall = request.form.get('overall')

    new_rating = Rating(restroom_name=location, cleanliness=cleanliness, accessibility="temp", functionality=True, overall=overall, comments=comments)
    db.session.add(new_rating)
    db.session.commit()

    return redirect('/')


@app.get('/new')
def create_restroom_form():
    return render_template('create_restroom.html', create_restroom_active=True)


@app.post('/create')
def create_restroom():
    restroom_name = request.form.get('restroom')
    cleanliness = request.form.get('clean_rating')
    accessibility = request.form.getlist('accessibility')
    functionality = request.form['func']

    if functionality == 'Open':
        functionality = True
    else:
        functionality = False

    overall = request.form.get('overall_rating')
    comments = request.form.get('comment')

    new_restroom = Rating(restroom_name=restroom_name, cleanliness=cleanliness, accessibility=accessibility, functionality=functionality, overall=overall, comments=comments)
    db.session.add(new_restroom)
    db.session.commit()
    return redirect('/')


@app.get('/maps')
def load_maps():
    return render_template('maps.html', maps_active=True, api_key=api_key)


@app.get('/singlerestroom/<int:rating_id>')
def view_single_restroom(rating_id):
    rating = Rating.query.get(rating_id)
    return render_template('single_restroom.html', rating=rating)


@app.get('/login')
def login():
    return render_template('login.html', login_active=True)


@app.get('/signup')
def display_sign_up_page():
    return render_template("signup.html", signup_active=True)


@app.get('/about')
def about():
    return render_template('about.html', about_active=True)


@app.get('/search')
def search():
    term = (request.args.get('searchbox'))
    ratings = db.session.query(Rating).filter(Rating.restroom_name.ilike('%' + term + '%')).all()
    # print(ratings)
    return render_template('index.html', ratings=ratings)


@app.get('/restroom/<int:rating_id>/edit')
def get_edit_restroom_page(rating_id: int):
    rating = Rating.query.get(rating_id)
    return render_template('edit_restroom.html', rating=rating)


@app.post('/restroom/<int:rating_id>')
def update_restroom(rating_id: int):
    rating = Rating.query.get(rating_id)
    restroom_name = request.form.get('restroom')
    cleanliness = request.form.get('clean_rating')
    accessibility = request.form.getlist('accessibility')
    functionality = request.form.get('func')

    if functionality == 'Open':
        functionality = True
    else:
        functionality = False

    overall = request.form.get('overall_rating')
    comments = request.form.get('comment')

    rating.restroom_name = restroom_name
    rating.cleanliness = cleanliness
    rating.accessibility = accessibility
    rating.functionality = functionality
    rating.overall = overall
    rating.comments = comments

    db.session.commit()

    return redirect(url_for('view_single_restroom', rating_id=rating_id))

@app.post('/<int:rating_id>/delete')
def delete_rating(rating_id: int):
    rating = Rating.query.get(rating_id)
    db.session.delete(rating)
    db.session.commit()
    return redirect('/')