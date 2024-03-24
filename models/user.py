from init import db, ma 
from marshmallow import fields


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=True)
    is_admin = db.Column(db.Boolean, default=False)

    books = db.relationship('Book', back_populates='user', cascade='all, delete')


class UserSchema(ma.Schema):

    books = fields.List(fields.Nested('BookSchema', exclude=['user']))
    class Meta:
        fields = ('id', 'username', 'email', 'password', 'is_admin', 'books')

user_schema = UserSchema(exclude=['password'])
users_schema = UserSchema(many=True, exclude=['password'])
