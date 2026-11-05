import os
from PIL import Image, ImageDraw, ImageFont

# Canvas dimensions (Full HD 16:9 Widescreen)
W = 1920
H = 1080

# Windows TrueType Fonts
FONT_REG = "C:/Windows/Fonts/segoeui.ttf"
FONT_BOLD = "C:/Windows/Fonts/segoeuib.ttf"
FONT_ITALIC = "C:/Windows/Fonts/segoeuii.ttf"

def get_font(size, bold=False, italic=False):
    f_path = FONT_BOLD if bold else (FONT_ITALIC if italic else FONT_REG)
    return ImageFont.truetype(f_path, size)

# Color Palette matching original PDF exactly
C_NAVY_BG = "#0d2335"
C_NAVY_ACCENT = "#122f46"
C_LIGHT_BG = "#f4f6f8"
C_WHITE = "#ffffff"
C_TEAL_DARK = "#005f5f"
C_TEAL = "#008b8b"
C_TEAL_LIGHT = "#e0f2f1"
C_CYAN_BRIGHT = "#00c49f"
C_CYAN = "#0ea5e9"
C_DARK = "#111827"
C_GRAY_TXT = "#4b5563"
C_MUTED = "#6b7280"
C_LIGHT_GRAY = "#9ca3af"
C_BORDER = "#e5e7eb"
C_GREEN = "#10b981"
C_AMBER = "#f59e0b"
C_RED = "#ef4444"
C_CARD_BG = "#ffffff"

def draw_standard_header(d, tag, title, slide_num):
    # Tag in uppercase with wide spacing
    f_tag = get_font(16, bold=True)
    spaced_tag = "  ".join(tag.upper())
    d.text((120, 75), spaced_tag, fill=C_TEAL, font=f_tag)

    # Main Title
    f_title = get_font(38, bold=True)
    d.text((120, 115), title, fill=C_DARK, font=f_title)

    # Slide Number
    f_num = get_font(18, bold=True)
    d.text((W - 160, H - 75), str(slide_num).zfill(2), fill=C_LIGHT_GRAY, font=f_num)

def create_slide_1():
    img = Image.new("RGB", (W, H), C_NAVY_BG)
    d = ImageDraw.Draw(img)

    # Top-left Pill Icon Badge
    d.ellipse([(120, 60), (220, 160)], fill="#00c49f")
    d.rounded_rectangle([(155, 95), (185, 125)], radius=4, fill=C_WHITE)
    # Cross
    d.rectangle([(167, 100), (173, 120)], fill="#00c49f")
    d.rectangle([(160, 107), (180, 113)], fill="#00c49f")

    # Title & Subtitle
    f_title = get_font(54, bold=True)
    d.text((120, 210), "PHARMACY MANAGEMENT SYSTEM", fill=C_WHITE, font=f_title)

    f_sub = get_font(24)
    d.text((120, 285), "A Centralized Web-Based ERP Platform for Retail Pharmacy Management", fill="#7dd3fc", font=f_sub)

    # Thin separator line
    d.line([(120, 335), (1050, 335)], fill="#1e3a53", width=2)

    # Presented By Section
    f_lbl = get_font(17, bold=True)
    d.text((450, 390), "Presented by:", fill=C_WHITE, font=f_lbl)

    f_pres = get_font(28, bold=True)
    d.text((250, 440), "MD ZEESHAN (23BTCS026HY)", fill="#00e5bf", font=f_pres)
    d.text((250, 495), "YUSUF HANZALA (23BTCS005HY)", fill="#00e5bf", font=f_pres)

    # Semester details
    f_sem = get_font(17, bold=True)
    d.text((1100, 440), "7 T H   S E M E S T E R", fill=C_WHITE, font=f_sem)
    d.text((1100, 475), "B . T E C H   C S", fill=C_WHITE, font=f_sem)
    d.text((1100, 510), "S E S S I O N   2 0 2 6 - 2 7", fill=C_WHITE, font=f_sem)

    # Supervisor Section
    d.text((450, 630), "Under the Supervision", fill=C_WHITE, font=f_lbl)
    d.text((530, 665), "Of", fill=C_WHITE, font=f_lbl)

    f_sup = get_font(28, bold=True)
    d.text((250, 720), "Mrs. Nusrath Fathima (Assistant Professor)", fill=C_WHITE, font=f_sup)

    # University & Department
    f_dept = get_font(20, italic=True)
    d.text((250, 850), "Department of Computer Science & Information Technology", fill="#7dd3fc", font=f_dept)
    d.text((250, 890), "Maulana Azad National Urdu University", fill="#7dd3fc", font=f_dept)

    return img

