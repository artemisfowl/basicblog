#!/usr/bin/env python

from sys import version
from flask import __version__ as flask_version

from app import application

# fixme: import the application from the init python file under app module

# fixme: add the code for setting up the right page to the user

def main():
	print(f"Python version :{version}")
	print(f"Flask module version :{flask_version}")

	# start the server
	application.run(debug=True)

	return 0

if __name__ == "__main__":
	main()
