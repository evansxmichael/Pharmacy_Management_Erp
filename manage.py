#!/usr/bin/env python
"""
==========================================
DJANGO MANAGEMENT SCRIPT (manage.py)
==========================================
This is the command-line utility for administrative tasks.
It acts as the entry point for running the development server, 
making database migrations, and executing other Django commands.

DO NOT modify the core logic of this file.
"""
import os
import sys

def main():
    """
    Initializes the Django environment and executes command-line tasks.
    """
    # This line tells Django exactly where to find your project's main settings file
    # so it knows how to connect to the database, load apps, etc.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pharmacy_project.settings')
    
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
        
    # This takes whatever you typed in the terminal (e.g., 'runserver') 
    # and actually executes it.
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()