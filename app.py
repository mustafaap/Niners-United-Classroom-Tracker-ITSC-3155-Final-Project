from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.get('/')
def index():
    return render_template('index.html')

@app.get('/new')
def create_restroom_form():
    return render_template('create_restroom.html')

@app.get('/<int:restroom_id>')
def single_restroom_form(restroom_id: int):
    restroom = db.get_restroom(restroom_id)
    return render_template('single_restroom.html', restroom=restroom)