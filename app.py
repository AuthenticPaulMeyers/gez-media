from website import create_app, db

myapp=create_app()


if __name__ == '__main__':
    # Run the Flask application
        myapp.run(debug=True)