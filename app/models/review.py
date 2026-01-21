from app import db
from datetime import datetime

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False) # e.g., 1-5 stars
    comment = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    book = db.relationship('Book', backref=db.backref('reviews', cascade="all, delete-orphan"))
    person = db.relationship('Person', backref=db.backref('reviews', cascade="all, delete-orphan"))

    def __init__(self, book_id, person_id, rating, comment=None):
        self.book_id = book_id
        self.person_id = person_id
        self.rating = rating
        self.comment = comment

    def __repr__(self):
        return f'<Review for Book {self.book_id} by Person {self.person_id} - Rating: {self.rating}>'

    def to_dict(self):
        return {
            'id': self.id,
            'book_id': self.book_id,
            'person_id': self.person_id,
            'rating': self.rating,
            'comment': self.comment,
            'created_at': self.created_at.isoformat()
        } 