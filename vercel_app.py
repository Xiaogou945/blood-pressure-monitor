from app import app, db
import os

def init_db():
    try:
        with app.app_context():
            db.create_all()
            print("Database initialized successfully")
    except Exception as e:
        print(f"Error initializing database: {str(e)}")

# Initialize the database when the application starts
init_db()

# Vercel expects an "app" object
application = app
