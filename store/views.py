# ==========================================
# IMPORTS & SETUP
# ==========================================
import random
import csv
from datetime import date, timedelta, datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required

from django.db import transaction
from django.db.models import Sum, F
from django.http import HttpResponse, JsonResponse

from .models import Medicine, Supplier, Stock, Sale, Customer, ReturnSale


@login_required(login_url='login')
def billing(request):
    is_manager_or_boss = request.user.is_superuser or request.user.groups.filter(name='Manager').exists()
    medicines = Medicine.objects.all()
    
    if 'cart' not in request.session:
        request.session['cart'] = []
    cart = request.session['cart']

    if request.method == 'POST':
        action = request.POST.get('action')
        
        # 1. MANUAL ADD TO CART
        if action == 'add':
            med_id = int(request.POST.get('medicine'))
            qty = int(request.POST.get('quantity'))
            medicine = Medicine.objects.filter(id=med_id).first()
            
            available_batches = Stock.objects.filter(medicine=medicine, quantity__gt=0).order_by('expiry_date')
            total_available_stock = sum(batch.quantity for batch in available_batches)

            if total_available_stock >= qty:
                first_batch_mrp = available_batches.first().mrp
                item_exists = False
                
                for item in cart:
                    if item['id'] == medicine.id:
                        if item['qty'] + qty <= total_available_stock:
                            item['qty'] += qty
                            item['total'] = item['qty'] * first_batch_mrp  
                            item_exists = True
                            messages.success(request, f"Updated cart: {item['qty']}x {medicine.name}.")
                        else:
                            messages.error(request, f"Cannot add more! Only {total_available_stock} units left.")
                            item_exists = True
                        break
                        
                if not item_exists:
                    cart.append({
                        'id': medicine.id,
                        'name': medicine.name,
                        'pack_size': medicine.pack_size,
                        'qty': qty,
                        'price': first_batch_mrp,  
                        'total': first_batch_mrp * qty  
                    })
                    messages.success(request, f"Added {qty}x {medicine.name} to cart.")
                    
                request.session['cart'] = cart
                request.session.modified = True
            else:
                messages.error(request, f"Insufficient stock! We only have {total_available_stock} units left.")
                
            return redirect('billing')
        
        # 2. BARCODE SCANNER ACTION
        elif action == 'scan':
            barcode_val = request.POST.get('barcode', '').strip()
            medicine = Medicine.objects.filter(barcode=barcode_val).first()
            
            if medicine:
                qty = 1
                available_batches = Stock.objects.filter(medicine=medicine, quantity__gt=0).order_by('expiry_date')
                total_available_stock = sum(batch.quantity for batch in available_batches)

                if total_available_stock >= qty:
                    first_batch_mrp = available_batches.first().mrp
                    item_exists = False
                    
                    for item in cart:
                        if item['id'] == medicine.id:
                            if item['qty'] + qty <= total_available_stock:
                                item['qty'] += qty
                                item['total'] = item['qty'] * first_batch_mrp  
                                item_exists = True
                                messages.success(request, f"Scanned! Updated cart: {item['qty']}x {medicine.name}.")
                            else:
                                messages.error(request, f"Cannot add more! Only {total_available_stock} units left.")
                                item_exists = True
                            break
                            
                    if not item_exists:
                        cart.append({
                            'id': medicine.id,
                            'name': medicine.name,
                            'qty': qty,
                            'price': first_batch_mrp,  
                            'total': first_batch_mrp * qty  
                        })
                        messages.success(request, f"Scanned! Added 1x {medicine.name} to cart.")
                        
                    request.session['cart'] = cart
                    request.session.modified = True
                else:
                    messages.error(request, f"Scan Failed: Insufficient stock for {medicine.name}!")
            else:
                messages.error(request, "Barcode not recognized in the system!")
                
            return redirect('billing')
        
        # 3. REMOVE FROM CART ACTION
        elif action == 'remove':
            remove_id = int(request.POST.get('remove_id'))
            request.session['cart'] = [item for item in cart if item['id'] != remove_id]
            request.session.modified = True
            messages.info(request, "Item removed from the bill.")
            return redirect('billing')

        # 4. FINAL GENERATE BILL ACTION
        elif action == 'generate':
            if not cart:
                messages.warning(request, "Your cart is empty.")
                return redirect('billing')

            cust_name = request.POST.get('cust_name', '').strip()
            cust_mobile = request.POST.get('cust_mobile', '').strip()
            doc_name = request.POST.get('doc_name', '').strip()
            payment_method = request.POST.get('payment_method', 'Cash')
            
            # Generate the Bill Number BEFORE database persistence
            bill_number = f"15489WS{random.randint(1000, 9999)}"

            # 1. SMART CRM CAPTURE
            current_customer = None
            if cust_mobile and cust_name:
                current_customer, created = Customer.objects.update_or_create(
                    phone=cust_mobile,
                    defaults={'name': cust_name, 'last_doctor': doc_name}
                )

            total_amount = 0
            total_taxable_value = 0
            total_cgst = 0
            total_sgst = 0
            bill_items = []
            gst_summary_dict = {}

            try:
                with transaction.atomic():
                    for item in cart:
                        medicine = Medicine.objects.get(id=item['id'])
                        qty_to_fulfill = item['qty']

                        available_batches = Stock.objects.select_for_update().filter(
                            medicine=medicine, quantity__gt=0
                        ).order_by('expiry_date')

                        if sum(b.quantity for b in available_batches) < qty_to_fulfill:
                            raise ValueError(f"Transaction failed: Not enough total stock for {item['name']}.")

                        first_batch_used = None

                        # 2. THE FEFO DEDUCTION LOOP
                        for batch in available_batches:
                            if qty_to_fulfill <= 0:
                                break

                            if first_batch_used is None:
                                first_batch_used = batch

                            if batch.quantity >= qty_to_fulfill:
                                Sale.objects.create(
                                    bill_no=bill_number,
                                    stock=batch,
                                    quantity=qty_to_fulfill,
                                    total_price=(qty_to_fulfill * batch.mrp),
                                    customer=current_customer,
                                    payment_method=payment_method
                                )
                                batch.quantity -= qty_to_fulfill
                                batch.save()
                                qty_to_fulfill = 0 
                            else:
                                qty_taken = batch.quantity
                                Sale.objects.create(
                                    bill_no=bill_number,
                                    stock=batch,
                                    quantity=qty_taken,
                                    total_price=(qty_taken * batch.mrp),
                                    customer=current_customer,
                                    payment_method=payment_method
                                )
                                qty_to_fulfill -= qty_taken
                                batch.quantity = 0
                                batch.save()

                        # 3. GST & RECEIPT MATH
                        total_amount += item['total']
                        gst_rate = getattr(medicine, 'gst_percentage', 12) 
                        taxable_val = item['total'] / (1 + (gst_rate / 100))
                        gst_amt = item['total'] - taxable_val
                        cgst_amt = gst_amt / 2
                        
                        total_taxable_value += taxable_val
                        total_cgst += cgst_amt
                        total_sgst += cgst_amt
                        
                        if gst_rate not in gst_summary_dict:
                            gst_summary_dict[gst_rate] = {'taxable': 0, 'cgst': 0, 'sgst': 0}
                            
                        gst_summary_dict[gst_rate]['taxable'] += taxable_val
                        gst_summary_dict[gst_rate]['cgst'] += cgst_amt
                        gst_summary_dict[gst_rate]['sgst'] += cgst_amt
                        
                        bill_items.append({
                            'name': medicine.name,
                            'pack_size': item.get('pack_size', '1 Unit'),
                            'qty': item['qty'],
                            'price': first_batch_used.mrp,
                            'total': item['total'],
                            'batch': first_batch_used.batch_no,
                            'expiry': first_batch_used.expiry_date.strftime('%b-%y'), 
                            'mfg': medicine.manufacturer[:4].upper() if medicine.manufacturer else 'GEN',
                        })

                    gst_summary_list = [
                        {'rate': k, 'taxable': v['taxable'], 'cgst': v['cgst'], 'sgst': v['sgst']} 
                        for k, v in gst_summary_dict.items()
                    ]

                    request.session['cart'] = []
                    request.session.modified = True
                    messages.success(request, "Final bill generated successfully! Inventory secured via FEFO.")

                    return render(request, 'billing.html', {
                        'medicines': medicines,
                        'bill_items': bill_items,
                        'final_total': total_amount,
                        'cart': [],
                        'cart_total': 0,
                        'cust_name': cust_name,
                        'cust_mobile': cust_mobile,
                        'doc_name': doc_name,
                        'bill_no': bill_number,
                        'total_taxable_value': total_taxable_value,
                        'total_cgst': total_cgst,
                        'total_sgst': total_sgst,
                        'gst_summary': gst_summary_list,
                        'is_manager_or_boss': is_manager_or_boss
                    })

            except ValueError as e:
                messages.error(request, str(e))
                return redirect('billing')

    return render(request, 'billing.html', {
        'medicines': medicines,
        'cart': cart,
        'cart_total': sum(item['total'] for item in cart),
        'is_manager_or_boss': is_manager_or_boss
    })


