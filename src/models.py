from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ARRAY
from sqlalchemy.ext.mutable import MutableList

db = SQLAlchemy()

class Rating(db.Model):
    __tablename__ = 'rating'

    rating_id = db.Column(db.Integer, primary_key=True)
    restroom_name = db.Column(db.String(255))
    rating_body = db.Column(db.Text)
    cleanliness = db.Column(db.Numeric(2,1))
    accessibility = db.Column(db.String(255))
    functionality = db.Column(db.Boolean)
    overall = db.Column(db.Numeric(2,1))
    map_tag = db.Column(db.String(255))
    votes = db.Column(db.Integer, default=0)
    rater_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=True)
    comments = db.Column(MutableList.as_mutable(db.ARRAY(db.Integer)), default=[])
    # rater = db.relationship('Users', backref='rating_user')

    def __init__(self, restroom_name, cleanliness, overall, rating_body=None, accessibility=None, functionality=None, map_tag=None, votes=None, rater_id=None, comments=None):
        self.restroom_name = restroom_name
        self.rating_body = rating_body
        self.cleanliness = cleanliness
        self.accessibility = accessibility
        self.functionality = functionality
        self.overall = overall
        self.map_tag = map_tag
        self.votes = votes
        self.rater_id = rater_id
        self.comments = comments if comments is not None else []


class Users(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    favorite = db.Column(db.String(255))
    picture = db.Column(db.String(255))
    commented_on = db.Column(MutableList.as_mutable(db.ARRAY(db.Integer)), default=[])
    rupvoted_on = db.Column(MutableList.as_mutable(db.ARRAY(db.Integer)), default=[])
    rdownvoted_on = db.Column(MutableList.as_mutable(db.ARRAY(db.Integer)), default=[])
    cupvoted_on = db.Column(MutableList.as_mutable(db.ARRAY(db.Integer)), default=[])
    cdownvoted_on = db.Column(MutableList.as_mutable(db.ARRAY(db.Integer)), default=[])

    def __init__(self, username: str, password: str, first_name: str, last_name: str, email: str, commented_on, rupvoted_on, rdownvoted_on, cupvoted_on, cdownvoted_on):
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.commented_on = commented_on
        self.rupvoted_on = rupvoted_on
        self.rdownvoted_on = rdownvoted_on
        self.cupvoted_on = cupvoted_on
        self.cdownvoted_on = cdownvoted_on


class Comments(db.Model):
    __tablename__ = 'comments'

    comment_id = db.Column(db.Integer, primary_key=True)
    comment_body = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=True)
    # user = db.relationship('Users', backref='user_comment')
    rating_id = db.Column(db.Integer, db.ForeignKey('rating.rating_id', ondelete='CASCADE'), nullable=True)
    # rating = db.relationship('Rating', backref='rating_comment', cascade='all, delete')
    total_votes = db.Column(db.Integer, default=0)
    comment_id_vote = db.Column(db.Integer, db.ForeignKey('comments.comment_id', ondelete='CASCADE'), nullable=True)
    # comment = db.relationship('Comments', foreign_keys=[comment_id_vote])

    def __init__(self, comment_body=None, user_id=None, rating_id=None, total_votes=None, comment_id_vote=None):
        self.comment_body = comment_body
        self.user_id = user_id
        self.rating_id = rating_id
        self.total_votes = total_votes
        self.comment_id_vote = comment_id_vote


class Rating_votes(db.Model):
    __tablename__ = 'rating_votes'

    vote_id = db.Column(db.Integer, primary_key=True)  # New primary key
    rating_id = db.Column(db.Integer, db.ForeignKey('rating.rating_id', ondelete='CASCADE'))  # Removed primary_key=True
    upvotes = db.Column(db.Integer, default=0)
    downvotes = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=True)
    # user = db.relationship('Users', backref='user_rating_votes', cascade='all, delete')
    rating_id_vote = db.Column(db.Integer, db.ForeignKey('rating.rating_id', ondelete='CASCADE'), nullable=True)
    # rating = db.relationship('Rating', backref='rating_votes', cascade='all, delete')
    # rating = db.relationship('Rating', foreign_keys=[rating_id], backref=db.backref('rating_votes', cascade='all, delete'))
    # rating_vote = db.relationship('Rating', foreign_keys=[rating_id_vote])

    def __init__(self,vote_id , rating_id, upvotes, downvotes, user_id, rating_id_vote):
        self.vote_id = vote_id
        self.rating_id = rating_id
        self.upvotes = upvotes
        self.downvotes = downvotes
        self.user_id = user_id
        self.rating_id_vote = rating_id_vote


class Comment_votes(db.Model):
    __tablename__ = 'comment_votes'

    comment_id = db.Column(db.Integer, primary_key=True)
    upvotes = db.Column(db.Integer, default=0)
    downvotes = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=True)
    # user = db.relationship('Users', backref='user_comment_votes', cascade='all, delete')
    comment_id_vote = db.Column(db.Integer, db.ForeignKey('comments.comment_id', ondelete='CASCADE'), nullable=True)
    # comment = db.relationship('Comments', backref='comment_votes', cascade='all, delete')

    def __init__(self, comment_id, upvotes, downvotes, user_id, comment_id_vote):
        self.comment_id = comment_id
        self.upvotes = upvotes
        self.downvotes = downvotes
        self.user_id = user_id
        self.comment_id_vote = comment_id_vote
