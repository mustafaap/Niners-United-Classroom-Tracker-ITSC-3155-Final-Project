from src.models import db, Rating
class RatingRepository:

    def delete_rating(self, rating_id):
        db.session.query(Rating).filter_by(rating_id).delete()
        db.session.commit()