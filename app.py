from website import create_app, db

myapp=create_app()


if __name__ == '__main__':
        # create the database
    with myapp.app_context():
        db.create_all()

    myapp.run(debug=True)