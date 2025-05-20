from website import create_app, db

myapp=create_app()


if __name__ == '__main__':
    # Run the Flask application
    with myapp.app_context():
        # Create the database tables
        db.create_all()
        myapp.run(debug=True)