def create_slide_2():
    img = Image.new("RGB", (W, H), C_LIGHT_BG)
    d = ImageDraw.Draw(img)
    draw_standard_header(d, "Introduction", "From Fragmented Operations to One Platform", 2)

    bullets = [
        "Pharmaceutical retail involves interconnected operations — billing, inventory, purchasing, customer management, and financial monitoring.",
        "Traditional pharmacy operations often rely on manual records or fragmented, disconnected software.",
        "This fragmentation makes stock monitoring, expiry tracking, billing, and business analysis difficult.",
        "PHARMACY ERP provides a centralized, web-based ERP platform that integrates these operations.",
        "The system is purpose-built around the real operational needs of a pharmacy."
    ]

    f_body = get_font(20)
    y = 240
    for b in bullets:
        d.ellipse([(120, y + 8), (134, y + 22)], fill=C_CYAN)
        
        words = b.split()
        line = ""
        for w in words:
            if len(line + " " + w) < 65:
                line = (line + " " + w).strip()
            else:
                d.text((160, y), line, fill=C_DARK, font=f_body)
                y += 34
                line = w
        if line:
            d.text((160, y), line, fill=C_DARK, font=f_body)
            y += 42
        y += 24

    # Right side: THE SHIFT container
    d.rounded_rectangle([(1220, 220), (1800, 850)], radius=16, fill="#e6f2f2", outline=C_BORDER, width=1)
    f_sh_lbl = get_font(16, bold=True)
    d.text((1440, 260), "T H E   S H I F T", fill=C_TEAL, font=f_sh_lbl)

    boxes = [("Billing", 1260, 320, 1500, 380),
             ("Inventory", 1520, 320, 1760, 380),
             ("Purchase", 1260, 400, 1500, 460),
             ("Customers", 1520, 400, 1760, 460)]
    f_btn = get_font(18)
    for txt, x1, y1, x2, y2 in boxes:
        d.rounded_rectangle([(x1, y1), (x2, y2)], radius=10, fill=C_WHITE, outline=C_BORDER, width=1)
        d.text((x1 + 35, y1 + 16), txt, fill=C_DARK, font=f_btn)

    # Down Arrow
    d.ellipse([(1480, 500), (1540, 560)], fill=C_TEAL)
    d.polygon([(1500, 520), (1520, 520), (1510, 545)], fill=C_WHITE)

    # Pharmacy ERP Banner
    d.rounded_rectangle([(1260, 600), (1760, 800)], radius=16, fill=C_TEAL_DARK)
    d.ellipse([(1290, 630), (1350, 690)], fill="#008b8b")
    # Medical cross in badge
    d.rectangle([(1317, 642), (1323, 678)], fill=C_WHITE)
    d.rectangle([(1302, 657), (1338, 663)], fill=C_WHITE)

    f_erp = get_font(24, bold=True)
    d.text((1375, 645), "PHARMACY ERP", fill=C_WHITE, font=f_erp)

    f_erp_desc = get_font(18)
    d.text((1290, 720), "One centralized, web-based platform", fill="#cce8e8", font=f_erp_desc)
    d.text((1290, 750), "integrating every core operation.", fill="#cce8e8", font=f_erp_desc)

    return img

def create_slide_3():
    img = Image.new("RGB", (W, H), C_LIGHT_BG)
    d = ImageDraw.Draw(img)
    draw_standard_header(d, "Problem Statement", "Problems in Traditional Pharmacy Management", 3)

    cards = [
        ("01", "Inventory Expiry", "Medicines may sit in stock until expiry; lack of batch-level monitoring causes financial losses.", C_TEAL),
        ("02", "Billing Inefficiency", "Manual medicine search and billing is slow, and tax calculation is prone to human error.", C_CYAN),
        ("03", "Stock Management", "Individual batches are hard to track, and low-stock medicines often go unnoticed.", C_DARK),
        ("04", "Customer Management", "Repeated manual customer entry and poor access to previous purchase history.", C_TEAL_DARK),
        ("05", "Financial Monitoring", "Limited real-time visibility into revenue, profit, and daily cash/UPI sales.", C_AMBER),
        ("06", "Access Control", "Different employees need different levels of system access — rarely enforced.", C_NAVY_BG)
    ]

    coords = [
        (120, 220), (690, 220), (1260, 220),
        (120, 560), (690, 560), (1260, 560)
    ]

    f_num = get_font(32, bold=True)
    f_card_t = get_font(22, bold=True)
    f_card_d = get_font(17)

    for (num, title, desc, col), (x, y) in zip(cards, coords):
        d.rounded_rectangle([(x, y), (x + 540, y + 290)], radius=14, fill=C_WHITE, outline=C_BORDER, width=1)
        
        # Circle Icon
        d.ellipse([(x + 35, y + 35), (x + 95, y + 95)], fill=col)
        # Inner symbol
        d.ellipse([(x + 55, y + 55), (x + 75, y + 75)], fill=C_WHITE)

        # Number on right
        d.text((x + 470, y + 30), num, fill="#d1d5db", font=f_num)

        # Title
        d.text((x + 35, y + 120), title, fill=C_DARK, font=f_card_t)

        # Description wrapped
        words = desc.split()
        line = ""
        dy = y + 165
        for w in words:
            if len(line + " " + w) < 36:
                line = (line + " " + w).strip()
            else:
                d.text((x + 35, dy), line, fill=C_GRAY_TXT, font=f_card_d)
                dy += 26
                line = w
        if line:
            d.text((x + 35, dy), line, fill=C_GRAY_TXT, font=f_card_d)

    return img

def create_slide_4():
    img = Image.new("RGB", (W, H), C_LIGHT_BG)
    d = ImageDraw.Draw(img)
    draw_standard_header(d, "Objectives", "Objectives of Pharmacy ERP", 4)

    left_items = [
        "Develop a centralized, web-based Pharmacy ERP",
        "Implement an interactive Point of Sale (POS) system",
        "Provide batch-level inventory management",
        "Implement FEFO (First-Expire-First-Out) handling",
        "Automate GST-aware billing calculations"
    ]

    right_items = [
        "Maintain customer information & purchase history",
        "Provide real-time business intelligence dashboards",
        "Identify low-stock and expiry-related risks",
        "Implement role-based access control (RBAC)",
        "Deploy the application on a cloud-hosted environment"
    ]

    f_item = get_font(21)
    
    y = 250
    for item in left_items:
        d.ellipse([(120, y + 2), (160, y + 42)], fill="#00c49f")
        # Checkmark
        d.line([(132, y + 22), (140, y + 30)], fill=C_WHITE, width=4)
        d.line([(140, y + 30), (150, y + 14)], fill=C_WHITE, width=4)
        d.text((185, y + 8), item, fill=C_DARK, font=f_item)
        y += 120

    y = 250
    for item in right_items:
        d.ellipse([(1000, y + 2), (1040, y + 42)], fill="#00c49f")
        d.line([(1012, y + 22), (1020, y + 30)], fill=C_WHITE, width=4)
        d.line([(1020, y + 30), (1030, y + 14)], fill=C_WHITE, width=4)
        d.text((1065, y + 8), item, fill=C_DARK, font=f_item)
        y += 120

    return img

