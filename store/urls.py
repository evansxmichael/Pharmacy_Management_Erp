from django.urls import path
from . import views

# ==========================================
# URL ROUTER (The Application Map)
# ==========================================
# This file connects specific web addresses (URLs) to their corresponding 
# Python functions in views.py. The 'name' parameter allows us to dynamically 
# link to these pages in our HTML templates using {% url 'name_here' %}.

urlpatterns = [
    
    # ------------------------------------------
    # 1. AUTHENTICATION ROUTES
    # ------------------------------------------
    path('login/', views.login_view, name='login'),      
    path('logout/', views.logout_view, name='logout'),   

    # ------------------------------------------
    # 2. CORE DASHBOARDS & UI PAGES
    # ------------------------------------------
    # The empty string '' means this is the homepage / default route
    path('', views.billing, name='billing'),
    path('inventory/', views.inventory_dashboard, name='inventory'),
    path('analytics/', views.analytics_dashboard, name='analytics'),
    path('crm/', views.crm_dashboard, name='crm'),
    
    # ------------------------------------------
    # 3. REVERSE LOGISTICS (RETURNS & EXCHANGES)
    # ------------------------------------------
    # Scans bill barcodes, verifies sales, and handles refunds/restocking
    path('returns/', views.returns_view, name='returns'),

    # ------------------------------------------
    # 4. DATA ENTRY ROUTES
    # ------------------------------------------
    path('add-stock/', views.add_stock, name='add_stock'),

    # ------------------------------------------
    # 5. BACKGROUND API & AJAX ENDPOINTS
    # ------------------------------------------
    # These routes don't load full HTML pages. They are used by JavaScript 
    # to fetch or submit data silently in the background without reloading the screen.
    path('ajax-add-medicine/', views.ajax_add_medicine, name='ajax_add_medicine'),
    path('ajax-add-supplier/', views.ajax_add_supplier, name='ajax_add_supplier'),
    path('api/get_customer/', views.get_customer, name='get_customer'),
    
]