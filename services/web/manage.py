# configure the Flask CLI tool to run and manage the app from the command line
from flask.cli import FlaskGroup

from project import app

#  create a new FlaskGroup extend the normal CLI with commands related to the Flask app
cli = FlaskGroup(app)


if __name__ == "__main__":
    cli()
