import math
from PIL import Image, ImageDraw, ImageFont

W = 2400
H = 1800

FONT_BOLD = "C:/Windows/Fonts/segoeuib.ttf"
FONT_REG = "C:/Windows/Fonts/segoeui.ttf"
FONT_ITALIC = "C:/Windows/Fonts/segoeuii.ttf"

def get_font(size, bold=False, italic=False):
    f_path = FONT_BOLD if bold else (FONT_ITALIC if italic else FONT_REG)
    return ImageFont.truetype(f_path, size)

def draw_quadratic_curve(d, p0, p1, p2, color="black", width=3, num_points=100):
    points = []
    for i in range(num_points + 1):
        t = i / float(num_points)
        x = (1 - t)**2 * p0[0] + 2 * (1 - t) * t * p1[0] + t**2 * p2[0]
        y = (1 - t)**2 * p0[1] + 2 * (1 - t) * t * p1[1] + t**2 * p2[1]
        points.append((x, y))
    d.line(points, fill=color, width=width)
    return points

def draw_arrowhead(d, tip, angle, size=20, color="black"):
    # angle in radians pointing in direction of flow
    left_angle = angle + math.pi - math.radians(25)
    right_angle = angle + math.pi + math.radians(25)
    
    p_left = (tip[0] + size * math.cos(left_angle), tip[1] + size * math.sin(left_angle))
    p_right = (tip[0] + size * math.cos(right_angle), tip[1] + size * math.sin(right_angle))
    
    d.polygon([tip, p_left, p_right], fill=color)

