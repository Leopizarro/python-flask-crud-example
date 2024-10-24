# python-flask-crud-example

Backend built with Python/flask.

This app was built to practice programming with Python/Flask specifically.

The app consists of a backend that stores projects information, which can include different categories and milestones associated. Milestones have importance and stages.

# How to run the app:

To set up the database, run: flask --app flaskr init-db

(make sure that you run the command from above to initialize de db, before running the app)

(running the init-db command when there's already a db created will delete the current db and create a new one)

To run the app, run: flask --app flaskr run --debug


# Run the app with Docker:

first initialize the sqlite database: flask --app flaskr init-db

then run the docker compose command: docker compose up -d --build



