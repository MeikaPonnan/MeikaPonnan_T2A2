from flask import Blueprint
from init import db, bcrypt 
from models.user import User
from models.book import Book
from models.review import Review


db_commands = Blueprint('db', __name__)

@db_commands.cli.command('create')
def create_tables():
    db.create_all()
    print("Tables created")


@db_commands.cli.command('drop')
def drop_tables():
    db.drop_all()
    print("Tables dropped")

@db_commands.cli.command('seed')
def seed_tables():
    users = [
        User(
            email="admin@email.com",
            password=bcrypt.generate_password_hash('123456').decode('utf-8'),is_admin=True
        ),
        User(
            username="User 1",
            email="user1@email.com",
            password=bcrypt.generate_password_hash('123456').decode('utf-8')
        )
    ]

    db.session.add_all(users)

    books = [
        Book(
            title="Book 1",
            author="author 1",
            pagecount="400",
            status="Read",
            review="long text",
            genre="Fantasy",
            user=users[0]
        ),

        Book(
            title="Book 2",
            author="author 2",
            pagecount="300",
            status="Read",
            review="long text",
            genre="Sci-fi",
            user=users[0]

        ),

        Book(
            title="Book 3",
            author="author 3",
            pagecount="300",
            status="Read",
            review="long text",
            genre="Sci-fi",
            user=users[1]
        ),

        Book(
            title="Book 4",
            author="author 4",
            pagecount="300",
            status="Read",
            review="long text",
            genre="Sci-fi",
            user=users[1]
        ),

    ]

    db.session.add_all(books)

    reviews = [
        Review(
            rating="5",
            comment="message",
            user=users[0],
            book=books[0]

        ),
        Review(
            rating="4",
            comment="message long",
            user=users[0],
            book=books[3]
        ),
        Review(
            rating="4.5",
            comment="message1",
            user=users[1],
            book=books[2]
            
        ),

        Review(
            rating="3",
            comment="message2",
            user=users[1],
            book=books[3]
        ),

    ]


    db.session.commit()

    print("Tables seeded")
