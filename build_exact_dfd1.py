import math
from PIL import Image, ImageDraw, ImageFont

W = 2800
H = 2100

FONT_BOLD = "C:/Windows/Fonts/segoeuib.ttf"
FONT_REG = "C:/Windows/Fonts/segoeui.ttf"
FONT_ITALIC = "C:/Windows/Fonts/segoeuii.ttf"

def get_font(size, bold=False, italic=False):
    f_path = FONT_BOLD if bold else (FONT_ITALIC if italic else FONT_REG)
    return ImageFont.truetype(f_path, size)

# Color Scheme matching the sample image
C_BANNER_GREEN = "#65a30d"  # Green banner
C_PROC_BG = "#bbf7d0"       # Light green process fill
C_PROC_BORDER = "#15803d"   # Dark green border
C_STORE_BG = "#dcfce7"      # Data store fill
C_STORE_BORDER = "#166534"
C_ENTITY_BG = "#f0fdf4"     # Entity box fill
C_ENTITY_BORDER = "#14532d"
C_TEXT = "#0f172a"
C_FLOW_TEXT = "#1e293b"

def draw_process(d, x, y, w, h, proc_id, title_lines):
    # Rounded rectangle with Gane & Sarson divider line near top
    d.rounded_rectangle([(x, y), (x + w, y + h)], radius=12, fill=C_PROC_BG, outline=C_PROC_BORDER, width=2)
    # Header divider
    div_y = y + int(h * 0.35)
    d.line([(x, div_y), (x + w, div_y)], fill=C_PROC_BORDER, width=2)
    
    # Process ID
    f_id = get_font(18, bold=True)
    d.draw_text = getattr(d, 'draw_text', None)
    d.text((x + w//2 - len(proc_id)*6, y + 8), proc_id, fill=C_PROC_BORDER, font=f_id)
    
    # Process Title Lines
    f_title = get_font(17, bold=True)
    start_y = div_y + 10
    for line in title_lines:
        txt_w = len(line) * 9
        d.text((x + max(12, (w - txt_w)//2), start_y), line, fill=C_TEXT, font=f_title)
        start_y += 24

def draw_entity(d, x, y, w, h, title_lines):
    d.rectangle([(x, y), (x + w, y + h)], fill=C_ENTITY_BG, outline=C_ENTITY_BORDER, width=3)
    f_ent = get_font(21, bold=True)
    start_y = y + (h - len(title_lines) * 28) // 2
    for line in title_lines:
        txt_w = len(line) * 11
        d.text((x + max(15, (w - txt_w)//2), start_y), line, fill=C_ENTITY_BORDER, font=f_ent)
        start_y += 30

def draw_data_store(d, x, y, w, h, ds_id, ds_name):
    # Open-ended rectangle with left slot
    # Top and bottom line, left border
    d.line([(x, y), (x + w, y)], fill=C_STORE_BORDER, width=3)
    d.line([(x, y + h), (x + w, y + h)], fill=C_STORE_BORDER, width=3)
    d.line([(x, y), (x, y + h)], fill=C_STORE_BORDER, width=3)
    
    # Vertical divider for ID
    div_x = x + 65
    d.line([(div_x, y), (div_x, y + h)], fill=C_STORE_BORDER, width=3)
    
    # Fill inner with light green
    d.rectangle([(x + 2, y + 2), (div_x - 2, y + h - 2)], fill=C_STORE_BG)
    d.rectangle([(div_x + 2, y + 2), (x + w - 2, y + h - 2)], fill="#f0fdf4")
    
    f_id = get_font(18, bold=True)
    d.text((x + 16, y + (h - 24)//2), ds_id, fill=C_STORE_BORDER, font=f_id)
    
    f_name = get_font(18, bold=True)
    d.text((div_x + 18, y + (h - 24)//2), ds_name, fill=C_TEXT, font=f_name)

def draw_arrow(d, p_start, p_end, label="", label_pos=None, label_above=True, color="black", width=2):
    d.line([p_start, p_end], fill=color, width=width)
    
    # Arrowhead
    angle = math.atan2(p_end[1] - p_start[1], p_end[0] - p_start[0])
    arrow_size = 14
    left_a = angle + math.pi - math.radians(25)
    right_a = angle + math.pi + math.radians(25)
    
    p_l = (p_end[0] + arrow_size * math.cos(left_a), p_end[1] + arrow_size * math.sin(left_a))
    p_r = (p_end[0] + arrow_size * math.cos(right_a), p_end[1] + arrow_size * math.sin(right_a))
    d.polygon([p_end, p_l, p_r], fill=color)
    
    # Label text
    if label:
        f_lbl = get_font(15, bold=False)
        if label_pos:
            lx, ly = label_pos
        else:
            mid_x = (p_start[0] + p_end[0]) / 2
            mid_y = (p_start[1] + p_end[1]) / 2
            offset = -22 if label_above else 8
            lx = mid_x - (len(label) * 8) / 2
            ly = mid_y + offset
        
        # Pill background for clean label reading
        lbl_w = len(label) * 9 + 12
        d.rounded_rectangle([(lx - 4, ly - 3), (lx + lbl_w, ly + 22)], radius=4, fill="#ffffff", outline="#cbd5e1", width=1)
        d.text((lx + 2, ly), label, fill=C_FLOW_TEXT, font=f_lbl)

def generate_dfd1():
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)

    # 1. TOP HEADER BANNER (Matching the sample image style)
    d.rectangle([(0, 0), (W, 190)], fill=C_BANNER_GREEN)
    f_h1 = get_font(42, bold=True)
    d.text((W//2 - 280, 45), "Requirements Analysis", fill="white", font=f_h1)
    
    f_h2 = get_font(30)
    d.text((W//2 - 380, 110), "Data Flow Diagram — Level One (Pharmacy ERP)", fill="white", font=f_h2)

    # =========================================================================
    # POSITIONS & COORDINATES
    # =========================================================================

    # ENTITY 1: Administrator (Top Center)
    draw_entity(d, 1220, 260, 320, 120, ["Administrator", "(Store Owner)"])

    # ENTITY 2: Medicine Supplier (Far Left)
    draw_entity(d, 80, 800, 300, 130, ["Medicine Supplier", "/ Wholesaler"])

    # ENTITY 3: Pharmacist / Cashier (Far Right)
    draw_entity(d, 2400, 800, 320, 130, ["Pharmacist / Cashier", "(POS Terminal)"])

    # ENTITY 4: Customer / Patient (Bottom Center)
    draw_entity(d, 1220, 1780, 320, 130, ["Customer / Patient", "(Client)"])

    # -------------------------------------------------------------------------
    # PROCESSES (Rounded Rectangles with top ID section)
    # -------------------------------------------------------------------------
    # 1.0 Auth & RBAC
    draw_process(d, 580, 260, 270, 100, "1.0", ["User Authentication", "& RBAC Engine"])

    # 7.0 Financial BI & Analytics
    draw_process(d, 1900, 260, 280, 100, "7.0", ["Financial BI &", "Analytics Engine"])

    # 3.0 Inventory & FEFO Dispatch
    draw_process(d, 560, 680, 290, 110, "3.0", ["Batch Inventory &", "FEFO Dispatch Logic"])

    # 6.0 Procurement & Reorder PO
    draw_process(d, 560, 960, 290, 110, "6.0", ["Procurement &", "Reorder PO Engine"])

    # 2.0 POS Billing & Reverse GST
    draw_process(d, 1860, 680, 300, 110, "2.0", ["POS Billing &", "Reverse GST Engine"])

    # 5.0 Reverse Logistics & Returns
    draw_process(d, 1860, 960, 300, 110, "5.0", ["Reverse Logistics &", "Returns Desk"])

    # 4.0 Smart CRM & Customer Lookup
    draw_process(d, 1230, 1480, 300, 110, "4.0", ["Smart CRM &", "Patient Directory"])

    # -------------------------------------------------------------------------
    # DATA STORES (Open-ended rectangles with Left ID Slot)
    # -------------------------------------------------------------------------
    # D1 Users & Roles
    draw_data_store(d, 120, 280, 350, 60, "D1", "Users & Roles Table")

    # D2 Medicine Catalog (Center-Left)
    draw_data_store(d, 1060, 640, 380, 65, "D2", "Medicine Catalog Table")

    # D3 Stock Batches (Center-Left Lower)
    draw_data_store(d, 1060, 770, 380, 65, "D3", "Stock Batches Table")

    # D4 Sales Ledger (Center-Right)
    draw_data_store(d, 1060, 960, 380, 65, "D4", "Sale Ledger Table")

    # D6 Return Audits (Center-Right Lower)
    draw_data_store(d, 1060, 1090, 380, 65, "D6", "ReturnSale Audit Table")

    # D5 Customer CRM (Above Customer entity)
    draw_data_store(d, 1060, 1310, 380, 65, "D5", "Customer Records Table")

    # D7 Suppliers Directory (Bottom Left)
    draw_data_store(d, 120, 1150, 350, 60, "D7", "Supplier Directory Table")

    # =========================================================================
    # DATA FLOW ARROWS & LABELS
    # =========================================================================

    # 1. Admin <---> 1.0 Auth
    draw_arrow(d, (1220, 300), (850, 300), label="Admin / Staff Login Credentials", label_pos=(880, 275))
    draw_arrow(d, (580, 310), (470, 310), label="Verify User & Role", label_pos=(480, 285))

    # 2. Admin <---> 7.0 Analytics
    draw_arrow(d, (1540, 310), (1900, 310), label="Request Revenue & Profit Reports", label_pos=(1560, 285))
    draw_arrow(d, (1900, 340), (1540, 340), label="Display KPI BI Charts & Metrics", label_pos=(1570, 345))
    draw_arrow(d, (1440, 980), (1920, 360), label="Read Historical Sales & Margin", label_pos=(1520, 520))

    # 3. Supplier <---> 3.0 Inventory & 6.0 Procurement
    draw_arrow(d, (380, 840), (560, 740), label="Batch Invoices & Consignments", label_pos=(390, 760))
    draw_arrow(d, (560, 1030), (380, 910), label="Reorder Purchase Orders (CSV)", label_pos=(380, 950))

    # 4. Process 3.0 Inventory <---> Data Stores D2 & D3
    draw_arrow(d, (850, 710), (1060, 670), label="Fetch Product Slabs", label_pos=(870, 665))
    draw_arrow(d, (850, 750), (1060, 800), label="Add / Deduct Batches (FEFO)", label_pos=(860, 775))

    # 5. Process 6.0 Procurement <---> Data Stores D2 & D3
    draw_arrow(d, (1060, 820), (850, 990), label="Evaluate Minimum Stock Levels", label_pos=(870, 910))

    # 6. Cashier <---> 2.0 POS Billing
    draw_arrow(d, (2400, 830), (2160, 740), label="Barcode Scan & Product Search", label_pos=(2190, 760))
    draw_arrow(d, (2160, 770), (2400, 860), label="Thermal Receipt & POS Alerts", label_pos=(2190, 820))

    # 7. Process 2.0 POS Billing <---> Data Stores D2, D3, D4
    draw_arrow(d, (1860, 700), (1440, 670), label="Query Active Products", label_pos=(1530, 665))
    draw_arrow(d, (1860, 740), (1440, 790), label="FEFO Batch Allocation", label_pos=(1550, 745))
    draw_arrow(d, (1860, 780), (1440, 980), label="Write Sale Record (Commit)", label_pos=(1560, 870))

    # 8. Customer <---> 4.0 CRM & 2.0 POS
    draw_arrow(d, (1380, 1780), (1380, 1590), label="Phone Number & Prescriptions", label_pos=(1390, 1680))
    draw_arrow(d, (1380, 1480), (1380, 1375), label="Save Patient Profile & Doctor", label_pos=(1390, 1420))
    draw_arrow(d, (1380, 1310), (1960, 790), label="AJAX Auto-Fill Customer Name", label_pos=(1620, 1150))
    draw_arrow(d, (2000, 790), (1540, 1820), label="Printed Tax Invoice & GST Bill", label_pos=(1760, 1450))

    # 9. Customer <---> 5.0 Returns Desk
    draw_arrow(d, (1540, 1850), (2000, 1070), label="Return Item & Receipt Barcode", label_pos=(1760, 1580))
    draw_arrow(d, (1860, 1000), (1440, 1000), label="Verify Bill Barcode in Ledger", label_pos=(1520, 975))
    draw_arrow(d, (1860, 1040), (1440, 1110), label="Log ReturnSale Audit Trail", label_pos=(1520, 1055))
    draw_arrow(d, (1860, 980), (1440, 830), label="Restock Returned Quantity", label_pos=(1530, 895))
    draw_arrow(d, (1960, 1070), (1500, 1870), label="Refund Amount / Exchange Credit", label_pos=(1660, 1690))

    # Footer Notation
    f_ft = get_font(16, italic=True)
    d.text((120, 2030), "Gane & Sarson DFD Level 1: Processes (Rounded Rectangles with ID)  |  Data Stores (Open Rectangles with ID)  |  Entities (Solid Rectangles)", fill="#64748b", font=f_ft)
    d.text((W - 420, 2030), "Pharmacy ERP — Level 1", fill="#64748b", font=f_ft)

    # Save as PNG
    png_out = "dfd_level_1_pharmacy_erp.png"
    img.save(png_out, "PNG", dpi=(300, 300))
    print(f"SUCCESS: Saved high-res PNG to {png_out}")

    # Save as PDF
    pdf_out = "dfd_level_1_pharmacy_erp.pdf"
    img.save(pdf_out, "PDF", resolution=150.0)
    print(f"SUCCESS: Saved single-page PDF to {pdf_out}")

if __name__ == '__main__':
    generate_dfd1()
