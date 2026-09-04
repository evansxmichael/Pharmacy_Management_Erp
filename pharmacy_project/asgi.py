"""
==========================================
ASGI CONFIGURATION (Asynchronous Server)
==========================================
ASGI (Asynchronous Server Gateway Interface) is the modern, async-capable 
successor to WSGI. 

While our current pharmacy system operates synchronously, this file future-proofs 
the architecture. If we ever want to add real-time features (like live WebSockets, 
instant chat, or background hardware tasks), the server (like Daphne or Uvicorn) 
will use this file to handle those concurrent connections.

DO NOT modify this file unless implementing Django Channels or WebSockets.
"""

import os
from django.core.asgi import get_asgi_application

# Points the async server to our master settings file
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pharmacy_project.settings')

# Exposes the ASGI callable as a module-level variable named ``application``.
application = get_asgi_application()