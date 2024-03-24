from flask import Blueprint, request
from init import db
from models.book import Book, books_schema, book_schema
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.review import Review, review_schema

books_bp = Blueprint('books', __name__, url_prefix='/books')

@books_bp.route('/')
def get_all_books():
    stmt = db.select(Book)
    books = db.session.scalars(stmt)
    return books_schema.dump(books)

@books_bp.route('<int:book_id>')
def get_one_book(book_id):
    stmt = db.select(Book).filter_by(id=book_id)
    book = db.session.scalar(stmt)
    if book:
        return book_schema.dump(book)
    else:
        return {"error": f"Book with id {book_id} not found."}, 404
    
@books_bp.route('/', methods=["POST"])
@jwt_required()
def create_book():
    body_data = request.get_json()
    book = Book(
        title=body_data.get('title'),
        author=body_data.get('author'),
        pagecount=body_data.get('pagecount'),
        status=body_data.get('status'),
        review=body_data.get('review'),
        genre=body_data.get('genre'),
        user_id= get_jwt_identity()

    )
    db.session.add(book)
    db.session.commit()
    return book_schema.dump(book), 201

@books_bp.route('/<int:book_id>', methods=["DELETE"])
def delete_book(book_id):
    stmt = db.select(Book).filter_by(id=book_id)
    book = db.session.scalar(stmt)
    if book:
        db.session.delete(book)
        db.session.commit()
        return {'message': f"Book '{book.title}' deleted successfully."}
    else:
        return {'error': f"Book with id {book_id} not found."}, 404
    
@books_bp.route('/<int:book_id>', methods=["PUT", "PATCH"])
def update_book(book_id):
    body_data = request.get_json()
    stmt = db.select(Book).filter_by(id=book_id)
    book = db.session.scalar(stmt)
    if book:
        book.title = body_data.get('title') or book.title
        book.author = body_data.get('author') or book.author
        book.pagecount = body_data.get('pagecount') or book.pagecount
        book.status = body_data.get('status') or book.status
        book.review = body_data.get('review') or book.review
        book.genre = body_data.get('genre') or book.genre
        db.session.commit()
        return book_schema.dump(book)
    else:
        return {'error': f'Book with id {book_id} not found.'}, 404

@books_bp.route("/<int:book_id>/reviews", methods=["POST"])
@jwt_required()
def create_review(book_id):
    body_data = request.get_json()
    stmt = d.select(Book).filter_by(id=book_id)
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
    
@books_bp.route("/<int:book_id>/reviews/<int:review_id>", methods=["DELETE"])
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
    
    
@books_bp.route("/<int:book_id>/reviews/<int:review_id>", methods=["PUT", "PATCH"])
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
    
          
