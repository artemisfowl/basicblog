#!/usr/bin/env python

from app import application

def main():
	application.run(host="0.0.0.0", use_reloader=True)
	return 0

if __name__ == "__main__":
	main()