# ==========================================
# 5. RETURN & SCAN WORKFLOW (NEW FEATURE)
# ==========================================
@login_required(login_url='login')
def returns_view(request):
    is_manager_or_boss = request.user.is_superuser or request.user.groups.filter(name='Manager').exists()
    scanned_bill_no = request.GET.get('bill_no', '').strip()
    bill_data = None

    # Step 1: Lookup by scanned barcode string
    if scanned_bill_no:
        sales_records = Sale.objects.filter(bill_no=scanned_bill_no).select_related('stock__medicine', 'customer')
        if sales_records.exists():
            first_sale = sales_records.first()
            bill_data = {
                'bill_no': scanned_bill_no,
                'customer': first_sale.customer,
                'payment_method': first_sale.payment_method,
                'items': sales_records,
                'date': first_sale.date
            }
        else:
            messages.error(request, f"No sales found for Bill No: {scanned_bill_no}")

    # Step 2: Handle Item Return Submission
    if request.method == 'POST':
        sale_id = request.POST.get('sale_id')
        qty_to_return = int(request.POST.get('return_qty', 1))
        restock = request.POST.get('restock') == 'on'
        reason = request.POST.get('reason', 'WRONG_ITEM')

        sale_item = get_object_or_404(Sale, id=sale_id)

        if qty_to_return <= 0 or qty_to_return > sale_item.quantity:
            messages.error(request, "Invalid return quantity entered.")
            return redirect(f"/returns/?bill_no={sale_item.bill_no}")

        with transaction.atomic():
            # Calculate unit refund value
            unit_price = sale_item.total_price / sale_item.quantity
            refund_amount = unit_price * qty_to_return

            # 1. Log the audit return record
            ReturnSale.objects.create(
                sale=sale_item,
                stock=sale_item.stock,
                quantity_returned=qty_to_return,
                refund_amount=refund_amount,
                reason=reason,
                restocked=restock
            )

            # 2. Put units back on the shelf if checked
            if restock and sale_item.stock:
                stock_batch = sale_item.stock
                stock_batch.quantity += qty_to_return
                stock_batch.save()

            # 3. Deduct from original Sale record so Financial Analytics stay accurate
            sale_item.quantity -= qty_to_return
            sale_item.total_price -= refund_amount
            sale_item.save()

            messages.success(request, f"Returned {qty_to_return} units of {sale_item.stock.medicine.name}. Refund amount: ₹{refund_amount:.2f}")
            return redirect(f"/returns/?bill_no={sale_item.bill_no}")

    return render(request, 'returns.html', {
        'bill_data': bill_data,
        'scanned_bill_no': scanned_bill_no,
        'is_manager_or_boss': is_manager_or_boss
    })


