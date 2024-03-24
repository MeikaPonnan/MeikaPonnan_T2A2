from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from init import db
from models.book import Book
from models.review import Review, review_schema

reviews_bp = Blueprint('reviews', __name__, url_prefix="/<int:book_id>/reviews")


@reviews_bp.route("/", methods=["POST"])
@jwt_required()
def create_review(book_id):
    body_data = request.get_json()
    stmt = db.select(Book).filter_by(id=book_id)
    book = db.session.scalar(stmt)
    if book:
        review = Review(
            rating = body_data.get('rating'),
            comment = body_data.get('comment'),
            user_id = get_jwt_identity(),
            book_id = book_id
        )
        db.session.add(review)
        db.session.commit()
        return review_schema.dump(review), 201
    else:
        return {"error": f"Book with id {book_id} doesn't exist"}, 404
    
@reviews_bp.route("/<int:review_id>", methods=["DELETE"])
@jwt_required()
def delete_review(book_id, review_id):
    stmt = db.select(Review).filter_by(id=review_id)
    review = db.session.scalar(stmt)
    if review and review.book.id == book_id:
        db.session.delete(review)
        db.session.commit()
        return {"message": f"Review ith id {review_id} has been deleted."}
    else:
        return {"error": f"Review with id {review_id} not found on book with id {book_id}."}, 404
    
    
@reviews_bp.route("/<int:review_id>", methods=["PUT", "PATCH"])
@jwt_required()
def edit_review(book_id, review_id):
    body_data = request.get_json()
    stmt = db.select(Review).filter_by(id=review_id, book_id=book_id)
    review = db.session.scalar(stmt)
    if review:
        review.rating = body_data.get('rating') or review.rating
        review.comment = body_data.get('comment') or review.comment
        db.session.commit()
        return review_schema.dump(review)
    else:
        return {"error": f"Review with id {review_id} not found for book with id {book_id}."}  
    
          