def create_slide_5():
    img = Image.new("RGB", (W, H), C_LIGHT_BG)
    d = ImageDraw.Draw(img)
    draw_standard_header(d, "Existing System", "The Conventional Approach", 5)

    # Left Pipeline
    steps = [
        "Medicine Purchase",
        "Manual / Separate Records",
        "Stock Management",
        "Billing",
        "Customer Records",
        "Financial Calculation",
        "Manual Reporting"
    ]
    f_step = get_font(18)
    y = 230
    for i, s in enumerate(steps):
        is_highlight = (i == 1)
        bg_col = "#005f5f" if is_highlight else C_WHITE
        txt_col = C_WHITE if is_highlight else C_DARK
        border_col = "#005f5f" if is_highlight else C_BORDER
        d.rounded_rectangle([(120, y), (560, y + 60)], radius=8, fill=bg_col, outline=border_col, width=1)
        d.text((160, y + 16), s, fill=txt_col, font=f_step)
        
        if i < len(steps) - 1:
            d.polygon([(335, y + 65), (345, y + 65), (340, y + 75)], fill=C_MUTED)
        y += 85

    # Middle Major Drawbacks
    f_sec = get_font(16, bold=True)
    d.text((660, 230), "M A J O R   D R A W B A C K S", fill=C_TEAL, font=f_sec)

    drawbacks = [
        "Fragmented information",
        "Manual data entry",
        "Difficult batch-level tracking",
        "Expiry monitoring challenges",
        "Slower billing workflow",
        "Limited real-time analytics",
        "Manual procurement monitoring",
        "Limited role-based access"
    ]
    f_db = get_font(19)
    y_db = 280
    for db in drawbacks:
        d.ellipse([(660, y_db + 8), (672, y_db + 20)], fill=C_CYAN)
        d.text((695, y_db), db, fill=C_DARK, font=f_db)
        y_db += 65

    # Right Main Gap Container
    d.rounded_rectangle([(1260, 220), (1800, 850)], radius=16, fill=C_NAVY_BG)
    d.ellipse([(1480, 280), (1580, 380)], fill="#00c49f")
    d.ellipse([(1515, 315), (1545, 345)], fill=C_NAVY_BG)

    f_gap_tag = get_font(15, bold=True)
    d.text((1490, 420), "M A I N   G A P", fill=C_CYAN_BRIGHT, font=f_gap_tag)

    f_gap = get_font(30, bold=True)
    d.text((1330, 490), "Operational data exists", fill=C_WHITE, font=f_gap)
    d.text((1330, 535), "— but it is not sufficiently", fill=C_WHITE, font=f_gap)
    d.text((1330, 580), "integrated.", fill=C_WHITE, font=f_gap)

    return img

def create_slide_6():
    img = Image.new("RGB", (W, H), C_LIGHT_BG)
    d = ImageDraw.Draw(img)
    draw_standard_header(d, "Proposed System", "PHARMACY ERP — Core Modules", 6)

    f_sub = get_font(19, italic=True)
    d.text((120, 175), "Integrates every major pharmacy operation into one centralized platform.", fill=C_MUTED, font=f_sub)

    modules = [
        ("POS & Billing", ["• Medicine search", "• Barcode input", "• Cart management", "• Billing"], False, C_TEAL),
        ("Inventory", ["• Batch tracking", "• Expiry management", "• FEFO", "• Low-stock monitoring"], False, C_DARK),
        ("CRM", ["• Customer directory", "• Purchase history", "• AJAX-based lookup", "• Lifetime spend metrics"], True, C_TEAL_DARK),
        ("Financial & BI", ["• GST calculation", "• Revenue tracking", "• Profit calculation", "• Sales analytics"], False, C_AMBER),
        ("Security", ["• Role-based access", "• Financial protection", "• Session auto-close", "• Admin vault route"], False, C_NAVY_BG)
    ]

    x_start = 120
    f_mod_t = get_font(22, bold=True)
    f_mod_b = get_font(18)

    for title, items, is_highlight, col in modules:
        bg_col = C_TEAL_DARK if is_highlight else C_WHITE
        border_col = C_TEAL_DARK if is_highlight else C_BORDER
        txt_col = C_WHITE if is_highlight else C_DARK
        body_col = C_TEAL_LIGHT if is_highlight else C_GRAY_TXT

        d.rounded_rectangle([(x_start, 240), (x_start + 310, 880)], radius=16, fill=bg_col, outline=border_col, width=2)
        
        # Circle icon
        ic_col = C_CYAN_BRIGHT if is_highlight else col
        d.ellipse([(x_start + 115, 290), (x_start + 195, 370)], fill=ic_col)

        # Title
        d.text((x_start + 35, 410), title, fill=txt_col, font=f_mod_t)

        # Items
        y_item = 480
        for itm in items:
            d.text((x_start + 35, y_item), itm, fill=body_col, font=f_mod_b)
            y_item += 45

        x_start += 340

    return img