# ==========================================
# 6. INVENTORY DASHBOARD
# ==========================================
@login_required(login_url='login')
def inventory_dashboard(request):
    is_manager_or_boss = request.user.is_superuser or request.user.groups.filter(name='Manager').exists()
    
    if not is_manager_or_boss:
        messages.error(request, "ACCESS DENIED: Cashiers cannot view the Inventory Command Center.")
        return redirect('billing')
        
    medicines = Medicine.objects.all()
    # select_related optimizes queries for foreign keys in the template
    stock_items = Stock.objects.select_related('medicine', 'supplier').order_by('expiry_date')
    
    today = date.today()
    thirty_days_from_now = today + timedelta(days=30)
    
    low_stock_medicines = [med for med in medicines if med.total_stock < med.minimum_stock_level]
    
    if request.GET.get('export') == 'po':
        response = HttpResponse(content_type='text/csv')
        filename = f"Purchase_Order_List_{today.strftime('%d_%b_%Y')}.csv"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        writer = csv.writer(response)
        writer.writerow(['Medicine Name', 'Category', 'Manufacturer', 'Current Stock', 'Minimum Required', 'Suggested Order Qty'])
        
        for med in low_stock_medicines:
            suggested_order = (med.minimum_stock_level - med.total_stock) + 20 
            writer.writerow([
                med.name, 
                med.category, 
                med.manufacturer if med.manufacturer else "N/A", 
                med.total_stock, 
                med.minimum_stock_level, 
                suggested_order
            ])
            
        return response

    # Split batches cleanly between active sellable stock and expired stock
    expired_stock = stock_items.filter(expiry_date__lte=today)
    expiring_soon = stock_items.filter(expiry_date__gt=today, expiry_date__lte=thirty_days_from_now)
    sellable_stock = stock_items.filter(expiry_date__gt=today)
    
    # Calculate valuation cleanly (sellable active stock vs expired loss)
    active_inventory_value = sum(item.quantity * item.mrp for item in sellable_stock)
    expired_loss_value = sum(item.quantity * item.mrp for item in expired_stock)
    
    context = {
        'medicines': medicines,
        'stock_items': stock_items,
        'low_stock_medicines': low_stock_medicines,
        'expired_stock': expired_stock,
        'expiring_soon': expiring_soon,
        'total_inventory_value': active_inventory_value,  # Matches the ₹15.32L active value in inventory.html
        'active_inventory_value': active_inventory_value,
        'expired_loss_value': expired_loss_value,
    }
    
    return render(request, 'inventory.html', context)

