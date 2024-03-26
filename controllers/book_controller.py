from flask import Blueprint, request
from init import db
from models.book import Book, books_schema, book_schema
from models.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity
from controllers.review_controller import reviews_bp

books_bp = Blueprint('books', __name__, url_prefix='/books')
books_bp.register_blueprint(reviews_bp)

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
    body_data = book_schema.load(request.get_json())

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
@jwt_required()

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
@jwt_required()
def update_book(book_id):
    body_data = book_schema.load(request.get_json(), partial=True)
    stmt = db.select(Book).filter_by(id=book_id)
    book = db.session.scalar(stmt)
    if book:
        if str(book.user.id) != get_jwt_identity():
            return {"error": "Not allowed."}, 403
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
    

# def is_user_admin():
#     user_id = get_jwt_identity()
#     stmt = db.select(User).filter_by(id=user_id)
#     user = db.session.scalar(stmt)
#     return user.is_admin