def create_slide_7():
    # DFD LEVEL 0 (Context Diagram) - Pixel-Perfect Layout
    img = Image.new("RGB", (W, H), C_LIGHT_BG)
    d = ImageDraw.Draw(img)
    draw_standard_header(d, "System Modeling", "Data Flow Diagram — Level 0 (Context Diagram)", 7)

    f_box_t = get_font(18, bold=True)
    f_box_d = get_font(15)
    f_pill = get_font(14, bold=True)

    # 1. External Entity 1: Cashier (Top Left)
    d.rounded_rectangle([(100, 200), (520, 390)], radius=12, fill=C_WHITE, outline=C_TEAL, width=2)
    d.rounded_rectangle([(100, 200), (520, 245)], radius=12, fill=C_TEAL)
    d.text((120, 212), "COUNTER CASHIER / PHARMACIST", fill=C_WHITE, font=f_box_t)
    d.text((120, 260), "• Barcode / Product queries", fill=C_GRAY_TXT, font=f_box_d)
    d.text((120, 295), "• Customer mobile & Cart items", fill=C_GRAY_TXT, font=f_box_d)
    d.text((120, 330), "• Bill requests & Return verification", fill=C_GRAY_TXT, font=f_box_d)

    # 2. External Entity 2: Store Manager / Admin (Top Right)
    d.rounded_rectangle([(1400, 200), (1820, 390)], radius=12, fill=C_WHITE, outline=C_NAVY_BG, width=2)
    d.rounded_rectangle([(1400, 200), (1820, 245)], radius=12, fill=C_NAVY_BG)
    d.text((1420, 212), "STORE MANAGER / ADMIN", fill=C_WHITE, font=f_box_t)
    d.text((1420, 260), "• New stock batch & Supplier entry", fill=C_GRAY_TXT, font=f_box_d)
    d.text((1420, 295), "• RBAC role configuration", fill=C_GRAY_TXT, font=f_box_d)
    d.text((1420, 330), "• BI inquiries & Low-stock PO export", fill=C_GRAY_TXT, font=f_box_d)

    # 3. External Entity 3: Customer (Bottom Left)
    d.rounded_rectangle([(100, 670), (520, 860)], radius=12, fill=C_WHITE, outline=C_GREEN, width=2)
    d.rounded_rectangle([(100, 670), (520, 715)], radius=12, fill=C_GREEN)
    d.text((120, 682), "CUSTOMER / PATIENT", fill=C_WHITE, font=f_box_t)
    d.text((120, 730), "• Prescription details & Phone number", fill=C_GRAY_TXT, font=f_box_d)
    d.text((120, 765), "• Cash / UPI payment", fill=C_GRAY_TXT, font=f_box_d)
    d.text((120, 800), "• Return item with receipt barcode", fill=C_GRAY_TXT, font=f_box_d)

    # 4. External Entity 4: Supplier (Bottom Right)
    d.rounded_rectangle([(1400, 670), (1820, 860)], radius=12, fill=C_WHITE, outline=C_AMBER, width=2)
    d.rounded_rectangle([(1400, 670), (1820, 715)], radius=12, fill=C_AMBER)
    d.text((1420, 682), "SUPPLIER / WHOLESALER", fill=C_WHITE, font=f_box_t)
    d.text((1420, 730), "• Medicine batch consignments", fill=C_GRAY_TXT, font=f_box_d)
    d.text((1420, 765), "• Invoices, purchase price, MRP", fill=C_GRAY_TXT, font=f_box_d)
    d.text((1420, 800), "• Automated reorder CSV purchase orders", fill=C_GRAY_TXT, font=f_box_d)

    # Central System Node 0.0
    d.rounded_rectangle([(680, 360), (1240, 700)], radius=24, fill=C_NAVY_BG, outline=C_TEAL, width=3)
    f_sys_num = get_font(26, bold=True)
    d.text((930, 395), "0.0", fill=C_CYAN_BRIGHT, font=f_sys_num)

    f_sys_t = get_font(27, bold=True)
    d.text((740, 455), "PHARMACY MANAGEMENT", fill=C_WHITE, font=f_sys_t)
    d.text((815, 500), "ERP SYSTEM", fill=C_WHITE, font=f_sys_t)

    f_sys_d = get_font(18)
    d.text((755, 575), "Central Cloud & Database Engine", fill="#a5f3fc", font=f_sys_d)
    d.text((765, 615), "POS • FEFO • GST • CRM • Reverse Logistics", fill="#cce8e8", font=get_font(16))

    # Flow Labels on crisp pill badges
    # Top-Left Flows
    d.rounded_rectangle([(550, 235), (820, 280)], radius=8, fill=C_WHITE, outline=C_TEAL, width=1)
    d.text((575, 248), "Sales Data / Scans  ->", fill=C_TEAL, font=f_pill)
    d.line([(520, 257), (550, 257)], fill=C_TEAL, width=2)
    d.line([(820, 257), (870, 257), (870, 360)], fill=C_TEAL, width=2)

    d.rounded_rectangle([(550, 310), (820, 355)], radius=8, fill=C_WHITE, outline=C_CYAN, width=1)
    d.text((575, 323), "<-  Thermal Bill / Alerts", fill=C_CYAN, font=f_pill)
    d.line([(520, 332), (550, 332)], fill=C_CYAN, width=2)
    d.line([(820, 332), (830, 332), (830, 360)], fill=C_CYAN, width=2)

    # Top-Right Flows
    d.rounded_rectangle([(1100, 235), (1370, 280)], radius=8, fill=C_WHITE, outline=C_NAVY_BG, width=1)
    d.text((1125, 248), "<-  Stock Entry / Roles", fill=C_NAVY_BG, font=f_pill)
    d.line([(1370, 257), (1400, 257)], fill=C_NAVY_BG, width=2)
    d.line([(1100, 257), (1050, 257), (1050, 360)], fill=C_NAVY_BG, width=2)

    d.rounded_rectangle([(1100, 310), (1370, 355)], radius=8, fill=C_WHITE, outline=C_AMBER, width=1)
    d.text((1125, 323), "BI Analytics / POs  ->", fill=C_AMBER, font=f_pill)
    d.line([(1370, 332), (1400, 332)], fill=C_AMBER, width=2)
    d.line([(1100, 332), (1090, 332), (1090, 360)], fill=C_AMBER, width=2)

    # Bottom-Left Flows
    d.rounded_rectangle([(550, 705), (820, 750)], radius=8, fill=C_WHITE, outline=C_GREEN, width=1)
    d.text((575, 718), "Prescription / Cash  ->", fill=C_GREEN, font=f_pill)
    d.line([(520, 727), (550, 727)], fill=C_GREEN, width=2)
    d.line([(820, 727), (830, 727), (830, 700)], fill=C_GREEN, width=2)

    d.rounded_rectangle([(550, 780), (820, 825)], radius=8, fill=C_WHITE, outline=C_CYAN, width=1)
    d.text((575, 793), "<-  Invoice / Refunds", fill=C_CYAN, font=f_pill)
    d.line([(520, 802), (550, 802)], fill=C_CYAN, width=2)
    d.line([(820, 802), (870, 802), (870, 700)], fill=C_CYAN, width=2)

    # Bottom-Right Flows
    d.rounded_rectangle([(1100, 705), (1370, 750)], radius=8, fill=C_WHITE, outline=C_AMBER, width=1)
    d.text((1125, 718), "<-  Batch Invoices", fill=C_AMBER, font=f_pill)
    d.line([(1370, 727), (1400, 727)], fill=C_AMBER, width=2)
    d.line([(1100, 727), (1090, 727), (1090, 700)], fill=C_AMBER, width=2)

    d.rounded_rectangle([(1100, 780), (1370, 825)], radius=8, fill=C_WHITE, outline=C_TEAL, width=1)
    d.text((1125, 793), "Reorder POs (CSV)  ->", fill=C_TEAL, font=f_pill)
    d.line([(1370, 802), (1400, 802)], fill=C_TEAL, width=2)
    d.line([(1100, 802), (1050, 802), (1050, 700)], fill=C_TEAL, width=2)

    # Bottom context note
    d.rounded_rectangle([(320, 930), (1600, 990)], radius=10, fill=C_WHITE, outline=C_BORDER, width=1)
    f_ctx = get_font(16)
    d.text((360, 948), "Level 0 Scope: Encapsulates human interaction roles, wholesale supply-chain, and POS transaction boundary.", fill=C_MUTED, font=f_ctx)

    return img

