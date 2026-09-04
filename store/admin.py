from django.contrib import admin
from .models import Supplier, Medicine, Stock, Sale, Customer, ReturnSale

# ==========================================
# 1. SUPPLIER ADMIN
# ==========================================
@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    """
    Controls the UI for the Supplier table in the Django Admin panel.
    """
    # list_display: Decides which columns appear in the main data table
    list_display = ('name', 'contact_person', 'phone')
    
    # search_fields: Adds a search bar at the top to look up these specific fields
    search_fields = ('name', 'phone')


# ==========================================
# 2. MEDICINE ADMIN (Product Catalog)
# ==========================================
@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    """
    Manages the general medicine catalog UI.
    """
    # Notice we include 'total_stock' here! Django is smart enough to pull
    # the @property we defined in models.py and display it as a column.
    list_display = ('name', 'category', 'manufacturer', 'minimum_stock_level', 'total_stock')
    
    search_fields = ('name', 'category', 'manufacturer')
    
    # list_filter: Adds a sidebar box allowing you to click and filter by category
    list_filter = ('category',)


# ==========================================
# 3. STOCK ADMIN (Physical Inventory)
# ==========================================
@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    """
    Manages the physical batches of medicine. This view is crucial for 
    the Boss to check exactly what is expiring and when.
    """
    list_display = ('medicine', 'batch_no', 'quantity', 'mrp', 'expiry_date', 'supplier')
    
    # Notice the double underscore in 'medicine__name'. 
    # This tells Django to search the related Medicine table's 'name' field!
    search_fields = ('medicine__name', 'batch_no')
    
    # Filters allow the Boss to quickly find stock from a specific supplier
    list_filter = ('expiry_date', 'supplier')
    
    # date_hierarchy: Adds a cool clickable timeline navigation bar at the top of the screen
    date_hierarchy = 'expiry_date'


# ==========================================
# 4. SALE ADMIN (Transaction Logs)
# ==========================================
@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    """
    Manages the financial transaction logs. Kept read-only for cashiers, 
    but the Boss can view and filter history here.
    """
    # Added bill_no and payment_method so receipt barcodes can be audited
    list_display = ('bill_no', 'stock', 'quantity', 'total_price', 'payment_method', 'date')
    search_fields = ('bill_no', 'stock__medicine__name')
    list_filter = ('date', 'payment_method')
    date_hierarchy = 'date'


# ==========================================
# 5. RETURN SALE ADMIN (Reverse Logistics Log)
# ==========================================
@admin.register(ReturnSale)
class ReturnSaleAdmin(admin.ModelAdmin):
    """
    Manages returned items, restocking status, and refund amounts.
    """
    list_display = ('sale', 'stock', 'quantity_returned', 'refund_amount', 'reason', 'restocked', 'returned_at')
    list_filter = ('reason', 'restocked', 'returned_at')
    search_fields = ('sale__bill_no', 'stock__medicine__name')
    date_hierarchy = 'returned_at'


# ==========================================
# 6. CUSTOMER ADMIN (Patient Directory)
# ==========================================
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """
    Allows the Boss to manage patient data, edit phone numbers, or track
    which doctor prescribed their last medication directly from the backend.
    """
    list_display = ('name', 'phone', 'last_doctor')
    search_fields = ('name', 'phone')