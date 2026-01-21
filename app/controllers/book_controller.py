from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.book import Book
from app.models.author import Author
from app.models.review import Review
from app.models.person import Person
from app import db

book_bp = Blueprint('book', __name__)

@book_bp.route('/')
def index():
    query = request.args.get('query')

    if query:
        # Perform search by book title or author name (case-insensitive)
        # We use outerjoin to include books even if they don't have an author (though our schema makes author required now)
        books = Book.query.join(Author).filter(
            (Book.title.ilike(f'%{query}%')) |
            (Author.name.ilike(f'%{query}%'))
        ).all()
    else:
        books = Book.query.all()

    return render_template('book_list.html', books=books, query=query)

@book_bp.route('/book/new', methods=['GET', 'POST'])
def new_book():
    if request.method == 'POST':
        title = request.form.get('title')
        author_name = request.form.get('author_name')
        publication_year = int(request.form.get('publication_year'))

        if not Book.validate_publication_year(publication_year):
            flash('Invalid publication year', 'error')
            return render_template('book_form.html') # No authors needed now

        # Check if author exists, otherwise create new
        author = Author.query.filter_by(name=author_name).first()
        if not author:
            author = Author(name=author_name)
            db.session.add(author)
            db.session.commit() # Commit to get author.id

        book = Book(title=title, author_id=author.id, publication_year=publication_year)
        db.session.add(book)
        db.session.commit()
        flash('Book added successfully!', 'success')
        return redirect(url_for('book.index'))

    return render_template('book_form.html')

@book_bp.route('/book/<int:id>/edit', methods=['GET', 'POST'])
def edit_book(id):
    book = Book.query.get_or_404(id)
    
    if request.method == 'POST':
        title = request.form.get('title') # Get title here
        author_name = request.form.get('author_name')
        publication_year = int(request.form.get('publication_year'))

        if not Book.validate_publication_year(publication_year):
            flash('Invalid publication year', 'error')
            return render_template('book_form.html', book=book) # No authors needed now
        
        # Check if author exists, otherwise create new
        author = Author.query.filter_by(name=author_name).first()
        if not author:
            author = Author(name=author_name)
            db.session.add(author)
            db.session.commit() # Commit to get author.id

        book.title = title
        book.author_id = author.id
        book.publication_year = publication_year

        db.session.commit()
        flash('Book updated successfully!', 'success')
        return redirect(url_for('book.index'))

    return render_template('book_form.html', book=book)

@book_bp.route('/book/<int:id>')
def book_detail(id):
    book = Book.query.get_or_404(id)
    reviews = Review.query.filter_by(book_id=book.id).order_by(Review.created_at.desc()).all()
    # We don't need to pass persons here anymore for the review form
    return render_template('book_detail.html', book=book, reviews=reviews)

@book_bp.route('/book/<int:id>/add_review', methods=['POST'])
def add_review(id):
    book = Book.query.get_or_404(id)
    rating = request.form.get('rating', type=int)
    comment = request.form.get('comment')
    person_name = request.form.get('person_name') # Get person name as text

    if not (1 <= rating <= 5):
        flash('Rating must be between 1 and 5.', 'error')
    elif not person_name:
        flash('Please provide your name for the review.', 'error')
    else:
        # Check if person exists, otherwise create new
        person = Person.query.filter_by(name=person_name).first()
        if not person:
            person = Person(name=person_name)
            db.session.add(person)
            db.session.commit() # Commit to get person.id

        # Check if the person has already reviewed this book
        existing_review = Review.query.filter_by(book_id=book.id, person_id=person.id).first()
        if existing_review:
            flash('You have already reviewed this book.', 'error')
        else:
            review = Review(book_id=book.id, person_id=person.id, rating=rating, comment=comment)
            db.session.add(review)
            db.session.commit()
            flash('Your review has been added!', 'success')
    
    return redirect(url_for('book.book_detail', id=book.id))

@book_bp.route('/book/<int:id>/delete', methods=['POST'])
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    flash('Book deleted successfully!', 'success')
    return redirect(url_for('book.index')) 