def create_slide_8():
    # DFD LEVEL 1 (Decomposition Diagram) - Pixel-Perfect Layout
    img = Image.new("RGB", (W, H), C_LIGHT_BG)
    d = ImageDraw.Draw(img)
    draw_standard_header(d, "System Modeling", "Data Flow Diagram — Level 1 (Decomposition Diagram)", 8)

    processes = [
        ("1.0", "Authentication & RBAC Control", "Validates login against User/Group models; routes to Admin, Manager, or Cashier UI.", "[Auth_User]", C_NAVY_BG),
        ("2.0", "POS & Reverse GST Billing Engine", "Accepts barcode/search input; calculates GST dynamically; creates Sale record.", "[D1, D2 -> D3]", C_TEAL),
        ("3.0", "FEFO Batch Inventory Dispatch", "Sorts stock by expiry_date; deducts sold units; triggers Signals on deletion.", "[D2 Stock]", C_GREEN),
        ("4.0", "Reverse Logistics (Returns Desk)", "Scans receipt barcode; validates bill items; restocks physical units; logs audit.", "[D3 -> D2, D4]", C_AMBER),
        ("5.0", "Smart CRM & Customer Directory", "Executes AJAX telephone lookup; links customer to doctor and spend total.", "[D5 Customer]", C_CYAN),
        ("6.0", "Procurement & Reorder Engine", "Evaluates batch stocks against minimum_stock_level; exports CSV reorder PO.", "[D1, D2 -> PO]", C_DARK),
        ("7.0", "Financial BI & Analytics Engine", "Aggregates daily sales, profit margins, GST totals, and payment modes.", "[D3 Ledger]", C_RED),
    ]

    f_p_num = get_font(16, bold=True)
    f_p_t = get_font(18, bold=True)
    f_p_d = get_font(14)
    f_tag = get_font(12, bold=True)

    y = 215
    for p_num, p_title, p_desc, store_tag, col in processes:
        d.rounded_rectangle([(100, y), (1040, y + 84)], radius=8, fill=C_WHITE, outline=C_BORDER, width=1)
        
        # Number bubble
        d.rounded_rectangle([(115, y + 15), (185, y + 69)], radius=6, fill=col)
        d.text((130, y + 28), p_num, fill=C_WHITE, font=f_p_num)

        # Title
        d.text((205, y + 16), p_title, fill=C_DARK, font=f_p_t)
        d.text((205, y + 46), p_desc, fill=C_GRAY_TXT, font=f_p_d)

        # Data store interaction tag
        d.rounded_rectangle([(890, y + 25), (1020, y + 59)], radius=4, fill="#f1f5f9", outline=C_BORDER)
        d.text((905, y + 33), store_tag, fill=col, font=f_tag)

        y += 95

    # Data Stores (Right Column)
    d.rounded_rectangle([(1100, 215), (1820, 265)], radius=8, fill=C_NAVY_BG)
    f_ds_head = get_font(15, bold=True)
    d.text((1170, 230), "DATABASE DATA STORES (RELATIONAL REPOSITORY)", fill=C_CYAN_BRIGHT, font=f_ds_head)

    data_stores = [
        ("D1", "Medicine Catalog Table", "Attributes: barcode, name, category, pack_size, gst%, min_stock."),
        ("D2", "Stock Batches Table", "Attributes: medicine_id, batch_no, expiry_date, quantity, purchase_price, mrp."),
        ("D3", "Sale Ledger Table", "Attributes: bill_no, stock_id, quantity, total_price, customer_id, payment_method, date."),
        ("D4", "ReturnSale Audit Table", "Attributes: sale_id, stock_id, quantity_returned, refund_amount, reason, restocked."),
        ("D5", "Customer CRM Table", "Attributes: name, phone (unique), last_doctor, cumulative purchase history."),
        ("D6", "Supplier Directory Table", "Attributes: name, contact_person, phone, email, address.")
    ]

    f_ds_id = get_font(16, bold=True)
    f_ds_t = get_font(17, bold=True)
    f_ds_d = get_font(13)

    y_ds = 285
    for ds_id, ds_t, ds_d in data_stores:
        d.rounded_rectangle([(1100, y_ds), (1820, y_ds + 92)], radius=8, fill=C_WHITE, outline=C_TEAL, width=2)
        d.rectangle([(1102, y_ds + 2), (1175, y_ds + 90)], fill=C_TEAL)
        d.text((1123, y_ds + 32), ds_id, fill=C_WHITE, font=f_ds_id)

        d.text((1195, y_ds + 16), ds_t, fill=C_DARK, font=f_ds_t)
        d.text((1195, y_ds + 48), ds_d, fill=C_GRAY_TXT, font=f_ds_d)
        y_ds += 105

    return img

