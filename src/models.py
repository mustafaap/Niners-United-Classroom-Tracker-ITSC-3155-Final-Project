from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Rating(db.Model):
    rating_id = db.Column(db.Integer, primary_key=True)
    restroom_name = db.Column(db.String(255))
    rating_body = db.Column(db.Text)
    cleanliness = db.Column(db.Numeric(2,1))
    accessibility = db.Column(db.String(255))
    functionality = db.Column(db.Boolean)
    overall = db.Column(db.Numeric(2,1))
    map_tag = db.Column(db.String(255))
    votes = db.Column(db.Integer)
    rater_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)
    rater = db.relationship('Users', backref='rating_user')


class Users(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    favorite = db.Column(db.String(255))
    picture = db.Column(db.String(255))

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

class Comments(db.Model):
    comment_id = db.Column(db.Integer, primary_key=True)
    comment_body = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)
    user = db.relationship('Users', backref='user_comment')
    rating_id = db.Column(db.Integer, db.ForeignKey('rating.rating_id'), nullable=True)
    rating = db.relationship('Rating', backref='rating_comment')
    total_votes = db.Column(db.Integer)

class Rating_votes(db.Model):
    rating_id = db.Column(db.Integer, primary_key=True)
    upvotes = db.Column(db.Integer)
    downvotes = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)
    user = db.relationship('Users', backref='user_rating_votes')
    rating_id_vote = db.Column(db.Integer, db.ForeignKey('rating.rating_id'), nullable=True)
    rating = db.relationship('Rating', backref='rating_votes')

class Comment_votes(db.Model):
    comment_id = db.Column(db.Integer, primary_key=True)
    upvotes = db.Column(db.Integer)
    downvotes = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)
    user = db.relationship('Users', backref='user_comment_votes')
    comment_id_vote = db.Column(db.Integer, db.ForeignKey('comments.comment_id'), nullable=True)
    comment = db.relationship('Comments', backref='comment_votes')