def generate_dfd0():
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)

    f_title = get_font(32, bold=True)
    f_sub = get_font(20)
    f_entity = get_font(26, bold=True)
    f_sys = get_font(28, bold=True)
    f_label = get_font(20, bold=False)

    # Main Header at the top
    d.text((120, 60), "DATA FLOW DIAGRAM (DFD) — LEVEL 0", fill="#111827", font=f_title)
    d.text((120, 110), "Context Level Diagram for Pharmacy Management ERP System", fill="#4b5563", font=f_sub)
    d.line([(120, 150), (W - 120, 150)], fill="#d1d5db", width=2)

    # 1. CENTER: SYSTEM (Circle)
    cx, cy = 1200, 950
    r = 160
    d.ellipse([(cx - r, cy - r), (cx + r, cy + r)], outline="black", width=3, fill="white")
    
    # Text inside Center Circle
    d.text((cx - 85, cy - 35), "Pharmacy ERP", fill="black", font=f_sys)
    d.text((cx - 45, cy + 5), "System", fill="black", font=f_sys)

    # 2. TOP ENTITY: Administrator (Box)
    admin_x1, admin_y1 = 1040, 230
    admin_x2, admin_y2 = 1360, 390
    d.rectangle([(admin_x1, admin_y1), (admin_x2, admin_y2)], outline="black", width=3, fill="white")
    d.text((admin_x1 + 45, admin_y1 + 55), "Administrator", fill="black", font=f_entity)

    # 3. TOP-LEFT: Database (Open-ended rectangle / DFD Data Store)
    db_x1, db_y1 = 440, 250
    db_x2, db_y2 = 780, 370
    # DFD Data Store: Top line, Bottom line, Left line (open on right)
    d.line([(db_x1, db_y1), (db_x2, db_y1)], fill="black", width=3)
    d.line([(db_x1, db_y2), (db_x2, db_y2)], fill="black", width=3)
    d.line([(db_x1, db_y1), (db_x1, db_y2)], fill="black", width=3)
    d.text((db_x1 + 60, db_y1 + 40), "Database", fill="black", font=f_entity)

    # Arrows between Database and Administrator
    # Arrow 1: Admin -> Database (top arrow)
    d.line([(admin_x1, 280), (db_x2, 280)], fill="black", width=3)
    draw_arrowhead(d, (db_x2, 280), math.pi, size=18)
    d.text((810, 245), "Store / Update Data", fill="#1f2937", font=get_font(18))

    # Arrow 2: Database -> Admin (bottom arrow)
    d.line([(db_x2, 340), (admin_x1, 340)], fill="black", width=3)
    draw_arrowhead(d, (admin_x1, 340), 0, size=18)
    d.text((810, 350), "Retrieve Records", fill="#1f2937", font=get_font(18))

    # 4. LEFT ENTITY: Medicine Supplier (Box)
    sup_x1, sup_y1 = 200, 860
    sup_x2, sup_y2 = 540, 1020
    d.rectangle([(sup_x1, sup_y1), (sup_x2, sup_y2)], outline="black", width=3, fill="white")
    d.text((sup_x1 + 40, sup_y1 + 45), "Medicine Supplier", fill="black", font=f_entity)
    d.text((sup_x1 + 80, sup_y1 + 85), "/ Wholesaler", fill="#4b5563", font=get_font(20))

    # 5. RIGHT ENTITY: Pharmacist / Cashier (User Box)
    user_x1, user_y1 = 1860, 860
    user_x2, user_y2 = 2200, 1020
    d.rectangle([(user_x1, user_y1), (user_x2, user_y2)], outline="black", width=3, fill="white")
    d.text((user_x1 + 45, user_y1 + 45), "Pharmacist / Cashier", fill="black", font=f_entity)
    d.text((user_x1 + 105, user_y1 + 85), "(POS User)", fill="#4b5563", font=get_font(20))

    # 6. BOTTOM ENTITY: Customer / Patient (Visitor Box)
    cust_x1, cust_y1 = 1040, 1510
    cust_x2, cust_y2 = 1360, 1670
    d.rectangle([(cust_x1, cust_y1), (cust_x2, cust_y2)], outline="black", width=3, fill="white")
    d.text((cust_x1 + 35, cust_y1 + 45), "Customer / Patient", fill="black", font=f_entity)
    d.text((cust_x1 + 105, cust_y1 + 85), "(Buyer)", fill="#4b5563", font=get_font(20))

    # =========================================================================
    # CURVED FLOW ARROWS WITH EXACT TEXT LABELS
    # =========================================================================

    # --- TOP: Administrator <---> System ---
    # Flow 1 (Left curve): Admin -> System (System / Stock Management)
    p0 = (1140, 390)
    p1 = (1030, 580)
    p2 = (1120, 800)
    draw_quadratic_curve(d, p0, p1, p2, width=3)
    tangent_angle = math.atan2(p2[1] - p1[1], p2[0] - p1[0])
    draw_arrowhead(d, p2, tangent_angle, size=18)
    
    d.text((930, 560), "System & Stock", fill="black", font=f_label)
    d.text((945, 590), "Management", fill="black", font=f_label)

    # Flow 2 (Right curve): System -> Admin (Website Activity / Sales Analytics)
    p0 = (1280, 800)
    p1 = (1370, 580)
    p2 = (1260, 390)
    draw_quadratic_curve(d, p0, p1, p2, width=3)
    tangent_angle = math.atan2(p2[1] - p1[1], p2[0] - p1[0])
    draw_arrowhead(d, p2, tangent_angle, size=18)

    d.text((1340, 560), "Sales Analytics &", fill="black", font=f_label)
    d.text((1360, 590), "Activity Logs", fill="black", font=f_label)

    # --- LEFT: Medicine Supplier <---> System ---
    # Flow 3 (Upper curve): Supplier -> System (Medicine & Batch Details)
    p0 = (540, 900)
    p1 = (780, 780)
    p2 = (1050, 900)
    draw_quadratic_curve(d, p0, p1, p2, width=3)
    tangent_angle = math.atan2(p2[1] - p1[1], p2[0] - p1[0])
    draw_arrowhead(d, p2, tangent_angle, size=18)

    d.text((690, 750), "Medicine & Batch Details", fill="black", font=f_label)

    # Flow 4 (Lower curve): System -> Supplier (Reorder Purchase Orders)
    p0 = (1050, 1000)
    p1 = (780, 1120)
    p2 = (540, 980)
    draw_quadratic_curve(d, p0, p1, p2, width=3)
    tangent_angle = math.atan2(p2[1] - p1[1], p2[0] - p1[0])
    draw_arrowhead(d, p2, tangent_angle, size=18)

    d.text((670, 1100), "Reorder Purchase Orders (CSV)", fill="black", font=f_label)

    # --- RIGHT: Pharmacist / Cashier <---> System ---
    # Flow 5 (Upper curve): Cashier -> System (Barcode Scan / Cart Items)
    p0 = (1860, 900)
    p1 = (1620, 780)
    p2 = (1350, 900)
    draw_quadratic_curve(d, p0, p1, p2, width=3)
    tangent_angle = math.atan2(p2[1] - p1[1], p2[0] - p1[0])
    draw_arrowhead(d, p2, tangent_angle, size=18)

    d.text((1510, 750), "Barcode Scan & Cart Items", fill="black", font=f_label)

    # Flow 6 (Lower curve): System -> Cashier (Thermal Bill & Stock Verification)
    p0 = (1350, 1000)
    p1 = (1620, 1120)
    p2 = (1860, 980)
    draw_quadratic_curve(d, p0, p1, p2, width=3)
    tangent_angle = math.atan2(p2[1] - p1[1], p2[0] - p1[0])
    draw_arrowhead(d, p2, tangent_angle, size=18)

    d.text((1460, 1090), "Thermal Bill, Receipt Barcode", fill="black", font=f_label)
    d.text((1500, 1120), "& Stock Verification", fill="black", font=f_label)

    # --- BOTTOM: Customer / Patient <---> System ---
    # Flow 7 (Left curve): Customer -> System (Prescription, Phone & Payment)
    p0 = (1140, 1510)
    p1 = (1030, 1320)
    p2 = (1120, 1100)
    draw_quadratic_curve(d, p0, p1, p2, width=3)
    tangent_angle = math.atan2(p2[1] - p1[1], p2[0] - p1[0])
    draw_arrowhead(d, p2, tangent_angle, size=18)

    d.text((880, 1300), "Prescription, Phone", fill="black", font=f_label)
    d.text((890, 1330), "& Payment (Cash/UPI)", fill="black", font=f_label)

    # Flow 8 (Right curve): System -> Customer (Invoice, Tax Bill & Refunds)
    p0 = (1280, 1100)
    p1 = (1370, 1320)
    p2 = (1260, 1510)
    draw_quadratic_curve(d, p0, p1, p2, width=3)
    tangent_angle = math.atan2(p2[1] - p1[1], p2[0] - p1[0])
    draw_arrowhead(d, p2, tangent_angle, size=18)

    d.text((1340, 1300), "Tax Invoice, Bill Receipt", fill="black", font=f_label)
    d.text((1370, 1330), "& Return Refunds", fill="black", font=f_label)

    # Footer note
    f_ft = get_font(15, italic=True)
    d.text((120, 1720), "DFD Notation: Process (Circle)  |  External Entities (Rectangles)  |  Data Store (Parallel Open Lines)  |  Data Flow (Directed Arrows)", fill="#6b7280", font=f_ft)
    d.text((W - 400, 1720), "Pharmacy ERP — Level 0", fill="#6b7280", font=f_ft)

    # Save as high-resolution PNG
    png_path = "dfd_level_0_pharmacy_erp.png"
    img.save(png_path, "PNG", dpi=(300, 300))
    print(f"SUCCESS: Saved high-res PNG to {png_path}")

    # Save as single-page PDF
    pdf_path = "dfd_level_0_pharmacy_erp.pdf"
    img.save(pdf_path, "PDF", resolution=150.0)
    print(f"SUCCESS: Saved single-page PDF to {pdf_path}")

if __name__ == '__main__':
    generate_dfd0()
