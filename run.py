from app import create_app, db
from datetime import datetime

app = create_app()

@app.context_processor
def inject_now():
    return {'now': datetime.now()}

@app.cli.command("init-db")
def init_db():
    """Initialize the database."""
    db.create_all()
    print('Initialized the database.')

if __name__ == '__main__':
    app.run(debug=True) 