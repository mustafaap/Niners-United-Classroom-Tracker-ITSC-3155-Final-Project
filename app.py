from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.get('/')
def index():
    return render_template('index.html')

@app.get('/new')
def create_restroom_form():
    return render_template('create_restroom.html')

@app.get('/login')
def login():
    return render_template('login.html')