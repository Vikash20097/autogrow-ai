from app import create_app
import os

app = create_app()

if __name__ == "__main__":
    # Auto-create database tables
    with app.app_context():
        from app import db
        db.create_all()
    
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
