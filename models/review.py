from init import db, ma 
from marshmallow import fields

class Review(db.Model):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)
    comment = db.Column(db.Text)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False)

    user = db.relationship('User', back_populates='reviews')
    book = db.relationship('Book', back_populates='reviews')



class ReviewSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=['username'])
    book = fields.Nested('BookSchema', exclude=['reviews'])

    class Meta:
        fields = ('id', 'rating', 'comment', 'user', 'book')

review_schema = ReviewSchema()
reviews_schema= ReviewSchema(many=True)


