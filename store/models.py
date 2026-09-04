from django.db import models
from django.utils import timezone
import datetime
from django.db.models.signals import post_delete
from django.dispatch import receiver


# ==========================================
# 1. SUPPLIER MODEL (The Wholesalers)
# ==========================================
class Supplier(models.Model):
    """
    Stores information about the wholesalers or distributors 
    from whom the medical store purchases inventory.
    """
    name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField()

    def __str__(self):
        return self.name


# ==========================================
# 2. MEDICINE MODEL (The Product Catalog)
# ==========================================
class Medicine(models.Model):
    """
    Represents the general catalog of medicines. 
    This does not track individual physical boxes (that is handled by the Stock model).
    """
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=200, blank=True, null=True)
    minimum_stock_level = models.IntegerField(default=10, help_text="Alert when total stock drops below this quantity")
    gst_percentage = models.IntegerField(default=12, help_text="GST % (e.g., 5, 12, 18)") 
    barcode = models.CharField(max_length=100, unique=True, null=True, blank=True)
    pack_size = models.CharField(max_length=50, default="10 Tabs")

    def __str__(self):
        return self.name

    @property
    def total_stock(self):
        """
        Dynamically calculates total strips/bottles across ALL active batches 
        for this specific medicine by aggregating the related Stock models.
        """
        return sum(stock.quantity for stock in self.stock_set.all())


# ==========================================
# 3. STOCK MODEL (Physical Inventory / Batches)
# ==========================================
class Stock(models.Model):
    """
    Represents a specific physical batch of a medicine purchased from a supplier.
    Crucial for FEFO (First Expire, First Out) tracking and profit calculation.
    """
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True)
    batch_no = models.CharField(max_length=50)
    expiry_date = models.DateField()
    quantity = models.IntegerField()
    purchase_price = models.FloatField(help_text="Price per unit from the supplier")
    mrp = models.FloatField(help_text="Maximum Retail Price (Selling price per unit)")
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.medicine.name} - Batch: {self.batch_no}"

    @property
    def is_expired(self):
        return self.expiry_date < datetime.date.today()

    @property
    def expires_soon(self):
        return self.expiry_date <= datetime.date.today() + datetime.timedelta(days=30)


# ==========================================
# 4. SALE MODEL (Transaction Records)
# ==========================================
class Sale(models.Model):
    """
    Records individual units sold. Used to generate financial analytics, 
    track daily revenue, and print customer bills.
    """
    # Bill number enables receipt barcode scanning for returns
    bill_no = models.CharField(max_length=50, null=True, blank=True, db_index=True)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    total_price = models.FloatField()

    customer = models.ForeignKey(
        'Customer', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='purchase_history'
    )
    
    PAYMENT_CHOICES = [
        ('Cash', 'Cash'),
        ('UPI', 'UPI'),
    ]
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default='Cash')

    def __str__(self):
        if self.stock and self.stock.medicine:
            customer_name = self.customer.name if self.customer else "Guest"
            bill_tag = f"[{self.bill_no}] " if self.bill_no else ""
            return f"{bill_tag}Sale: {self.stock.medicine.name} x {self.quantity} (Buyer: {customer_name})"
        return f"Legacy Test Sale x {self.quantity}"


# ==========================================
# 5. RETURN SALE MODEL (Audit & Reverse Logistics)
# ==========================================
class ReturnSale(models.Model):
    """
    Tracks returned or exchanged items from customer receipts.
    Ensures an audit trail is maintained without corrupting past sales records.
    """
    RETURN_REASONS = [
        ('WRONG_ITEM', 'Wrong Item Purchased'),
        ('DEFECTIVE', 'Damaged / Defective Seal'),
        ('EXCESS', 'Prescription Changed / Excess Medicine'),
    ]

    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='returns')
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    quantity_returned = models.PositiveIntegerField(default=1)
    refund_amount = models.FloatField(help_text="Amount returned to customer")
    reason = models.CharField(max_length=50, choices=RETURN_REASONS, default='WRONG_ITEM')
    restocked = models.BooleanField(default=True, help_text="Checked if units were returned to stock shelf")
    returned_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Return for Bill {self.sale.bill_no} - {self.stock.medicine.name} (x{self.quantity_returned})"


# ==========================================
# 6. CUSTOMER MODEL (Patient Directory / CRM)
# ==========================================
class Customer(models.Model):
    """
    Patient directory for maintaining relationships, tracking returning customers, 
    and associating them with previous doctors and prescriptions.
    """
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, unique=True)
    last_doctor = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.phone})"


# ==========================================
# 7. DJANGO SIGNALS (Automated Triggers)
# ==========================================
@receiver(post_delete, sender=Sale)
def restore_stock_on_sale_delete(sender, instance, **kwargs):
    """
    BACKGROUND AUTOMATION: Listens for any 'Sale' record being deleted.
    If a sale is canceled or reversed, it automatically fetches the exact 
    batch from the database and returns the sold quantity back to the inventory.
    """
    if instance.stock:
        stock = Stock.objects.get(id=instance.stock.id)
        stock.quantity += instance.quantity
        stock.save()