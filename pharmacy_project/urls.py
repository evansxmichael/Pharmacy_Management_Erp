"""
==========================================
MAIN URL DISPATCHER (The Highway)
==========================================
This file acts as the primary gatekeeper for the entire application.
It does not handle business logic or HTML rendering. Instead, it looks 
at the URL the user is requesting and routes them to the correct app folder.

For this pharmacy system, all standard web traffic is routed directly 
to the 'store' app's internal URL configuration.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # ==========================================
    # 1. DJANGO ADMIN PANEL
    # ==========================================
    path('admin/', admin.site.urls),
    
    # ==========================================
    # 2. MAIN PHARMACY APPLICATION
    # ==========================================
    # This catches all standard traffic (e.g., yourwebsite.com/) 
    # and forwards it to the 'store/urls.py' file to handle the specific pages.
    path('', include('store.urls')), 
]

# Admin Panel Custom Branding
admin.site.site_header = "Pharmacy Management ERP"
admin.site.site_title = "Pharmacy Management ERP"
admin.site.index_title = "Pharmacy ERP Administration"