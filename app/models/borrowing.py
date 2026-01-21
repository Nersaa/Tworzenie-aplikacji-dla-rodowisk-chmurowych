from app import db
from datetime import datetime

class Borrowing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
    borrow_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    return_date = db.Column(db.DateTime, nullable=True)

    book = db.relationship('Book', backref='borrowings')
    person = db.relationship('Person')

    def __init__(self, book_id, person_id, borrow_date=None):
        self.book_id = book_id
        self.person_id = person_id
        if borrow_date is None:
            self.borrow_date = datetime.utcnow()
        else:
            self.borrow_date = borrow_date

    def __repr__(self):
        return f'<Borrowing {self.book_id} by {self.person_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'book_id': self.book_id,
            'person_id': self.person_id,
            'borrow_date': self.borrow_date.isoformat() if self.borrow_date else None,
            'return_date': self.return_date.isoformat() if self.return_date else None
        } 