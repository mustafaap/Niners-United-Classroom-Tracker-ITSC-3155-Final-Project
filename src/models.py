from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Rating(db.Model):
    rating_id = db.Column(db.Integer, primary_key=True)
    restroom_name = db.Column(db.String(255), nullable=False)
    cleanliness = db.Column(db.Integer, nullable=False)
    accessibility = db.Column(db.String(255), nullable=False)
    functionality = db.Column(db.Boolean, nullable=False)
    overall = db.Column(db.Integer, nullable=False)
    comments = db.Column(db.String(255), nullable=False)