def create_slide_9():
    # Working Model (Methodology)
    img = Image.new("RGB", (W, H), C_LIGHT_BG)
    d = ImageDraw.Draw(img)
    draw_standard_header(d, "Methodology", "PHARMACY ERP — Working Model", 9)

    # Left Model Flow
    flow_steps = [
        "User",
        "Frontend — HTML / CSS / JS / Bootstrap",
        "Django — Views & Business Logic",
        "Django ORM",
        "SQLite Database",
        "Result / Data returned to User"
    ]

    f_fl = get_font(18, bold=True)
    y = 230
    for i, st in enumerate(flow_steps):
        is_last = (i == len(flow_steps) - 1)
        bg = "#00c49f" if is_last else C_NAVY_BG
        txt_col = C_DARK if is_last else C_WHITE
        d.rounded_rectangle([(120, y), (820, y + 68)], radius=12, fill=bg)
        d.ellipse([(140, y + 14), (180, y + 54)], fill=C_WHITE)
        d.text((205, y + 20), st, fill=txt_col, font=f_fl)
        
        if i < len(flow_steps) - 1:
            d.polygon([(465, y + 74), (475, y + 74), (470, y + 84)], fill=C_MUTED)
        y += 95

    # Right Example Workflow Container
    d.rounded_rectangle([(920, 220), (1800, 880)], radius=16, fill="#e6f2f2", outline=C_BORDER, width=1)
    f_wf_head = get_font(16, bold=True)
    d.text((1120, 260), "E X A M P L E   —   B I L L I N G   W O R K F L O W", fill=C_TEAL, font=f_wf_head)

    workflow = [
        "1  Select / scan medicine",
        "2  Retrieve batch information",
        "3  Apply FEFO logic",
        "4  Calculate GST",
        "5  Create sale record",
        "6  Update inventory",
        "7  Generate bill"
    ]

    f_wf = get_font(20, bold=True)
    y_wf = 330
    for item in workflow:
        num = item[0]
        text = item[3:]
        d.ellipse([(980, y_wf), (1030, y_wf + 50)], fill=C_NAVY_BG)
        d.text((1000, y_wf + 10), num, fill=C_WHITE, font=f_wf)
        d.text((1060, y_wf + 12), text, fill=C_DARK, font=f_wf)
        y_wf += 75

    return img

def create_slide_10():
    # Three-Tier Architecture
    img = Image.new("RGB", (W, H), C_LIGHT_BG)
    d = ImageDraw.Draw(img)
    draw_standard_header(d, "System Architecture", "Three-Tier Modular Architecture", 10)

    # 3 Layers on Left
    layers = [
        ("Presentation Layer", ["HTML5", "CSS3", "Bootstrap 5", "JavaScript", "AJAX"]),
        ("Application Layer", ["Python", "Django", "Views & Business Logic", "Auth & Authorization", "Django ORM"]),
        ("Data Layer", ["SQLite", "Relational Models", "Master Data", "Transactional Data"])
    ]

    f_lay_t = get_font(22, bold=True)
    f_pill = get_font(17)

    y = 230
    for l_title, pills in layers:
        d.rounded_rectangle([(120, y), (1150, y + 175)], radius=14, fill=C_NAVY_BG)
        d.text((150, y + 20), l_title, fill=C_WHITE, font=f_lay_t)

        x_p = 150
        y_p = y + 75
        for p in pills:
            p_len = len(p) * 11 + 30
            d.rounded_rectangle([(x_p, y_p), (x_p + p_len, y_p + 45)], radius=6, fill=C_NAVY_ACCENT)
            d.text((x_p + 15, y_p + 10), p, fill=C_WHITE, font=f_pill)
            x_p += p_len + 15
        
        if y < 500:
            d.polygon([(630, y + 185), (640, y + 185), (635, y + 195)], fill=C_MUTED)
        y += 220

    # Right Supporting Technologies
    d.rounded_rectangle([(1230, 230), (1800, 840)], radius=16, fill=C_WHITE, outline=C_BORDER, width=1)
    f_tech_head = get_font(16, bold=True)
    d.text((1270, 270), "S U P P O R T I N G   T E C H N O L O G I E S", fill=C_TEAL, font=f_tech_head)

    techs = ["Select2", "JsBarcode", "Chart.js", "python-dotenv"]
    f_tech_item = get_font(20)
    y_t = 330
    for t in techs:
        d.ellipse([(1270, y_t + 8), (1284, y_t + 22)], fill=C_CYAN)
        d.text((1310, y_t), t, fill=C_DARK, font=f_tech_item)
        y_t += 55

    d.text((1270, 580), "D E P L O Y M E N T", fill=C_TEAL, font=f_tech_head)
    deps = ["PythonAnywhere", "Django WSGI"]
    y_d = 640
    for dp in deps:
        d.ellipse([(1270, y_d + 8), (1284, y_d + 22)], fill=C_CYAN)
        d.text((1310, y_d), dp, fill=C_DARK, font=f_tech_item)
        y_d += 55

    return img

def create_slide_11():
    # Technology Stack Table
    img = Image.new("RGB", (W, H), C_LIGHT_BG)
    d = ImageDraw.Draw(img)
    draw_standard_header(d, "Tools & Technologies", "Technology Stack", 11)

    table_data = [
        ("Programming Language", "Python 3.14", "Asynchronous Requests", "AJAX"),
        ("Backend", "Django 6.0.4", "Search", "Select2"),
        ("Database", "SQLite", "Barcode", "JsBarcode"),
        ("ORM", "Django ORM", "Visualization", "Chart.js"),
        ("Frontend", "HTML5, CSS3", "Configuration", "python-dotenv"),
        ("UI Framework", "Bootstrap 5", "Deployment", "PythonAnywhere"),
        ("Client-side Scripting", "Vanilla JavaScript (ES6)", "Server Interface", "Django WSGI")
    ]

    # Table Header
    d.rounded_rectangle([(120, 220), (920, 280)], radius=8, fill=C_NAVY_BG)
    d.rounded_rectangle([(960, 220), (1800, 280)], radius=8, fill=C_NAVY_BG)

    f_th = get_font(18, bold=True)
    d.text((150, 238), "Layer", fill=C_WHITE, font=f_th)
    d.text((500, 238), "Technologies", fill=C_WHITE, font=f_th)

    d.text((990, 238), "Layer", fill=C_WHITE, font=f_th)
    d.text((1380, 238), "Technologies", fill=C_WHITE, font=f_th)

    f_td1 = get_font(18, bold=True)
    f_td2 = get_font(18)

    y = 295
    for l1, t1, l2, t2 in table_data:
        bg = "#f8fafc" if (y % 2 == 0) else C_WHITE
        d.rounded_rectangle([(120, y), (920, y + 65)], radius=6, fill=bg, outline=C_BORDER, width=1)
        d.text((150, y + 18), l1, fill=C_DARK, font=f_td1)
        d.text((500, y + 18), t1, fill=C_GRAY_TXT, font=f_td2)

        d.rounded_rectangle([(960, y), (1800, y + 65)], radius=6, fill=bg, outline=C_BORDER, width=1)
        d.text((990, y + 18), l2, fill=C_DARK, font=f_td1)
        d.text((1380, y + 18), t2, fill=C_GRAY_TXT, font=f_td2)
        y += 75

    return img

