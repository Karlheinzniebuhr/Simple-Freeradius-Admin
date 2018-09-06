import sys

sys.path.append('/var/www/flask/Simple-Freeradius-Admin/')

from SimpleAdmin import app as application

if __name__ == "__main__":
	application.run()