# ==========================================
# 7. ANALYTICS DASHBOARD
# ==========================================
@login_required(login_url='login')
def analytics_dashboard(request):
    is_manager_or_boss = request.user.is_superuser or request.user.groups.filter(name='Manager').exists()
    
    if not is_manager_or_boss:
        messages.error(request, "ACCESS DENIED: Cashiers cannot view Financial Analytics.")
        return redirect('billing')
    
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')
    
    today = date.today()
    if start_date_str and end_date_str:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        date_label = f"Filtered: {start_date.strftime('%d %b %Y')} to {end_date.strftime('%d %b %Y')}"
    else:
        start_date = today
        end_date = today
        date_label = "Today's Live Data"

    filtered_sales = Sale.objects.filter(date__date__gte=start_date, date__date__lte=end_date, stock__isnull=False, quantity__gt=0)
    
    total_cash = filtered_sales.filter(payment_method='Cash').aggregate(Sum('total_price'))['total_price__sum'] or 0
    total_upi = filtered_sales.filter(payment_method='UPI').aggregate(Sum('total_price'))['total_price__sum'] or 0
    
    total_revenue = filtered_sales.aggregate(total=Sum('total_price'))['total'] or 0.0
    total_cost = filtered_sales.annotate(
        cost=F('stock__purchase_price') * F('quantity')
    ).aggregate(total_cost=Sum('cost'))['total_cost'] or 0.0
    total_profit = total_revenue - total_cost

    top_sellers = filtered_sales.values(
        med_name=F('stock__medicine__name')
    ).annotate(total_qty=Sum('quantity')).order_by('-total_qty')[:5]

    chart_labels = [item['med_name'] for item in top_sellers]
    chart_data = [item['total_qty'] for item in top_sellers]
    
    detailed_sales = filtered_sales.order_by('-date')

    aggregated_sales = filtered_sales.values(
        medicine_name=F('stock__medicine__name')
    ).annotate(
        total_qty_sold=Sum('quantity'),
        total_revenue=Sum('total_price')
    ).order_by('-total_revenue')

    if request.GET.get('export') == 'csv':
        response = HttpResponse(content_type='text/csv')
        filename = f"Xishaan_Pharmacy_Sales_{start_date.strftime('%Y%m%d')}_to_{end_date.strftime('%Y%m%d')}.csv"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        writer = csv.writer(response)
        writer.writerow(['Bill No', 'Date & Time', 'Medicine Name', 'Batch No', 'Quantity Sold', 'Total Revenue (INR)'])
        
        for sale in detailed_sales:
            formatted_date = sale.date.strftime("%d-%m-%Y %H:%M")
            writer.writerow([
                sale.bill_no or 'N/A',
                formatted_date, 
                sale.stock.medicine.name, 
                sale.stock.batch_no, 
                sale.quantity, 
                sale.total_price
            ])
            
        return response 

    context = {
        'todays_revenue': total_revenue, 
        'todays_profit': total_profit,
        'chart_labels': chart_labels,
        'chart_data': chart_data,
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d'),
        'date_label': date_label,
        'aggregated_sales': aggregated_sales,
        'total_cash': total_cash,
        'total_upi': total_upi,
    }
    
    return render(request, 'analytics.html', context)


