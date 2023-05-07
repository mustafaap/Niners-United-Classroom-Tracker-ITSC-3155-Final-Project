from src.models import db, Rating, Users, Comments, Rating_votes, Comment_votes

def test_delete_rating(test_client):
    # Clear database
    Rating.query.delete()
    db.session.commit()

    # Add test rating
    temp_rating1 = Rating(rater_id=1, restroom_name="Testroom1", cleanliness=3.0, overall=3.5)
    temp_rating2 = Rating(rater_id=2, restroom_name="Testroom 2", cleanliness=2.0, overall=2.5)
    db.session.add(temp_rating1)
    db.session.add(temp_rating2)
    db.session.commit()

    # Get the rating's ID
    rating_id1 = temp_rating1.rating_id
    rating_id2 = temp_rating2.rating_id
    # Delete the test rating
    response = test_client.post(f'/restroom/{rating_id1}/delete')

    assert response.status_code == 302

    # Check that the rating was deleted from the database
    rating1 = db.session.get(Rating, rating_id1)
    assert rating1 is None
    # Check that the rating was not deleted from the database
    rating2 = db.session.get(Rating, rating_id2)
    assert rating2 is not None
    
    # Clear database
    Rating.query.delete()
    db.session.commit()