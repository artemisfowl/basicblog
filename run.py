#!/usr/bin/env python

from app import application

# fixme: import the application from the init python file under app module

# fixme: add the code for setting up the right page to the user

def main():
	application.run(host="0.0.0.0", debug=True)
	return 0

if __name__ == "__main__":
	main()