# ==========================================
# 8. AUTHENTICATION VIEWS
# ==========================================
def login_view(request):
    if request.user.is_authenticated:
        return redirect('billing')

    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(request, username=u, password=p)
        
        if user is not None:
            auth_login(request, user)
            return redirect('billing')
        else:
            messages.error(request, "Invalid username or password.")
            
    return render(request, 'login.html')


def logout_view(request):
    auth_logout(request)
    return redirect('login')


# ==========================================
# 9. CRM DASHBOARD (Patient Directory)
# ==========================================
@login_required(login_url='login')
def crm_dashboard(request):
    customers = Customer.objects.prefetch_related(
        'purchase_history__stock__medicine'
    ).annotate(
        total_spent=Sum('purchase_history__total_price')
    ).order_by('-id')
    
    all_sales = Sale.objects.select_related('stock__medicine', 'customer').all().order_by('-date')

    context = {
        'customers': customers,
        'all_sales': all_sales
    }
    return render(request, 'crm.html', context)


# ==========================================
# 10. ADD STOCK (Data Entry)
# ==========================================
@login_required(login_url='login')
def add_stock(request):
    is_manager_or_boss = request.user.is_superuser or request.user.groups.filter(name='Manager').exists()
    
    if not is_manager_or_boss:
        messages.error(request, "ACCESS DENIED: Cashiers cannot add new stock.")
        return redirect('billing')

    if request.method == 'POST':
        medicine_id = request.POST.get('medicine_id')
        supplier_id = request.POST.get('supplier_id')
        batch_no = request.POST.get('batch_no')
        quantity = request.POST.get('quantity')
        purchase_price = request.POST.get('purchase_price')
        mrp = request.POST.get('mrp')
        expiry_date = request.POST.get('expiry_date')

        try:
            selected_medicine = Medicine.objects.get(id=medicine_id)
            selected_supplier = Supplier.objects.get(id=supplier_id)

            Stock.objects.create(
                medicine=selected_medicine,
                supplier=selected_supplier,
                batch_no=batch_no,
                quantity=quantity,
                purchase_price=purchase_price,
                mrp=mrp,
                expiry_date=expiry_date
            )
            
            messages.success(request, f"Successfully added {quantity} units of {selected_medicine.name} to inventory!")
            return redirect('inventory')

        except Exception as e:
            messages.error(request, f"Error adding stock: {str(e)}")

    medicines = Medicine.objects.all().order_by('name')
    suppliers = Supplier.objects.all().order_by('name')

    context = {
        'medicines': medicines,
        'suppliers': suppliers
    }
    return render(request, 'add_stock.html', context)


# ==========================================
# 11. BACKGROUND AJAX & API ENDPOINTS
# ==========================================
@login_required(login_url='login')
def ajax_add_medicine(request):
    if request.method == 'POST' and request.user.is_superuser:
        name = request.POST.get('name')
        category = request.POST.get('category', '')
        manufacturer = request.POST.get('manufacturer', '')
        min_stock = request.POST.get('minimum_stock_level', 10)
        gst = request.POST.get('gst_percentage', 12)
        barcode_val = request.POST.get('barcode', '').strip() or None
        
        try:
            med = Medicine.objects.create(
                name=name, category=category, manufacturer=manufacturer, 
                minimum_stock_level=min_stock, gst_percentage=gst, 
                barcode=barcode_val
            )
            return JsonResponse({'success': True, 'id': med.id, 'name': med.name})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})


@login_required(login_url='login')
def ajax_add_supplier(request):
    if request.method == 'POST' and request.user.is_superuser:
        name = request.POST.get('name')
        contact = request.POST.get('contact_person', '')
        phone = request.POST.get('phone', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address', '')
        
        try:
            sup = Supplier.objects.create(
                name=name, contact_person=contact, phone=phone, 
                email=email, address=address
            )
            return JsonResponse({'success': True, 'id': sup.id, 'name': sup.name})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})


@login_required(login_url='login')
def get_customer(request):
    phone = request.GET.get('phone', None)
    if phone:
        customer = Customer.objects.filter(phone=phone).first()
        if customer:
            return JsonResponse({
                'found': True,
                'name': customer.name,
                'doctor': customer.last_doctor
            })
    return JsonResponse({'found': False})