def create_slide_12():
    # Key Technical Features
    img = Image.new("RGB", (W, H), C_LIGHT_BG)
    d = ImageDraw.Draw(img)
    draw_standard_header(d, "Key Technical Features", "Where the Technical Depth Shows", 12)

    features = [
        ("FEFO Algorithm", "Prioritizes earliest-expiring medicine batches automatically.", C_TEAL),
        ("AJAX Operations", "Enables asynchronous customer lookup and master-data creation.", C_CYAN),
        ("Dynamic GST", "Performs GST-aware billing calculations in real time.", C_TEAL_DARK),
        ("Django Signals", "Synchronizes inventory automatically when transactions change.", C_NAVY_BG),
        ("RBAC", "Separates access between Owner, Manager, and Cashier roles.", C_AMBER),
        ("Business Intelligence", "Converts sales data into revenue, profit and inventory insights.", C_RED)
    ]

    coords = [
        (120, 220), (690, 220), (1260, 220),
        (120, 560), (690, 560), (1260, 560)
    ]

    f_t = get_font(24, bold=True)
    f_d = get_font(18)

    for (title, desc, col), (x, y) in zip(features, coords):
        d.rounded_rectangle([(x, y), (x + 540, y + 290)], radius=14, fill=C_WHITE, outline=C_BORDER, width=1)
        
        # Circle Icon
        d.ellipse([(x + 35, y + 35), (x + 105, y + 105)], fill=col)
        # Inner symbol
        d.ellipse([(x + 55, y + 55), (x + 85, y + 85)], fill=C_WHITE)

        # Title
        d.text((x + 35, y + 135), title, fill=C_DARK, font=f_t)

        # Description wrapped
        words = desc.split()
        line = ""
        dy = y + 185
        for w in words:
            if len(line + " " + w) < 36:
                line = (line + " " + w).strip()
            else:
                d.text((x + 35, dy), line, fill=C_GRAY_TXT, font=f_d)
                dy += 28
                line = w
        if line:
            d.text((x + 35, dy), line, fill=C_GRAY_TXT, font=f_d)

    return img

def create_slide_13():
    # Applications
    img = Image.new("RGB", (W, H), C_LIGHT_BG)
    d = ImageDraw.Draw(img)
    draw_standard_header(d, "Applications", "Applications of Pharmacy ERP", 13)

    # Left Container (Primary)
    d.rounded_rectangle([(120, 220), (920, 860)], radius=18, fill=C_NAVY_BG)
    d.ellipse([(160, 260), (230, 330)], fill="#00c49f")
    d.rounded_rectangle([(180, 280), (210, 310)], radius=4, fill=C_WHITE)

    f_p_tag = get_font(16, bold=True)
    d.text((160, 360), "P R I M A R Y   A P P L I C A T I O N", fill="#7dd3fc", font=f_p_tag)

    f_scope = get_font(28, bold=True)
    d.text((160, 410), "Current project scope", fill=C_WHITE, font=f_scope)

    scopes = ["Retail pharmacies", "Medical stores", "Independent pharmacy businesses"]
    f_sc_item = get_font(22)
    y_sc = 520
    for s in scopes:
        d.ellipse([(160, y_sc + 8), (180, y_sc + 28)], fill=C_WHITE)
        d.text((210, y_sc), s, fill=C_WHITE, font=f_sc_item)
        y_sc += 80

    # Right Container (Extended)
    d.rounded_rectangle([(1000, 220), (1800, 860)], radius=18, fill=C_WHITE, outline=C_BORDER, width=1)
    d.ellipse([(1050, 260), (1120, 330)], fill=C_NAVY_BG)
    d.ellipse([(1075, 285), (1095, 305)], fill=C_WHITE)

    d.text((1050, 360), "P O T E N T I A L   E X T E N D E D   A P P L I C A T I O N S", fill=C_TEAL, font=f_p_tag)

    f_fut = get_font(28, bold=True)
    d.text((1050, 410), "Future growth directions", fill=C_DARK, font=f_fut)

    ext = [
        "Multi-branch pharmacy management",
        "Pharmacy chain operations",
        "Centralized inventory monitoring",
        "Pharmacy-owner business analytics",
        "Mobile-based pharmacy management"
    ]
    f_ext_item = get_font(21)
    y_ex = 500
    for e in ext:
        d.ellipse([(1050, y_ex + 8), (1064, y_ex + 22)], fill=C_CYAN)
        d.text((1090, y_ex), e, fill=C_DARK, font=f_ext_item)
        y_ex += 65

    return img

