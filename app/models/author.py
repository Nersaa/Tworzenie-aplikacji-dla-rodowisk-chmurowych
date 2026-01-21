from app import db

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    books = db.relationship('Book', backref='author', lazy=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'<Author {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        } 