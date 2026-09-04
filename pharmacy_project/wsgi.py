"""
==========================================
WSGI CONFIGURATION (Synchronous Server)
==========================================
WSGI (Web Server Gateway Interface) is the standard standard Python specification 
for web servers and applications to communicate. 

When this project is deployed to a production environment (like AWS, Heroku, 
or a standard VPS using Gunicorn/Apache), the web server will look for the 
'application' callable inside this file to serve the Django project.

DO NOT modify this file unless implementing custom WSGI middleware.
"""

import os
from django.core.wsgi import get_wsgi_application

# Points the server to our master settings file so it knows how to configure the app
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pharmacy_project.settings')

# Exposes the WSGI callable as a module-level variable named ``application``.
application = get_wsgi_application()