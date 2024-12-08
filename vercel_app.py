from app import app, db

# Initialize the database
with app.app_context():
    db.create_all()

# Vercel expects an "app" object
app = app