def create_slide_14():
    # Timeline
    img = Image.new("RGB", (W, H), C_LIGHT_BG)
    d = ImageDraw.Draw(img)
    draw_standard_header(d, "Project Timeline", "Development Progression", 14)

    f_sub = get_font(18, italic=True)
    d.text((120, 175), "Actual build sequence of the already-developed project (replace with real dates if available).", fill=C_MUTED, font=f_sub)

    steps_row1 = [
        ("1", "Requirement Analysis"),
        ("2", "System Design & Database Modeling"),
        ("3", "Backend Development (Django)"),
        ("4", "Frontend & POS Development"),
        ("5", "Inventory & FEFO Implementation"),
        ("6", "CRM & AJAX Integration")
    ]

    steps_row2 = [
        ("7", "BI Dashboard & Financial Modules"),
        ("8", "Security & RBAC"),
        ("9", "Testing & Bug Fixing"),
        ("10", "Cloud Deployment"),
        ("11", "Documentation & Presentation")
    ]

    f_num = get_font(20, bold=True)
    f_card = get_font(15, bold=True)

    # Row 1
    x = 120
    for num, txt in steps_row1:
        d.ellipse([(x + 95, 270), (x + 145, 320)], fill=C_NAVY_BG)
        d.text((x + 112, 280), num, fill=C_WHITE, font=f_num)

        d.rounded_rectangle([(x, 350), (x + 240, 480)], radius=10, fill=C_WHITE, outline=C_BORDER, width=1)
        
        words = txt.split()
        line = ""
        dy = 375
        for w in words:
            if len(line + " " + w) < 18:
                line = (line + " " + w).strip()
            else:
                d.text((x + 15, dy), line, fill=C_DARK, font=f_card)
                dy += 24
                line = w
        if line:
            d.text((x + 15, dy), line, fill=C_DARK, font=f_card)

        x += 280

    # Row 2
    x = 260
    for num, txt in steps_row2:
        d.ellipse([(x + 95, 590), (x + 145, 640)], fill=C_TEAL)
        d.text((x + 105 if len(num) > 1 else x + 112, 600), num, fill=C_WHITE, font=f_num)

        d.rounded_rectangle([(x, 670), (x + 240, 800)], radius=10, fill=C_WHITE, outline=C_BORDER, width=1)

        words = txt.split()
        line = ""
        dy = 695
        for w in words:
            if len(line + " " + w) < 18:
                line = (line + " " + w).strip()
            else:
                d.text((x + 15, dy), line, fill=C_DARK, font=f_card)
                dy += 24
                line = w
        if line:
            d.text((x + 15, dy), line, fill=C_DARK, font=f_card)

        x += 280

    return img

def create_slide_15():
    # Future Scope
    img = Image.new("RGB", (W, H), C_LIGHT_BG)
    d = ImageDraw.Draw(img)
    draw_standard_header(d, "Future Scope", "Phase 2 Roadmap", 15)

    cards = [
        ("AI & Machine Learning", ["• Prescription OCR", "• Medicine demand forecasting", "• Seasonal shortage prediction"], C_NAVY_BG),
        ("Mobile & API", ["• Django REST Framework", "• Mobile app for pharmacy owners", "• Bluetooth receipt printer sync"], C_TEAL),
        ("Communication Automation", ["• WhatsApp Business integration", "• Digital receipt delivery", "• Automated supplier alerts"], C_CYAN),
        ("Cloud & DevOps", ["• PostgreSQL migration", "• Docker containerization", "• CI/CD pipeline", "• Scalable cloud deployment"], C_DARK)
    ]

    coords = [
        (120, 230), (1000, 230),
        (120, 560), (1000, 560)
    ]

    f_t = get_font(26, bold=True)
    f_item = get_font(20)

    for (title, items, col), (x, y) in zip(cards, coords):
        d.rounded_rectangle([(x, y), (x + 800, y + 290)], radius=16, fill=C_WHITE, outline=C_BORDER, width=1)
        
        # Circle icon
        d.ellipse([(x + 40, y + 40), (x + 110, y + 110)], fill=col)
        d.ellipse([(x + 65, y + 65), (x + 85, y + 85)], fill=C_WHITE)

        # Title
        d.text((x + 140, y + 55), title, fill=C_DARK, font=f_t)

        # Items
        y_it = y + 140
        for itm in items:
            d.text((x + 50, y_it), itm, fill=C_GRAY_TXT, font=f_item)
            y_it += 42

    return img

def create_slide_16():
    # Conclusion
    img = Image.new("RGB", (W, H), C_NAVY_BG)
    d = ImageDraw.Draw(img)

    f_tag = get_font(16, bold=True)
    d.text((120, 75), "C O N C L U S I O N", fill="#7dd3fc", font=f_tag)

    f_title = get_font(42, bold=True)
    d.text((120, 120), "Pharmacy ERP, in Summary", fill=C_WHITE, font=f_title)

    points = [
        "Provides an integrated ERP solution for end-to-end pharmacy operations.",
        "Combines billing, inventory, CRM, financial processing, analytics and security.",
        "Batch-level inventory management and FEFO improve stock handling.",
        "AJAX-based workflows improve operational efficiency.",
        "BI dashboards provide better business visibility.",
        "RBAC provides controlled access to system functionality.",
        "Cloud deployment makes the application accessible beyond local development."
    ]

    f_pt = get_font(21)
    y = 230
    for pt in points:
        d.ellipse([(120, y + 4), (160, y + 44)], fill="#00c49f")
        # Checkmark
        d.line([(132, y + 24), (140, y + 32)], fill=C_WHITE, width=4)
        d.line([(140, y + 32), (150, y + 16)], fill=C_WHITE, width=4)

        d.text((185, y + 10), pt, fill=C_WHITE, font=f_pt)
        y += 85

    # Bottom Highlight Quote
    f_quote = get_font(24, bold=True, italic=True)
    d.text((120, 910), "PHARMACY ERP transforms fragmented pharmacy operations into a centralized digital", fill="#7dd3fc", font=f_quote)
    d.text((120, 950), "management workflow.", fill="#7dd3fc", font=f_quote)

    return img

def render_all_slides():
    print("Generating all 16 presentation slides in 1920x1080 resolution...")
    slides = [
        create_slide_1(),
        create_slide_2(),
        create_slide_3(),
        create_slide_4(),
        create_slide_5(),
        create_slide_6(),
        create_slide_7(),
        create_slide_8(),
        create_slide_9(),
        create_slide_10(),
        create_slide_11(),
        create_slide_12(),
        create_slide_13(),
        create_slide_14(),
        create_slide_15(),
        create_slide_16()
    ]

    out_pdf = "Pharmacy_Management_ERP_Major_Project.pdf"
    slides[0].save(
        out_pdf,
        "PDF",
        resolution=100.0,
        save_all=True,
        append_images=slides[1:]
    )
    print(f"SUCCESS: Created pixel-perfect 16-slide PDF at {out_pdf}")

if __name__ == '__main__':
    render_all_slides()
