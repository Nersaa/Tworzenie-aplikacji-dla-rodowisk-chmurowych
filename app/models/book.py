from app import db
from datetime import datetime
from app.models.author import Author # Import the Author model

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    publication_year = db.Column(db.Integer, nullable=False)

    # Add foreign key to author
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, title, author_id, publication_year):
        self.title = title
        self.author_id = author_id
        self.publication_year = publication_year

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author.name, # Access the author's name via the relationship
            'publication_year': self.publication_year,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    @staticmethod
    def validate_publication_year(year):
        current_year = datetime.now().year
        return 1800 <= year <= current_year

    def __repr__(self):
        return f'<Book {self.title}>' 