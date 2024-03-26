from init import db, ma 
from marshmallow import fields
from marshmallow.validate import Length, OneOf
from marshmallow.exceptions import ValidationError

VALID_STATUSES =('Read', 'Not Read', 'Currently reading')
class Book(db.Model):
    __tablename__= "books"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    author = db.Column(db.String(100))
    pagecount = db.Column(db.Integer)
    status = db.Column(db.String(100))
    review = db.Column(db.Text)
    genre = db.Column(db.String(100))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', back_populates='books')
    reviews = db.relationship('Review', back_populates='book', cascade='all, delete')



class BookSchema(ma.Schema):
    
    title = fields.String(required=True, validate=Length(min=2, error="Title must be at least 2 characters long.")


    )
    status = fields.String(Validate=OneOf(VALID_STATUSES))
    

    user = fields.Nested('UserSchema', only = ['username'])
    comments = fields.List(fields.Nested('ReviewSchema'))
    

    class Meta:
        fields = ('id', 'title', 'author', 'pagecount', 'status', 'review', 'genre', 'user')
        ordered=True
            
book_schema = BookSchema()
books_schema = BookSchema(many=True)

