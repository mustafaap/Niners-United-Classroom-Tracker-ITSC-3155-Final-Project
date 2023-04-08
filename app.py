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

@app.get('/')
def index():
    ratings = Rating.query.all()
    return render_template('index.html', ratings=ratings)

@app.get('/new')
def create_restroom_form():
    return render_template('create_restroom.html')

@app.post('/')
def create_restroom():
    restroom_name = request.form.get('restroom')
    cleanliness = request.form.get('clean_rating')
    #accessibility
    accessibility = request.form.getlist('accessibility')
    #functionality
    functionality = request.form['func']
    print(functionality)

    if functionality == 'Open':
        functionality = True
    else:
        functionality = False

    overall = request.form.get('overall_rating')
    comments = request.form.get('comment')

    new_restroom = Rating(restroom_name = restroom_name, cleanliness = cleanliness, accessibility = accessibility, functionality = functionality, overall = overall, comments = comments)
    db.session.add(new_restroom)
    db.session.commit()
    return redirect('/')


@app.get('/singlerestroom')
def view_single_restroom():
    return render_template('single_restroom.html')

@app.get('/signup')
def display_sign_up_page():
    return render_template("signup.html")

@app.get('/login')
def login():
    return render_template('login.html')

@app.get('/about')
def about():
    return render_template('about.html')
