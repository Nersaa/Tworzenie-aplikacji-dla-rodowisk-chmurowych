from app import db
from datetime import datetime

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    borrowings = db.relationship('Borrowing', backref='borrower', lazy=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'<Person {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.isoformat()
        } 