from init import db, ma 
from marshmallow import fields


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
    reviews = db.relationship('Review', back_populates='book')



class BookSchema(ma.Schema):

    user = fields.Nested('UserSchema', only = ['username'])
    comments = fields.List(fields.Nested('ReviewSchema'))
    

    class Meta:
        fields = ('id', 'title', 'author', 'pagecount', 'status', 'review', 'genre', 'user')
        ordered=True
            
book_schema = BookSchema()
books_schema = BookSchema(many=True)

