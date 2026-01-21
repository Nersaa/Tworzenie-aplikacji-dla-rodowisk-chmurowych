from app import create_app, db
from app.models import Author, Book, Person, Borrowing, Review
from datetime import datetime, timedelta

app = create_app()

with app.app_context():
    print('Adding test data...')

    # Add Authors (ensure unique names, or handle duplicates)
    authors_data = {
        'George Orwell': None,
        'Aldous Huxley': None,
        'Jane Austen': None,
        'George R.R. Martin': None,
        'J.R.R. Tolkien': None,
        'C.S. Lewis': None,
        'Agatha Christie': None
    }
    for name in authors_data:
        author = Author.query.filter_by(name=name).first()
        if not author:
            author = Author(name=name)
            db.session.add(author)
        authors_data[name] = author
    db.session.commit()
    print(f'Added {Author.query.count()} authors.')

    # Add Persons
    persons_data = {
        'Alice Smith': None,
        'Bob Johnson': None,
        'Charlie Brown': None,
        'Diana Prince': None,
        'Eve Adams': None
    }
    for name in persons_data:
        person = Person.query.filter_by(name=name).first()
        if not person:
            person = Person(name=name)
            db.session.add(person)
        persons_data[name] = person
    db.session.commit()
    print(f'Added {Person.query.count()} persons.')

    # Add Books
    books_data = [
        {'title': '1984', 'author': 'George Orwell', 'year': 1949},
        {'title': 'Animal Farm', 'author': 'George Orwell', 'year': 1945},
        {'title': 'Brave New World', 'author': 'Aldous Huxley', 'year': 1932},
        {'title': 'Pride and Prejudice', 'author': 'Jane Austen', 'year': 1813},
        {'title': 'A Game of Thrones', 'author': 'George R.R. Martin', 'year': 1996},
        {'title': 'A Clash of Kings', 'author': 'George R.R. Martin', 'year': 1998},
        {'title': 'The Hobbit', 'author': 'J.R.R. Tolkien', 'year': 1937},
        {'title': 'The Lord of the Rings', 'author': 'J.R.R. Tolkien', 'year': 1954},
        {'title': 'The Chronicles of Narnia', 'author': 'C.S. Lewis', 'year': 1950},
        {'title': 'And Then There Were None', 'author': 'Agatha Christie', 'year': 1939}
    ]
    for book_info in books_data:
        author_obj = authors_data[book_info['author']]
        book = Book.query.filter_by(title=book_info['title'], author_id=author_obj.id).first()
        if not book:
            book = Book(title=book_info['title'], author_id=author_obj.id, publication_year=book_info['year'])
            db.session.add(book)
    db.session.commit()
    # Fetch all books again to ensure we have their IDs for reviews
    all_books = {b.title: b for b in Book.query.all()}
    print(f'Added {Book.query.count()} books.')

    # Add Borrowings (ensure unique, or handle duplicates if re-running)
    # Alice borrows 1984
    book1984 = all_books.get('1984')
    alice = persons_data.get('Alice Smith')
    if book1984 and alice and not Borrowing.query.filter_by(book_id=book1984.id, person_id=alice.id).first():
        borrowing1 = Borrowing(book_id=book1984.id, person_id=alice.id, borrow_date=datetime.utcnow() - timedelta(days=7))
        db.session.add(borrowing1)

    # Bob borrows Brave New World
    bookBraveNewWorld = all_books.get('Brave New World')
    bob = persons_data.get('Bob Johnson')
    if bookBraveNewWorld and bob and not Borrowing.query.filter_by(book_id=bookBraveNewWorld.id, person_id=bob.id).first():
        borrowing2 = Borrowing(book_id=bookBraveNewWorld.id, person_id=bob.id, borrow_date=datetime.utcnow() - timedelta(days=3))
        db.session.add(borrowing2)

    db.session.commit()
    print(f'Added {Borrowing.query.count()} borrowings.')

    # Add Reviews
    review_data = [
        {'book': '1984', 'person': 'Alice Smith', 'rating': 5, 'comment': 'A timeless classic, thought-provoking and disturbing.'},
        {'book': 'Animal Farm', 'person': 'Bob Johnson', 'rating': 4, 'comment': 'A powerful allegory.'},
        {'book': 'Brave New World', 'person': 'Alice Smith', 'rating': 4, 'comment': 'Fascinating vision of a dystopian future.'},
        {'book': 'The Hobbit', 'person': 'Charlie Brown', 'rating': 5, 'comment': 'An amazing adventure, perfect for all ages.'},
        {'book': 'Pride and Prejudice', 'person': 'Diana Prince', 'rating': 5, 'comment': 'A delightful read with great characters.'},
        {'book': 'A Game of Thrones', 'person': 'Eve Adams', 'rating': 4, 'comment': 'Epic fantasy, very engaging storyline.'}
    ]

    for review_info in review_data:
        book_obj = all_books.get(review_info['book'])
        person_obj = persons_data.get(review_info['person'])
        if book_obj and person_obj:
            # Check if review already exists to avoid duplicates if script is run multiple times
            existing_review = Review.query.filter_by(book_id=book_obj.id, person_id=person_obj.id).first()
            if not existing_review:
                review = Review(book_id=book_obj.id, person_id=person_obj.id, 
                                rating=review_info['rating'], comment=review_info['comment'])
                db.session.add(review)
    db.session.commit()
    print(f'Added {Review.query.count()} reviews.')

    print('Test data added successfully!') 