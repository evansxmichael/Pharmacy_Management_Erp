import os
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas

def generate_pdf():
    pdf_filename = "Pharmacy_Management_ERP_Major_Project.pdf"
    width = 13.333 * inch
    height = 7.5 * inch
    c = canvas.Canvas(pdf_filename, pagesize=(width, height))

    # Color Palette
    C_NAVY_BG = HexColor("#0c1f30")
    C_NAVY_CARD = HexColor("#14304a")
    C_LIGHT_BG = HexColor("#f4f7f6")
    C_WHITE = HexColor("#ffffff")
    C_TEAL = HexColor("#008b8b")
    C_TEAL_LIGHT = HexColor("#e0f2f1")
    C_CYAN = HexColor("#0ea5e9")
    C_DARK = HexColor("#1e293b")
    C_MUTED = HexColor("#64748b")
    C_BORDER = HexColor("#e2e8f0")
    C_GREEN = HexColor("#10b981")
    C_AMBER = HexColor("#f59e0b")
    C_RED = HexColor("#ef4444")

    def draw_slide_header(tag, title, slide_num):
        c.setFillColor(C_LIGHT_BG)
        c.rect(0, 0, width, height, fill=1, stroke=0)
        
        # Tag
        c.setFillColor(C_TEAL)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(0.8 * inch, height - 0.75 * inch, tag.upper())
        
        # Main Title
        c.setFillColor(C_DARK)
        c.setFont("Helvetica-Bold", 22)
        c.drawString(0.8 * inch, height - 1.15 * inch, title)

        # Number
        c.setFillColor(C_MUTED)
        c.setFont("Helvetica-Bold", 13)
        c.drawRightString(width - 0.8 * inch, height - 0.85 * inch, str(slide_num).zfill(2))

    # =========================================================================
    # SLIDE 1: TITLE SLIDE (Cover)
    # =========================================================================
    c.setFillColor(C_NAVY_BG)
    c.rect(0, 0, width, height, fill=1, stroke=0)

    # Decorative Badge
    c.setFillColor(C_TEAL)
    c.roundRect(0.8 * inch, height - 1.2 * inch, 2.0 * inch, 0.45 * inch, 4, fill=1, stroke=0)
    c.setFillColor(C_WHITE)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(1.8 * inch, height - 1.05 * inch, "MAJOR PROJECT")

    # Title & Subtitle
    c.setFont("Helvetica-Bold", 34)
    c.drawString(0.8 * inch, height - 2.0 * inch, "PHARMACY MANAGEMENT SYSTEM")

    c.setFillColor(C_CYAN)
    c.setFont("Helvetica", 17)
    c.drawString(0.8 * inch, height - 2.45 * inch, "A Centralized Web-Based ERP Platform for Retail Pharmacy Operations")

    # Divider
    c.setFillColor(HexColor("#1e415f"))
    c.rect(0.8 * inch, height - 2.8 * inch, width - 1.6 * inch, 0.04 * inch, fill=1, stroke=0)

    # Presenters Card
    c.setFillColor(C_NAVY_CARD)
    c.setStrokeColor(HexColor("#285073"))
    c.setLineWidth(1)
    c.roundRect(0.8 * inch, height - 5.5 * inch, 5.6 * inch, 2.4 * inch, 8, fill=1, stroke=1)

    c.setFillColor(C_TEAL_LIGHT)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(1.1 * inch, height - 3.4 * inch, "PRESENTED BY:")

    c.setFillColor(C_WHITE)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(1.1 * inch, height - 3.8 * inch, "• MD ZEESHAN  (Roll No: 23BTCS026HY)")
    c.drawString(1.1 * inch, height - 4.2 * inch, "• YUSUF HANZALA  (Roll No: 23BTCS005HY)")

    c.setFillColor(C_CYAN)
    c.setFont("Helvetica", 11)
    c.drawString(1.1 * inch, height - 4.7 * inch, "7th Semester, B.Tech Computer Science | Session 2026-27")

    # Supervisor Card
    c.setFillColor(C_NAVY_CARD)
    c.setStrokeColor(HexColor("#285073"))
    c.roundRect(6.8 * inch, height - 5.5 * inch, 5.7 * inch, 2.4 * inch, 8, fill=1, stroke=1)

    c.setFillColor(C_TEAL_LIGHT)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(7.1 * inch, height - 3.4 * inch, "UNDER THE SUPERVISION OF:")

    c.setFillColor(C_WHITE)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(7.1 * inch, height - 3.8 * inch, "Mrs. Nusrath Fathima")

    c.setFillColor(HexColor("#c8dcf0"))
    c.setFont("Helvetica", 11)
    c.drawString(7.1 * inch, height - 4.2 * inch, "Assistant Professor, Dept. of Computer Science & Information Technology")

    c.setFillColor(C_CYAN)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(7.1 * inch, height - 4.6 * inch, "Maulana Azad National Urdu University (MANUU), Hyderabad")

    # Footer
    c.setFillColor(HexColor("#8caac8"))
    c.setFont("Helvetica", 10)
    c.drawCentredString(width / 2.0, 0.7 * inch, "Centralized Web Architecture  |  FEFO Automated Inventory  |  Dynamic GST POS  |  Smart Patient CRM")
    c.showPage()

    # =========================================================================
    # SLIDE 2: INTRODUCTION
    # =========================================================================
    draw_slide_header("Introduction", "From Fragmented Operations to One Centralized Platform", 2)

    # Left Container
    c.setFillColor(C_WHITE)
    c.setStrokeColor(C_BORDER)
    c.roundRect(0.8 * inch, 0.8 * inch, 7.2 * inch, 5.2 * inch, 8, fill=1, stroke=1)

    bullets_s2 = [
        ("Interconnected Retail Nature", "Pharmacy retail operations naturally involve heavily interdependent processes — POS customer billing, batch inventory, drug procurement, reverse logistics, and tax analytics."),
        ("The Fragmented Reality", "Traditional retail pharmacies often rely on manual paper registers, standalone billing machines, or isolated desktop spreadsheets that fail to synchronize in real time."),
        ("Operational Bottlenecks", "This disconnection makes drug expiry tracking, low-stock reordering, reverse logistics, and overall profit auditing error-prone, laborious, and risky."),
        ("The Centralized ERP Solution", "Pharmacy Management ERP resolves this with a full-stack, cloud-hosted web system that consolidates all retail workflows into an integrated, real-time command platform."),
        ("Real-World Operational Alignment", "Purpose-built around real daily pharmacy workflows — including rapid barcode scanning, FEFO batch allocation, thermal receipts, and smart patient directories.")
    ]

    y_pos = height - 1.9 * inch
    for head, body in bullets_s2:
        c.setFillColor(C_DARK)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(1.1 * inch, y_pos, "• " + head + ": ")
        
        c.setFillColor(C_MUTED)
        c.setFont("Helvetica", 10.5)
        text_obj = c.beginText(1.1 * inch, y_pos - 0.22 * inch)
        text_obj.setFont("Helvetica", 10)
        text_obj.setFillColor(C_MUTED)
        text_obj.textLines(body)
        c.drawText(text_obj)
        y_pos -= 0.95 * inch

    # Right Container (The Shift)
    c.setFillColor(HexColor("#f1f8f8"))
    c.setStrokeColor(C_TEAL)
    c.roundRect(8.3 * inch, 0.8 * inch, 4.2 * inch, 5.2 * inch, 8, fill=1, stroke=1)

    c.setFillColor(C_TEAL)
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(10.4 * inch, height - 1.8 * inch, "THE OPERATIONAL SHIFT")

    items = ["Manual Billing & Receipts", "Disjointed Inventory Ledgers", "Unmonitored Medicine Expiry", "Disconnected Patient Records"]
    y_shift = height - 2.5 * inch
    for item in items:
        c.setFillColor(C_WHITE)
        c.setStrokeColor(C_BORDER)
        c.roundRect(8.6 * inch, y_shift, 3.6 * inch, 0.55 * inch, 6, fill=1, stroke=1)
        c.setFillColor(C_DARK)
        c.setFont("Helvetica", 11)
        c.drawCentredString(10.4 * inch, y_shift + 0.18 * inch, item)
        y_shift -= 0.68 * inch

    # Down arrow text
    c.setFillColor(C_TEAL)
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(10.4 * inch, y_shift + 0.1 * inch, "↓")

    # Banner
    c.setFillColor(C_TEAL)
    c.roundRect(8.6 * inch, 1.1 * inch, 3.6 * inch, 0.85 * inch, 6, fill=1, stroke=0)
    c.setFillColor(C_WHITE)
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(10.4 * inch, 1.55 * inch, "PHARMACY MANAGEMENT ERP")
    c.setFillColor(C_TEAL_LIGHT)
    c.setFont("Helvetica", 10)
    c.drawCentredString(10.4 * inch, 1.30 * inch, "One Unified, Cloud-Hosted Command Center")
    c.showPage()

    # =========================================================================
    # SLIDE 3: PROBLEM STATEMENT
    # =========================================================================
    draw_slide_header("Problem Statement", "Critical Bottlenecks in Traditional Pharmacy Retail", 3)

    problems = [
        ("01", "Inventory Expiry & Dead Stock", "Medicines sit on shelves unnoticed until expiry. Lack of batch-level tracking causes heavy recurring financial losses and safety hazards.", C_RED),
        ("02", "Billing Inefficiency & Errors", "Manual product lookups and manual pricing calculations slow down checkout queues, leading to pricing errors and customer dissatisfaction.", C_AMBER),
        ("03", "Coarse-Grained Stock Monitoring", "Tracking only gross medicine quantities without individual batch numbers, supplier tags, and manufacturing records prevents audit traceability.", C_TEAL),
        ("04", "Lack of Patient Traceability", "Manual customer logging fails to retain prescription history, visiting doctors, or previous purchase records for regular chronic patients.", C_CYAN),
        ("05", "Blind Financial Visibility", "Business owners lack real-time visibility into daily revenue, net profit margins, GST liability, and fast-moving vs dead inventory.", C_DARK),
        ("06", "Absence of Role-Based Security", "Cashiers, store managers, and owners share identical access permissions, exposing sensitive wholesale costs and financial metrics.", C_NAVY_CARD),
    ]

    coords_3 = [
        (0.8, 4.0), (4.85, 4.0), (8.9, 4.0),
        (0.8, 1.2), (4.85, 1.2), (8.9, 1.2)
    ]
    for (idx, title, desc, col), (x, y) in zip(problems, coords_3):
        c.setFillColor(C_WHITE)
        c.setStrokeColor(C_BORDER)
        c.roundRect(x * inch, y * inch, 3.6 * inch, 2.5 * inch, 8, fill=1, stroke=1)

        c.setFillColor(col)
        c.roundRect((x + 0.25) * inch, (y + 1.95) * inch, 0.65 * inch, 0.35 * inch, 4, fill=1, stroke=0)
        c.setFillColor(C_WHITE)
        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString((x + 0.57) * inch, (y + 2.05) * inch, idx)

        c.setFillColor(C_DARK)
        c.setFont("Helvetica-Bold", 12)
        c.drawString((x + 0.25) * inch, (y + 1.65) * inch, title)

        c.setFillColor(C_MUTED)
        c.setFont("Helvetica", 10)
        txt = c.beginText((x + 0.25) * inch, (y + 1.35) * inch)
        txt.setFont("Helvetica", 9.5)
        txt.setFillColor(C_MUTED)
        txt.textLines(desc)
        c.drawText(txt)
    c.showPage()

    # =========================================================================
    # SLIDE 4: OBJECTIVES
    # =========================================================================
    draw_slide_header("Project Objectives", "Concrete Engineering Goals of Pharmacy Management ERP", 4)

    objectives = [
        ("Centralized Web Platform", "Build a unified, responsive web ERP accessible across local network and cloud without requiring heavy client installations."),
        ("Interactive POS & Barcode Billing", "Implement instant medicine lookup via Select2 and physical barcode scanner input for sub-second checkout operations."),
        ("FEFO Batch-Level Inventory", "Enforce First-Expire-First-Out logic at the database level to ensure batches expiring earliest are automatically dispensed first."),
        ("Automated Reverse GST Engine", "Dynamically compute inclusive GST and tax breakups according to each medicine's registered tax slab (5%, 12%, 18%)."),
        ("Smart Patient CRM Directory", "Maintain patient profiles, visiting doctors, and cumulative purchase history with seamless AJAX auto-fill during billing."),
        ("Business Intelligence Dashboards", "Provide real-time analytics for revenue, net profit, batch expiry timelines, cash/UPI payment distributions, and CSV exports."),
        ("Reverse Logistics & Returns Desk", "Facilitate receipt barcode scanning for customer returns with automated stock shelf replenishment and refund tracking."),
        ("Three-Tier Role-Based Security", "Enforce strict separation of duties among Administrator (Owner), Store Manager, and Counter Cashier.")
    ]

    for i, (title, desc) in enumerate(objectives):
        col_idx = 0 if i < 4 else 1
        row_idx = i % 4
        x = 0.8 if col_idx == 0 else 6.8
        y = height - (2.6 * inch + (row_idx * 1.25 * inch))

        c.setFillColor(C_WHITE)
        c.setStrokeColor(C_BORDER)
        c.roundRect(x * inch, y, 5.7 * inch, 1.15 * inch, 6, fill=1, stroke=1)

        c.setFillColor(C_GREEN)
        c.circle((x + 0.45) * inch, y + 0.58 * inch, 0.22 * inch, fill=1, stroke=0)
        c.setFillColor(C_WHITE)
        c.setFont("Helvetica-Bold", 12)
        c.drawCentredString((x + 0.45) * inch, y + 0.50 * inch, "✓")

        c.setFillColor(C_DARK)
        c.setFont("Helvetica-Bold", 11.5)
        c.drawString((x + 0.85) * inch, y + 0.72 * inch, title)

        c.setFillColor(C_MUTED)
        c.setFont("Helvetica", 9.5)
        txt = c.beginText((x + 0.85) * inch, y + 0.50 * inch)
        txt.setFont("Helvetica", 9)
        txt.setFillColor(C_MUTED)
        txt.textLines(desc)
        c.drawText(txt)
    c.showPage()

    # =========================================================================
    # SLIDE 5: DFD LEVEL 0 (CONTEXT DIAGRAM) -- CRITICAL REQUIREMENT
    # =========================================================================
    draw_slide_header("System Modeling", "Data Flow Diagram — Level 0 (Context Diagram)", 5)

    # Center Process 0.0
    c.setFillColor(C_NAVY_BG)
    c.setStrokeColor(C_TEAL)
    c.setLineWidth(3)
    c.roundRect(4.6 * inch, 2.6 * inch, 4.1 * inch, 2.4 * inch, 12, fill=1, stroke=1)

    c.setFillColor(C_CYAN)
    c.setFont("Helvetica-Bold", 15)
    c.drawCentredString(6.65 * inch, 4.4 * inch, "0.0")

    c.setFillColor(C_WHITE)
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(6.65 * inch, 3.9 * inch, "PHARMACY MANAGEMENT")
    c.drawCentredString(6.65 * inch, 3.55 * inch, "ERP SYSTEM")

    c.setFillColor(C_TEAL_LIGHT)
    c.setFont("Helvetica", 10)
    c.drawCentredString(6.65 * inch, 3.1 * inch, "Centralized Web & Database Engine")

    # Entity 1: Cashier (Top Left)
    c.setFillColor(C_WHITE)
    c.setStrokeColor(C_TEAL)
    c.setLineWidth(1.5)
    c.roundRect(0.8 * inch, 4.3 * inch, 3.1 * inch, 1.7 * inch, 8, fill=1, stroke=1)
    c.setFillColor(C_TEAL)
    c.setFont("Helvetica-Bold", 10.5)
    c.drawString(1.0 * inch, 5.65 * inch, "COUNTER CASHIER / PHARMACIST")
    c.setFillColor(C_MUTED)
    c.setFont("Helvetica", 9)
    c.drawString(1.0 * inch, 5.35 * inch, "• Barcode / Product queries")
    c.drawString(1.0 * inch, 5.10 * inch, "• Customer phone & Cart item input")
    c.drawString(1.0 * inch, 4.85 * inch, "• Receipt & Return verification")

    # Entity 2: Admin (Top Right)
    c.setFillColor(C_WHITE)
    c.setStrokeColor(C_NAVY_BG)
    c.setLineWidth(1.5)
    c.roundRect(9.4 * inch, 4.3 * inch, 3.1 * inch, 1.7 * inch, 8, fill=1, stroke=1)
    c.setFillColor(C_NAVY_BG)
    c.setFont("Helvetica-Bold", 10.5)
    c.drawString(9.6 * inch, 5.65 * inch, "STORE MANAGER / ADMIN")
    c.setFillColor(C_MUTED)
    c.setFont("Helvetica", 9)
    c.drawString(9.6 * inch, 5.35 * inch, "• Stock batch & Supplier entries")
    c.drawString(9.6 * inch, 5.10 * inch, "• RBAC role configuration")
    c.drawString(9.6 * inch, 4.85 * inch, "• BI analytics & Reorder PO queries")

    # Entity 3: Customer (Bottom Left)
    c.setFillColor(C_WHITE)
    c.setStrokeColor(C_GREEN)
    c.setLineWidth(1.5)
    c.roundRect(0.8 * inch, 1.4 * inch, 3.1 * inch, 1.7 * inch, 8, fill=1, stroke=1)
    c.setFillColor(C_GREEN)
    c.setFont("Helvetica-Bold", 10.5)
    c.drawString(1.0 * inch, 2.75 * inch, "CUSTOMER / PATIENT")
    c.setFillColor(C_MUTED)
    c.setFont("Helvetica", 9)
    c.drawString(1.0 * inch, 2.45 * inch, "• Prescriptions & Contact phone")
    c.drawString(1.0 * inch, 2.20 * inch, "• Cash / UPI Payment")
    c.drawString(1.0 * inch, 1.95 * inch, "• Return item with receipt barcode")

    # Entity 4: Supplier (Bottom Right)
    c.setFillColor(C_WHITE)
    c.setStrokeColor(C_AMBER)
    c.setLineWidth(1.5)
    c.roundRect(9.4 * inch, 1.4 * inch, 3.1 * inch, 1.7 * inch, 8, fill=1, stroke=1)
    c.setFillColor(C_AMBER)
    c.setFont("Helvetica-Bold", 10.5)
    c.drawString(9.6 * inch, 2.75 * inch, "SUPPLIER / WHOLESALER")
    c.setFillColor(C_MUTED)
    c.setFont("Helvetica", 9)
    c.drawString(9.6 * inch, 2.45 * inch, "• Medicine batch consignments")
    c.drawString(9.6 * inch, 2.20 * inch, "• Purchase invoices & MRP data")
    c.drawString(9.6 * inch, 1.95 * inch, "• Automated reorder CSV orders")

    # Connecting Flow Labels
    c.setFillColor(C_DARK)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(4.0 * inch, 5.3 * inch, "→ Sales Data / Returns →")
    c.drawString(4.0 * inch, 4.9 * inch, "← Thermal Bill / Alerts ←")

    c.drawString(8.2 * inch, 5.3 * inch, "← New Stock / Roles ←")
    c.drawString(8.2 * inch, 4.9 * inch, "→ BI Reports & POs →")

    c.drawString(4.0 * inch, 2.3 * inch, "→ Prescriptions & Cash →")
    c.drawString(4.0 * inch, 1.9 * inch, "← Invoice & Refunds ←")

    c.drawString(8.2 * inch, 2.3 * inch, "← Invoices & Batches ←")
    c.drawString(8.2 * inch, 1.9 * inch, "→ Purchase Orders (CSV) →")

    # Bottom summary box
    c.setFillColor(C_WHITE)
    c.setStrokeColor(C_BORDER)
    c.roundRect(2.5 * inch, 0.45 * inch, 8.3 * inch, 0.65 * inch, 6, fill=1, stroke=1)
    c.setFillColor(C_MUTED)
    c.setFont("Helvetica", 9.5)
    c.drawCentredString(6.65 * inch, 0.72 * inch, "Context: Central system manages single-point of truth with real-time ACID transactions in SQLite.")
    c.showPage()

    # =========================================================================
    # SLIDE 6: DFD LEVEL 1 (DECOMPOSITION DIAGRAM) -- CRITICAL REQUIREMENT
    # =========================================================================
    draw_slide_header("System Modeling", "Data Flow Diagram — Level 1 (Decomposition Diagram)", 6)

    # Processes (Left column)
    processes_d1 = [
        ("1.0", "Authentication & RBAC Control", "Validates login against User/Group models; routes to Admin, Manager, or Cashier UI.", C_NAVY_BG),
        ("2.0", "POS & Reverse GST Billing Engine", "Accepts barcode/product queries; calculates GST dynamically; creates Sale transaction.", C_TEAL),
        ("3.0", "FEFO Batch Inventory Dispatch", "Sorts stock by expiry_date; deducts sold quantities; triggers Signal replenishment on deletion.", C_GREEN),
        ("4.0", "Reverse Logistics (Returns Desk)", "Scans receipt barcode; validates bill items; restocks physical units; logs ReturnSale audit.", C_AMBER),
        ("5.0", "Smart CRM & Customer Directory", "Executes AJAX telephone lookup; links customer to doctor, prescriptions, and purchase total.", C_CYAN),
        ("6.0", "Procurement & Reorder Engine", "Evaluates batch stocks against minimum_stock_level; exports CSV reorder purchase orders.", C_DARK),
        ("7.0", "Financial BI & Analytics Engine", "Aggregates daily sales, profit margins, GST totals, and payment modes (Cash/UPI).", C_RED),
    ]

    for i, (num, title, desc, col) in enumerate(processes_d1):
        y = height - (2.2 * inch + (i * 0.73 * inch))
        c.setFillColor(C_WHITE)
        c.setStrokeColor(C_BORDER)
        c.roundRect(0.8 * inch, y, 6.8 * inch, 0.66 * inch, 6, fill=1, stroke=1)

        c.setFillColor(col)
        c.roundRect(0.9 * inch, y + 0.12 * inch, 0.65 * inch, 0.42 * inch, 4, fill=1, stroke=0)
        c.setFillColor(C_WHITE)
        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(1.22 * inch, y + 0.24 * inch, num)

        c.setFillColor(C_DARK)
        c.setFont("Helvetica-Bold", 10.5)
        c.drawString(1.65 * inch, y + 0.38 * inch, title)

        c.setFillColor(C_MUTED)
        c.setFont("Helvetica", 8.5)
        c.drawString(1.65 * inch, y + 0.16 * inch, desc)

    # Data Stores (Right Column)
    data_stores = [
        ("D1", "Medicine Catalog Table", "Attributes: barcode, name, category, manufacturer, pack_size, gst_percentage, min_stock."),
        ("D2", "Stock Batches Table", "Attributes: medicine_id, batch_no, expiry_date, quantity, purchase_price, mrp, supplier_id."),
        ("D3", "Sale Ledger Table", "Attributes: bill_no, stock_id, quantity, total_price, customer_id, payment_method, date."),
        ("D4", "ReturnSale Audit Table", "Attributes: sale_id, stock_id, quantity_returned, refund_amount, reason, restocked, returned_at."),
        ("D5", "Customer CRM Table", "Attributes: name, phone (unique), last_doctor, cumulative purchase history."),
        ("D6", "Supplier Directory Table", "Attributes: name, contact_person, phone, email, address.")
    ]

    c.setFillColor(C_NAVY_BG)
    c.roundRect(8.0 * inch, height - 2.05 * inch, 4.5 * inch, 0.38 * inch, 4, fill=1, stroke=0)
    c.setFillColor(C_CYAN)
    c.setFont("Helvetica-Bold", 9.5)
    c.drawCentredString(10.25 * inch, height - 1.9 * inch, "DATABASE DATA STORES (RELATIONAL REPOSITORY)")

    for j, (ds_id, ds_name, ds_desc) in enumerate(data_stores):
        y = height - (2.75 * inch + (j * 0.78 * inch))
        c.setFillColor(C_WHITE)
        c.setStrokeColor(C_TEAL)
        c.setLineWidth(1.5)
        c.roundRect(8.0 * inch, y, 4.5 * inch, 0.70 * inch, 6, fill=1, stroke=1)

        c.setFillColor(C_TEAL)
        c.roundRect(8.1 * inch, y + 0.12 * inch, 0.55 * inch, 0.46 * inch, 3, fill=1, stroke=0)
        c.setFillColor(C_WHITE)
        c.setFont("Helvetica-Bold", 10.5)
        c.drawCentredString(8.37 * inch, y + 0.25 * inch, ds_id)

        c.setFillColor(C_DARK)
        c.setFont("Helvetica-Bold", 10.5)
        c.drawString(8.75 * inch, y + 0.42 * inch, ds_name)

        c.setFillColor(C_MUTED)
        c.setFont("Helvetica", 8)
        c.drawString(8.75 * inch, y + 0.18 * inch, ds_desc)
    c.showPage()

    # =========================================================================
    # SLIDE 7: CORE PROPOSED MODULES
    # =========================================================================
    draw_slide_header("Proposed System", "Core Operational Modules of Pharmacy Management ERP", 7)

    modules_7 = [
        ("POS & Dynamic Billing", ["• Barcode scanner input", "• Select2 live medicine search", "• Real-time cart calculation", "• Scannable thermal receipt printing"], C_TEAL),
        ("FEFO Batch Inventory", ["• Batch-level tracking", "• Automatic earliest-expiry allocation", "• Visual expiry alert badges", "• Automated stock deduction"], C_GREEN),
        ("Patient CRM Directory", ["• Fast AJAX phone lookup", "• Prescribing doctor tracking", "• Lifetime purchases & spend", "• Returning patient loyalty"], C_CYAN),
        ("Financial Analytics & BI", ["• Dynamic GST tax breakdown", "• Revenue & profit margins", "• Best-selling medicine ranking", "• CSV financial export"], C_AMBER),
        ("Reverse Logistics Desk", ["• Receipt barcode returns", "• Return reason logging", "• Automatic shelf restocking", "• Customer refund computation"], C_RED),
        ("Security & RBAC", ["• Admin, Manager, Cashier roles", "• View-level access restrictions", "• Sensitive cost masking", "• Auto session timeout on close"], C_NAVY_BG),
    ]

    for (m_title, m_items, m_col), (x, y) in zip(modules_7, coords_3):
        c.setFillColor(C_WHITE)
        c.setStrokeColor(C_BORDER)
        c.roundRect(x * inch, y * inch, 3.6 * inch, 2.5 * inch, 8, fill=1, stroke=1)

        c.setFillColor(m_col)
        c.roundRect(x * inch, (y + 2.05) * inch, 3.6 * inch, 0.45 * inch, 6, fill=1, stroke=0)
        c.setFillColor(C_WHITE)
        c.setFont("Helvetica-Bold", 10.5)
        c.drawCentredString((x + 1.8) * inch, (y + 2.2) * inch, m_title.upper())

        c.setFillColor(C_DARK)
        c.setFont("Helvetica", 10)
        y_item = y + 1.65
        for itm in m_items:
            c.drawString((x + 0.3) * inch, y_item * inch, itm)
            y_item -= 0.35
    c.showPage()

    # =========================================================================
    # SLIDE 8: THREE-TIER SYSTEM ARCHITECTURE
    # =========================================================================
    draw_slide_header("System Architecture", "Three-Tier Modular Web Architecture", 8)

    layers_8 = [
        ("Presentation Layer (Client)", "HTML5  •  CSS3  •  Bootstrap 5.3  •  Vanilla JavaScript (ES6)  •  AJAX  •  Select2  •  JsBarcode  •  FontAwesome", C_TEAL),
        ("Application Layer (Business Logic)", "Python 3.14  •  Django 6.0.4  •  Django Views & Middleware  •  Django ORM  •  FEFO Engine  •  Signals  •  RBAC Engine", C_NAVY_BG),
        ("Data Layer (Persistent Storage)", "SQLite Database (Production Deployment)  •  Relational Models (Medicine, Stock, Sale, ReturnSale, Customer, Supplier)", C_DARK),
        ("Cloud Infrastructure & Security", "PythonAnywhere Cloud PaaS  •  Django WSGI  •  Session Timeout Security  •  python-dotenv Secret Vault", C_CYAN)
    ]

    for i, (l_title, l_techs, l_col) in enumerate(layers_8):
        y = height - (2.6 * inch + (i * 1.25 * inch))
        c.setFillColor(C_WHITE)
        c.setStrokeColor(C_BORDER)
        c.roundRect(0.8 * inch, y, 11.733 * inch, 1.05 * inch, 6, fill=1, stroke=1)

        c.setFillColor(l_col)
        c.rect(0.8 * inch, y, 0.18 * inch, 1.05 * inch, fill=1, stroke=0)

        c.setFillColor(l_col)
        c.setFont("Helvetica-Bold", 13)
        c.drawString(1.2 * inch, y + 0.65 * inch, l_title)

        c.setFillColor(C_DARK)
        c.setFont("Helvetica", 10.5)
        c.drawString(1.2 * inch, y + 0.30 * inch, l_techs)
    c.showPage()

    # =========================================================================
    # SLIDE 9: TECHNOLOGY STACK
    # =========================================================================
    draw_slide_header("Tools & Technologies", "Full Implementation Technology Stack", 9)

    tech_left = [
        ("Programming Language", "Python 3.14 (High-efficiency backend execution)"),
        ("Backend Framework", "Django 6.0.4 (MVC/MVT modular framework)"),
        ("Database Engine", "SQLite / Relational Schema (Zero-config, ACID-compliant)"),
        ("Object-Relational Mapper", "Django ORM (Safe parameterized queries & transactions)"),
        ("UI Presentation", "HTML5, CSS3, Bootstrap 5.3 (Responsive desktop/tablet UI)"),
        ("Client-Side Scripting", "Vanilla JavaScript (ES6) (Fast DOM & event handling)")
    ]

    tech_right = [
        ("Asynchronous Operations", "AJAX (Background patient search & master additions)"),
        ("Search Autocomplete", "Select2 (Fuzzy fast medicine lookup in POS)"),
        ("Barcode Generation", "JsBarcode (Thermal bill scannable CODE128 generation)"),
        ("Data Visualization", "Chart.js (Interactive financial & revenue line charts)"),
        ("Environment Security", "python-dotenv (Vault isolation for SECRET_KEY)"),
        ("Cloud Deployment", "PythonAnywhere & Django WSGI (Public web access)")
    ]

    for i, (k, v) in enumerate(tech_left):
        y = height - (2.3 * inch + (i * 0.85 * inch))
        c.setFillColor(C_WHITE)
        c.setStrokeColor(C_BORDER)
        c.roundRect(0.8 * inch, y, 5.6 * inch, 0.75 * inch, 6, fill=1, stroke=1)
        c.setFillColor(C_TEAL)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(1.0 * inch, y + 0.45 * inch, k)
        c.setFillColor(C_DARK)
        c.setFont("Helvetica", 9.5)
        c.drawString(1.0 * inch, y + 0.20 * inch, v)

    for i, (k, v) in enumerate(tech_right):
        y = height - (2.3 * inch + (i * 0.85 * inch))
        c.setFillColor(C_WHITE)
        c.setStrokeColor(C_BORDER)
        c.roundRect(6.8 * inch, y, 5.7 * inch, 0.75 * inch, 6, fill=1, stroke=1)
        c.setFillColor(C_CYAN)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(7.0 * inch, y + 0.45 * inch, k)
        c.setFillColor(C_DARK)
        c.setFont("Helvetica", 9.5)
        c.drawString(7.0 * inch, y + 0.20 * inch, v)
    c.showPage()

    # =========================================================================
    # SLIDE 10: KEY TECHNICAL DEPTH & INNOVATIONS
    # =========================================================================
    draw_slide_header("Technical Depth", "Core Algorithms & Implementation Highlights", 10)

    highlights = [
        ("Automated FEFO Dispatch Algorithm", "Instead of arbitrary manual batch picking, queries evaluate all active batches ordered by expiry_date ASC. If quantity exceeds first batch, it automatically rolls to next batch without manual intervention.", C_TEAL),
        ("Dynamic Reverse GST Calculation", "Since medicine MRPs are legally tax-inclusive in India, the billing engine executes reverse calculation: Base = Total / (1 + GST/100), accurately reporting CGST and SGST on receipts.", C_GREEN),
        ("Event-Driven Django Signals", "Implemented post_delete receiver signal on Sale transactions. If a transaction is canceled or refunded, stock is automatically credited back to its exact batch without manual adjustment.", C_CYAN),
        ("Asynchronous Patient Auto-Fill", "Typing customer phone trigger debounced AJAX queries to /api/get_customer/. It returns patient name and visiting doctor instantaneously, accelerating checkout speed.", C_AMBER),
        ("Multi-Tier Role-Based Security", "Custom middleware and template permission checks verify request.user.groups. Store cashiers are blocked from seeing profit metrics and cannot create new batches.", C_RED),
        ("Enterprise POS Session Hardening", "Configured SESSION_EXPIRE_AT_BROWSER_CLOSE = True and SESSION_COOKIE_AGE = 1800, guaranteeing counter terminals auto-logout upon browser closure or inactivity.", C_NAVY_BG)
    ]

    for (title, desc, col), (x, y) in zip(highlights, coords_3):
        c.setFillColor(C_WHITE)
        c.setStrokeColor(C_BORDER)
        c.roundRect(x * inch, y * inch, 3.6 * inch, 2.5 * inch, 8, fill=1, stroke=1)

        c.setFillColor(col)
        c.rect(x * inch, (y + 2.42) * inch, 3.6 * inch, 0.08 * inch, fill=1, stroke=0)

        c.setFillColor(col)
        c.setFont("Helvetica-Bold", 11.5)
        c.drawString((x + 0.25) * inch, (y + 2.05) * inch, title)

        txt = c.beginText((x + 0.25) * inch, (y + 1.75) * inch)
        txt.setFont("Helvetica", 9)
        txt.setFillColor(C_DARK)
        txt.textLines(desc)
        c.drawText(txt)
    c.showPage()

    # =========================================================================
    # SLIDE 11: DATABASE SCHEMA
    # =========================================================================
    draw_slide_header("Database Design", "Relational Entity Schema & Data Relationships", 11)

    models_data = [
        ("Medicine (Product Master)", ["• barcode (Unique)", "• name, category", "• manufacturer", "• gst_percentage", "• minimum_stock_level", "• pack_size", "• @property total_stock"]),
        ("Stock (Batch Inventory)", ["• batch_no", "• expiry_date (Date)", "• quantity (Int)", "• purchase_price (Float)", "• mrp (Float)", "• FK -> Medicine (CASCADE)", "• FK -> Supplier (SET_NULL)"]),
        ("Sale (Transaction Ledger)", ["• bill_no (Indexed)", "• quantity (Int)", "• total_price (Float)", "• payment_method (Cash/UPI)", "• date (DateTimeField)", "• FK -> Stock (CASCADE)", "• FK -> Customer (SET_NULL)"]),
        ("ReturnSale (Audit Trail)", ["• quantity_returned (Int)", "• refund_amount (Float)", "• reason (WRONG/DEFECT/EXCESS)", "• restocked (Boolean)", "• returned_at (DateTime)", "• FK -> Sale (CASCADE)", "• FK -> Stock (CASCADE)"]),
        ("Customer (Smart CRM)", ["• name (Char)", "• phone (Unique 15)", "• last_doctor (Char)", "• related: purchase_history", "• computed: total_spent", "", ""]),
        ("Supplier (Wholesaler)", ["• name (Char 200)", "• contact_person", "• phone, email", "• address (Text)", "• related: stock_set", "", ""])
    ]

    for (m_name, m_fields), (x, y) in zip(models_data, coords_3):
        c.setFillColor(C_WHITE)
        c.setStrokeColor(C_BORDER)
        c.roundRect(x * inch, y * inch, 3.6 * inch, 2.5 * inch, 8, fill=1, stroke=1)

        c.setFillColor(C_NAVY_BG)
        c.roundRect(x * inch, (y + 2.08) * inch, 3.6 * inch, 0.42 * inch, 6, fill=1, stroke=0)
        c.setFillColor(C_CYAN)
        c.setFont("Helvetica-Bold", 10.5)
        c.drawCentredString((x + 1.8) * inch, (y + 2.22) * inch, m_name)

        c.setFillColor(C_DARK)
        c.setFont("Helvetica", 9)
        y_f = y + 1.8
        for fld in m_fields:
            if fld:
                c.drawString((x + 0.25) * inch, y_f * inch, fld)
                y_f -= 0.25
    c.showPage()

    # =========================================================================
    # SLIDE 12: DEVELOPMENT PROGRESSION
    # =========================================================================
    draw_slide_header("Project Progression", "Phased Development Milestones (Major Project Build)", 12)

    milestones = [
        ("Phase 1: Requirements & Modeling", "Analysis of pharmaceutical retail workflows, GST compliance rules, FEFO logic, and SQLite relational database schema."),
        ("Phase 2: Core Backend Engine", "Implemented Django models, Django ORM relationships, management commands, and database migrations."),
        ("Phase 3: Interactive POS Billing", "Developed quick-checkout billing interface with dynamic Select2 searching, barcode reader input, and thermal receipt generator."),
        ("Phase 4: Inventory & FEFO Engine", "Built batch management, automatic earliest-expiry deduction, low-stock reorder CSV export, and batch entry forms."),
        ("Phase 5: Reverse Logistics & Returns", "Engineered returns desk with bill barcode verification, refund calculation, and automated stock shelf restoration."),
        ("Phase 6: CRM & Business Intelligence", "Integrated asynchronous patient lookup, customer purchase history directory, and real-time Chart.js KPI analytics."),
        ("Phase 7: Security & Cloud Deployment", "Enforced RBAC permissions, environment variable secret isolation, session hardening, and cloud deployment on PythonAnywhere.")
    ]

    for i, (m_title, m_desc) in enumerate(milestones):
        y = height - (2.1 * inch + (i * 0.74 * inch))
        c.setFillColor(C_WHITE)
        c.setStrokeColor(C_BORDER)
        c.roundRect(0.8 * inch, y, 11.733 * inch, 0.67 * inch, 6, fill=1, stroke=1)

        c.setFillColor(C_TEAL)
        c.roundRect(0.95 * inch, y + 0.12 * inch, 0.65 * inch, 0.42 * inch, 4, fill=1, stroke=0)
        c.setFillColor(C_WHITE)
        c.setFont("Helvetica-Bold", 10.5)
        c.drawCentredString(1.27 * inch, y + 0.24 * inch, f"P{i+1}")

        c.setFillColor(C_DARK)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(1.75 * inch, y + 0.38 * inch, m_title)

        c.setFillColor(C_MUTED)
        c.setFont("Helvetica", 9)
        c.drawString(1.75 * inch, y + 0.16 * inch, m_desc)
    c.showPage()

    # =========================================================================
    # SLIDE 13: APPLICATIONS
    # =========================================================================
    draw_slide_header("Applications & Use Cases", "Practical Deployment Scenarios for Pharmacy ERP", 13)

    apps = [
        ("Independent Retail Pharmacies", "Single-location medical stores that require quick barcode billing, automated FEFO expiry protection, and simplified daily GST bookkeeping.", C_TEAL),
        ("Hospital Outpatient Dispensaries", "High-volume hospital pharmacies that demand high-speed customer lookup, doctor-prescription tracking, and tight batch accountability.", C_NAVY_BG),
        ("Chain & Multi-Counter Stores", "Multi-terminal medical retail stores with designated cashier and store manager roles, preventing data tampering and stock leakage.", C_CYAN),
        ("Rural Healthcare Centers", "Low-overhead deployment capable of running on modest hardware and low bandwidth with reliable local SQLite storage and cloud synchronization.", C_GREEN)
    ]

    for i, (title, desc, col) in enumerate(apps):
        x = 0.8 if i % 2 == 0 else 6.8
        y = 3.8 if i < 2 else 1.2
        c.setFillColor(C_WHITE)
        c.setStrokeColor(C_BORDER)
        c.roundRect(x * inch, y * inch, 5.7 * inch, 2.3 * inch, 8, fill=1, stroke=1)

        c.setFillColor(col)
        c.roundRect(x * inch, (y + 1.88) * inch, 5.7 * inch, 0.42 * inch, 6, fill=1, stroke=0)
        c.setFillColor(C_WHITE)
        c.setFont("Helvetica-Bold", 11)
        c.drawCentredString((x + 2.85) * inch, (y + 2.02) * inch, title.upper())

        txt = c.beginText((x + 0.35) * inch, (y + 1.45) * inch)
        txt.setFont("Helvetica", 10.5)
        txt.setFillColor(C_DARK)
        txt.textLines(desc)
        c.drawText(txt)
    c.showPage()

    # =========================================================================
    # SLIDE 14: FUTURE ROADMAP
    # =========================================================================
    draw_slide_header("Future Scope", "Phase 2 Technological Roadmap", 14)

    future = [
        ("AI & Machine Learning", "• OCR-based doctor prescription parsing\n• Predictive medicine stock replenishment\n• Seasonal disease outbreak demand forecasting", C_TEAL),
        ("Mobile & REST API Ecosystem", "• Django REST Framework (DRF) API endpoints\n• Mobile Android/iOS apps for store owners\n• Bluetooth mobile thermal printer integration", C_CYAN),
        ("Communication Automation", "• WhatsApp Business Cloud API integration\n• Automated SMS digital receipt delivery\n• Automated low-stock email alerts to suppliers", C_AMBER),
        ("Enterprise Scalability & DevOps", "• Seamless migration from SQLite to PostgreSQL\n• Docker containerization & microservice scaling\n• Automated CI/CD pipeline deployment", C_NAVY_BG)
    ]

    for (title, desc, col), (x, y) in zip(future, [(0.8, 3.8), (6.8, 3.8), (0.8, 1.2), (6.8, 1.2)]):
        c.setFillColor(C_WHITE)
        c.setStrokeColor(C_BORDER)
        c.roundRect(x * inch, y * inch, 5.7 * inch, 2.3 * inch, 8, fill=1, stroke=1)

        c.setFillColor(col)
        c.roundRect(x * inch, (y + 1.88) * inch, 5.7 * inch, 0.42 * inch, 6, fill=1, stroke=0)
        c.setFillColor(C_WHITE)
        c.setFont("Helvetica-Bold", 11)
        c.drawCentredString((x + 2.85) * inch, (y + 2.02) * inch, title.upper())

        txt = c.beginText((x + 0.35) * inch, (y + 1.45) * inch)
        txt.setFont("Helvetica", 10.5)
        txt.setFillColor(C_DARK)
        txt.textLines(desc)
        c.drawText(txt)
    c.showPage()

    # =========================================================================
    # SLIDE 15: CONCLUSION
    # =========================================================================
    c.setFillColor(C_NAVY_BG)
    c.rect(0, 0, width, height, fill=1, stroke=0)

    c.setFillColor(C_TEAL_LIGHT)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(0.8 * inch, height - 1.0 * inch, "CONCLUSION & SUMMARY")

    c.setFillColor(C_WHITE)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(0.8 * inch, height - 1.45 * inch, "Transforming Retail Pharmacy into an Automated Digital Enterprise")

    concl_points = [
        ("Centralized Web Efficiency", "Successfully eliminated disjointed paper ledgers and fragmented software by consolidating POS, inventory, CRM, and analytics into one web platform."),
        ("Elimination of Expiry Losses", "Enforced automated FEFO batch allocation, preventing older stock from expiring unnoticed on shelves."),
        ("Compliance & Billing Speed", "Implemented dynamic reverse GST calculations and barcode scanning, enabling rapid, error-free checkout counter operations."),
        ("Auditability & Reverse Logistics", "Delivered barcode-verified customer returns desk with automatic shelf inventory recovery and ReturnSale audit logs."),
        ("Academic & Practical Success", "Fully implemented, tested, and cloud-deployed on PythonAnywhere with complete role-based security, ready for real-world deployment.")
    ]

    for i, (head, body) in enumerate(concl_points):
        y = height - (2.4 * inch + (i * 0.95 * inch))
        c.setFillColor(C_NAVY_CARD)
        c.setStrokeColor(HexColor("#285073"))
        c.roundRect(0.8 * inch, y, 11.733 * inch, 0.82 * inch, 6, fill=1, stroke=1)

        c.setFillColor(C_CYAN)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(1.1 * inch, y + 0.48 * inch, "✔  " + head + ":")

        c.setFillColor(HexColor("#dce6f2"))
        c.setFont("Helvetica", 10.5)
        c.drawString(1.1 * inch, y + 0.22 * inch, body)

    c.setFillColor(C_TEAL)
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(width / 2.0, 0.65 * inch, "THANK YOU  |  QUESTIONS & DISCUSSION")
    c.showPage()

    c.save()
    print(f"SUCCESS: Generated PDF at {pdf_filename}")

if __name__ == '__main__':
    generate_pdf()
