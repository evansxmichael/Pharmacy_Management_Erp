import os
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Brand Colors
    C_NAVY_BG = RGBColor(12, 31, 48)
    C_NAVY_ACCENT = RGBColor(20, 48, 74)
    C_TEAL = RGBColor(0, 139, 139)
    C_TEAL_LIGHT = RGBColor(224, 242, 241)
    C_CYAN = RGBColor(14, 165, 233)
    C_LIGHT_BG = RGBColor(244, 247, 246)
    C_WHITE = RGBColor(255, 255, 255)
    C_DARK_TXT = RGBColor(30, 41, 59)
    C_MUTED_TXT = RGBColor(100, 116, 139)
    C_BORDER = RGBColor(226, 232, 240)
    C_GREEN = RGBColor(16, 185, 129)
    C_AMBER = RGBColor(245, 158, 11)
    C_RED = RGBColor(239, 68, 68)

    def add_bg(slide, is_dark=False):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = C_NAVY_BG if is_dark else C_LIGHT_BG
        bg.line.fill.background()
        return bg

    def add_header(slide, tag_text, title_text, slide_num=""):
        # Category Tag
        tag_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.45), Inches(8), Inches(0.35))
        tf_tag = tag_box.text_frame
        tf_tag.word_wrap = True
        p_tag = tf_tag.paragraphs[0]
        p_tag.text = tag_text.upper()
        p_tag.font.size = Pt(10)
        p_tag.font.bold = True
        p_tag.font.color.rgb = C_TEAL
        
        # Main Slide Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(10.5), Inches(0.65))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = C_DARK_TXT

        if slide_num:
            num_box = slide.shapes.add_textbox(Inches(12.0), Inches(0.55), Inches(0.8), Inches(0.4))
            tf_num = num_box.text_frame
            p_num = tf_num.paragraphs[0]
            p_num.text = str(slide_num).zfill(2)
            p_num.alignment = PP_ALIGN.RIGHT
            p_num.font.size = Pt(13)
            p_num.font.bold = True
            p_num.font.color.rgb = C_MUTED_TXT

    # =========================================================================
    # SLIDE 1: TITLE SLIDE (Cover)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    add_bg(s1, is_dark=True)

    # Decorative accent card
    card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.7), Inches(1.8), Inches(0.65))
    card.fill.solid()
    card.fill.fore_color.rgb = C_TEAL
    card.line.fill.background()
    tf_c = card.text_frame
    p_c = tf_c.paragraphs[0]
    p_c.text = "MAJOR PROJECT"
    p_c.font.bold = True
    p_c.font.size = Pt(11)
    p_c.font.color.rgb = C_WHITE
    p_c.alignment = PP_ALIGN.CENTER

    # Main Project Title
    t_box = s1.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(11.5), Inches(1.8))
    tf_t = t_box.text_frame
    p1 = tf_t.paragraphs[0]
    p1.text = "PHARMACY MANAGEMENT SYSTEM"
    p1.font.bold = True
    p1.font.size = Pt(36)
    p1.font.color.rgb = C_WHITE

    p2 = tf_t.add_paragraph()
    p2.text = "A Centralized Web-Based ERP Platform for Retail Pharmacy Operations"
    p2.font.size = Pt(17)
    p2.font.color.rgb = C_CYAN
    p2.space_before = Pt(8)

    # Divider Line
    line = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(3.2), Inches(11.733), Inches(0.04))
    line.fill.solid()
    line.fill.fore_color.rgb = RGBColor(30, 65, 95)
    line.line.fill.background()

    # Presenters Card
    pres_box = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(3.6), Inches(5.6), Inches(2.2))
    pres_box.fill.solid()
    pres_box.fill.fore_color.rgb = C_NAVY_ACCENT
    pres_box.line.color.rgb = RGBColor(40, 80, 115)
    tf_pres = pres_box.text_frame
    tf_pres.word_wrap = True
    
    p = tf_pres.paragraphs[0]
    p.text = "PRESENTED BY:"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_TEAL_LIGHT
    
    p = tf_pres.add_paragraph()
    p.text = "• MD ZEESHAN  (Roll No: 23BTCS026HY)"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_WHITE
    p.space_before = Pt(6)

    p = tf_pres.add_paragraph()
    p.text = "• YUSUF HANZALA  (Roll No: 23BTCS005HY)"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_WHITE
    p.space_before = Pt(4)

    p = tf_pres.add_paragraph()
    p.text = "7th Semester, B.Tech Computer Science | Academic Session 2026-27"
    p.font.size = Pt(11)
    p.font.color.rgb = C_CYAN
    p.space_before = Pt(8)

    # Supervisor & Department Card
    sup_box = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(3.6), Inches(5.7), Inches(2.2))
    sup_box.fill.solid()
    sup_box.fill.fore_color.rgb = C_NAVY_ACCENT
    sup_box.line.color.rgb = RGBColor(40, 80, 115)
    tf_sup = sup_box.text_frame
    tf_sup.word_wrap = True

    p = tf_sup.paragraphs[0]
    p.text = "UNDER THE SUPERVISION OF:"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_TEAL_LIGHT

    p = tf_sup.add_paragraph()
    p.text = "Mrs. Nusrath Fathima"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_WHITE
    p.space_before = Pt(6)

    p = tf_sup.add_paragraph()
    p.text = "Assistant Professor, Dept. of Computer Science & Information Technology"
    p.font.size = Pt(12)
    p.font.color.rgb = RGBColor(200, 220, 240)
    p.space_before = Pt(2)

    p = tf_sup.add_paragraph()
    p.text = "Maulana Azad National Urdu University (MANUU), Hyderabad"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_CYAN
    p.space_before = Pt(4)

    # Footer note
    ft = s1.shapes.add_textbox(Inches(0.8), Inches(6.4), Inches(11.7), Inches(0.5))
    tf_ft = ft.text_frame
    p_ft = tf_ft.paragraphs[0]
    p_ft.text = "Centralized Web Architecture  |  FEFO Automated Inventory  |  Dynamic GST POS  |  Smart Patient CRM"
    p_ft.font.size = Pt(10)
    p_ft.font.color.rgb = RGBColor(140, 170, 200)
    p_ft.alignment = PP_ALIGN.CENTER

    # =========================================================================
    # SLIDE 2: INTRODUCTION (The Operational Shift)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_bg(s2)
    add_header(s2, "Introduction", "From Fragmented Operations to One Centralized Platform", "02")

    # Left bullet list container
    l_box = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(7.2), Inches(5.2))
    l_box.fill.solid()
    l_box.fill.fore_color.rgb = C_WHITE
    l_box.line.color.rgb = C_BORDER
    tf_l = l_box.text_frame
    tf_l.word_wrap = True

    bullets = [
        ("Interconnected Retail Nature: ", "Pharmacy retail operations naturally involve heavily interdependent processes — POS customer billing, batch inventory, drug procurement, reverse logistics, and tax analytics."),
        ("The Fragmented Reality: ", "Traditional retail pharmacies often rely on manual paper registers, standalone billing machines, or isolated desktop spreadsheets that fail to synchronize in real time."),
        ("Operational Bottlenecks: ", "This disconnection makes drug expiry tracking, low-stock reordering, reverse logistics, and overall profit auditing error-prone, laborious, and risky."),
        ("The Centralized ERP Solution: ", "Pharmacy Management ERP resolves this with a full-stack, cloud-hosted web system that consolidates all retail workflows into an integrated, real-time command platform."),
        ("Real-World Operational Alignment: ", "Purpose-built around real daily pharmacy workflows — including rapid barcode scanning, FEFO batch allocation, thermal receipts, and smart patient directories.")
    ]
    for i, (head, body) in enumerate(bullets):
        p = tf_l.paragraphs[0] if i == 0 else tf_l.add_paragraph()
        p.space_before = Pt(10)
        p.font.size = Pt(12)
        run_h = p.add_run()
        run_h.text = "•  " + head
        run_h.font.bold = True
        run_h.font.color.rgb = C_DARK_TXT
        run_b = p.add_run()
        run_b.text = body
        run_b.font.color.rgb = C_MUTED_TXT

    # Right comparison graphic
    r_box = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.3), Inches(1.6), Inches(4.2), Inches(5.2))
    r_box.fill.solid()
    r_box.fill.fore_color.rgb = RGBColor(241, 248, 248)
    r_box.line.color.rgb = C_TEAL
    tf_r = r_box.text_frame
    tf_r.word_wrap = True
    
    p = tf_r.paragraphs[0]
    p.text = "THE OPERATIONAL SHIFT"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_TEAL
    p.alignment = PP_ALIGN.CENTER

    sub_items = ["Manual Billing & Receipts", "Disjointed Inventory Ledgers", "Unmonitored Medicine Expiry", "Disconnected Patient Records"]
    top_pos = 2.4
    for item in sub_items:
        card_item = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.6), Inches(top_pos), Inches(3.6), Inches(0.55))
        card_item.fill.solid()
        card_item.fill.fore_color.rgb = C_WHITE
        card_item.line.color.rgb = C_BORDER
        tf_ci = card_item.text_frame
        p_ci = tf_ci.paragraphs[0]
        p_ci.text = item
        p_ci.font.size = Pt(10.5)
        p_ci.font.color.rgb = C_DARK_TXT
        p_ci.alignment = PP_ALIGN.CENTER
        top_pos += 0.65

    # Down Arrow
    arrow = s2.shapes.add_shape(MSO_SHAPE.DOWN_ARROW, Inches(10.15), Inches(5.1), Inches(0.5), Inches(0.45))
    arrow.fill.solid()
    arrow.fill.fore_color.rgb = C_TEAL
    arrow.line.fill.background()

    # Solution Banner
    sol = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.6), Inches(5.7), Inches(3.6), Inches(0.85))
    sol.fill.solid()
    sol.fill.fore_color.rgb = C_TEAL
    sol.line.fill.background()
    tf_sol = sol.text_frame
    p_s1 = tf_sol.paragraphs[0]
    p_s1.text = "PHARMACY MANAGEMENT ERP"
    p_s1.font.bold = True
    p_s1.font.size = Pt(11.5)
    p_s1.font.color.rgb = C_WHITE
    p_s1.alignment = PP_ALIGN.CENTER
    p_s2 = tf_sol.add_paragraph()
    p_s2.text = "One Unified, Cloud-Hosted Command Center"
    p_s2.font.size = Pt(9.5)
    p_s2.font.color.rgb = C_TEAL_LIGHT
    p_s2.alignment = PP_ALIGN.CENTER

    # =========================================================================
    # SLIDE 3: PROBLEM STATEMENT
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_bg(s3)
    add_header(s3, "Problem Statement", "Critical Bottlenecks in Traditional Pharmacy Retail", "03")

    problems = [
        ("01", "Inventory Expiry & Dead Stock", "Medicines sit on shelves unnoticed until expiry. Lack of batch-level tracking causes heavy recurring financial losses and safety hazards.", C_RED),
        ("02", "Billing Inefficiency & Errors", "Manual product lookups and manual pricing calculations slow down checkout queues, leading to pricing errors and customer dissatisfaction.", C_AMBER),
        ("03", "Coarse-Grained Stock Monitoring", "Tracking only gross medicine quantities without individual batch numbers, supplier tags, and manufacturing records prevents audit traceability.", C_TEAL),
        ("04", "Lack of Patient Traceability", "Manual customer logging fails to retain prescription history, visiting doctors, or previous purchase records for regular chronic patients.", C_CYAN),
        ("05", "Blind Financial Visibility", "Business owners lack real-time visibility into daily revenue, net profit margins, GST liability, and fast-moving vs dead inventory.", C_DARK_TXT),
        ("06", "Absence of Role-Based Security", "Cashiers, store managers, and owners share identical access permissions, exposing sensitive wholesale costs and financial metrics.", C_NAVY_ACCENT),
    ]

    coords = [
        (0.8, 1.6), (4.85, 1.6), (8.9, 1.6),
        (0.8, 4.3), (4.85, 4.3), (8.9, 4.3)
    ]
    for (idx, title, desc, col), (x, y) in zip(problems, coords):
        box = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(3.6), Inches(2.35))
        box.fill.solid()
        box.fill.fore_color.rgb = C_WHITE
        box.line.color.rgb = C_BORDER
        
        # Pill badge
        badge = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x + 0.2), Inches(y + 0.2), Inches(0.6), Inches(0.35))
        badge.fill.solid()
        badge.fill.fore_color.rgb = col
        badge.line.fill.background()
        tf_b = badge.text_frame
        p_b = tf_b.paragraphs[0]
        p_b.text = idx
        p_b.font.bold = True
        p_b.font.size = Pt(10)
        p_b.font.color.rgb = C_WHITE
        p_b.alignment = PP_ALIGN.CENTER

        tb = s3.shapes.add_textbox(Inches(x + 0.2), Inches(y + 0.65), Inches(3.2), Inches(1.5))
        tf = tb.text_frame
        tf.word_wrap = True
        
        pt = tf.paragraphs[0]
        pt.text = title
        pt.font.bold = True
        pt.font.size = Pt(13)
        pt.font.color.rgb = C_DARK_TXT
        
        pd = tf.add_paragraph()
        pd.text = desc
        pd.font.size = Pt(10.5)
        pd.font.color.rgb = C_MUTED_TXT
        pd.space_before = Pt(4)

    # =========================================================================
    # SLIDE 4: OBJECTIVES OF PHARMACY ERP
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_bg(s4)
    add_header(s4, "Project Objectives", "Concrete Engineering Goals of Pharmacy Management ERP", "04")

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
        y = 1.6 + (row_idx * 1.3)

        box = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(5.7), Inches(1.15))
        box.fill.solid()
        box.fill.fore_color.rgb = C_WHITE
        box.line.color.rgb = C_BORDER

        # Check Icon Badge
        badge = s4.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x + 0.2), Inches(y + 0.25), Inches(0.4), Inches(0.4))
        badge.fill.solid()
        badge.fill.fore_color.rgb = C_GREEN
        badge.line.fill.background()
        tf_b = badge.text_frame
        p_b = tf_b.paragraphs[0]
        p_b.text = "✓"
        p_b.font.bold = True
        p_b.font.size = Pt(11)
        p_b.font.color.rgb = C_WHITE
        p_b.alignment = PP_ALIGN.CENTER

        tb = s4.shapes.add_textbox(Inches(x + 0.75), Inches(y + 0.1), Inches(4.75), Inches(0.95))
        tf = tb.text_frame
        tf.word_wrap = True

        pt = tf.paragraphs[0]
        pt.text = title
        pt.font.bold = True
        pt.font.size = Pt(12)
        pt.font.color.rgb = C_DARK_TXT

        pd = tf.add_paragraph()
        pd.text = desc
        pd.font.size = Pt(10)
        pd.font.color.rgb = C_MUTED_TXT
        pd.space_before = Pt(2)

    # =========================================================================
    # SLIDE 5: DFD LEVEL 0 (CONTEXT DIAGRAM) -- CRITICAL REQUIREMENT
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_bg(s5)
    add_header(s5, "System Modeling", "Data Flow Diagram — Level 0 (Context Diagram)", "05")

    # Central System Node (0.0)
    sys_circle = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.7), Inches(2.7), Inches(3.9), Inches(2.2))
    sys_circle.fill.solid()
    sys_circle.fill.fore_color.rgb = C_NAVY_BG
    sys_circle.line.color.rgb = C_TEAL
    sys_circle.line.width = Pt(2.5)
    tf_sc = sys_circle.text_frame
    tf_sc.word_wrap = True
    
    p = tf_sc.paragraphs[0]
    p.text = "0.0"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = C_CYAN
    p.alignment = PP_ALIGN.CENTER

    p = tf_sc.add_paragraph()
    p.text = "PHARMACY MANAGEMENT\nERP SYSTEM"
    p.font.bold = True
    p.font.size = Pt(15)
    p.font.color.rgb = C_WHITE
    p.alignment = PP_ALIGN.CENTER
    p.space_before = Pt(4)

    p = tf_sc.add_paragraph()
    p.text = "Centralized Web & Database Engine"
    p.font.size = Pt(9.5)
    p.font.color.rgb = C_TEAL_LIGHT
    p.alignment = PP_ALIGN.CENTER
    p.space_before = Pt(4)

    # External Entity 1: Cashier / Pharmacist (Top-Left)
    e1 = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(3.1), Inches(1.5))
    e1.fill.solid()
    e1.fill.fore_color.rgb = C_WHITE
    e1.line.color.rgb = C_TEAL
    e1.line.width = Pt(1.5)
    tf_e1 = e1.text_frame
    tf_e1.word_wrap = True
    p = tf_e1.paragraphs[0]
    p.text = "COUNTER CASHIER / PHARMACIST"
    p.font.bold = True
    p.font.size = Pt(10)
    p.font.color.rgb = C_TEAL
    p = tf_e1.add_paragraph()
    p.text = "• Barcode / Product Queries\n• Customer Contact & Cart Input\n• Return Verification Request"
    p.font.size = Pt(8.5)
    p.font.color.rgb = C_MUTED_TXT

    # Flow arrows E1 <-> System
    arrow_e1_in = s5.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(4.0), Inches(2.0), Inches(0.6), Inches(0.2))
    arrow_e1_in.fill.solid()
    arrow_e1_in.fill.fore_color.rgb = C_TEAL
    arrow_e1_in.line.fill.background()

    arrow_e1_out = s5.shapes.add_shape(MSO_SHAPE.LEFT_ARROW, Inches(4.0), Inches(2.4), Inches(0.6), Inches(0.2))
    arrow_e1_out.fill.solid()
    arrow_e1_out.fill.fore_color.rgb = C_CYAN
    arrow_e1_out.line.fill.background()

    # External Entity 2: Store Manager / Admin (Top-Right)
    e2 = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(9.4), Inches(1.6), Inches(3.1), Inches(1.5))
    e2.fill.solid()
    e2.fill.fore_color.rgb = C_WHITE
    e2.line.color.rgb = C_NAVY_BG
    e2.line.width = Pt(1.5)
    tf_e2 = e2.text_frame
    tf_e2.word_wrap = True
    p = tf_e2.paragraphs[0]
    p.text = "STORE MANAGER / ADMIN"
    p.font.bold = True
    p.font.size = Pt(10)
    p.font.color.rgb = C_NAVY_BG
    p = tf_e2.add_paragraph()
    p.text = "• New Batch & Supplier Entry\n• User Role Provisioning\n• BI Analytics & Audit Inquiries"
    p.font.size = Pt(8.5)
    p.font.color.rgb = C_MUTED_TXT

    # Flow arrows E2 <-> System
    arrow_e2_in = s5.shapes.add_shape(MSO_SHAPE.LEFT_ARROW, Inches(8.7), Inches(2.0), Inches(0.6), Inches(0.2))
    arrow_e2_in.fill.solid()
    arrow_e2_in.fill.fore_color.rgb = C_NAVY_BG
    arrow_e2_in.line.fill.background()

    arrow_e2_out = s5.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(8.7), Inches(2.4), Inches(0.6), Inches(0.2))
    arrow_e2_out.fill.solid()
    arrow_e2_out.fill.fore_color.rgb = C_AMBER
    arrow_e2_out.line.fill.background()

    # External Entity 3: Customer / Patient (Bottom-Left)
    e3 = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.6), Inches(3.1), Inches(1.5))
    e3.fill.solid()
    e3.fill.fore_color.rgb = C_WHITE
    e3.line.color.rgb = C_GREEN
    e3.line.width = Pt(1.5)
    tf_e3 = e3.text_frame
    tf_e3.word_wrap = True
    p = tf_e3.paragraphs[0]
    p.text = "CUSTOMER / PATIENT"
    p.font.bold = True
    p.font.size = Pt(10)
    p.font.color.rgb = C_GREEN
    p = tf_e3.add_paragraph()
    p.text = "• Prescription & Phone Number\n• Return Items & Scannable Bill\n• Cash / UPI Payment"
    p.font.size = Pt(8.5)
    p.font.color.rgb = C_MUTED_TXT

    # Flow arrows E3 <-> System
    arrow_e3_in = s5.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(4.0), Inches(5.0), Inches(0.6), Inches(0.2))
    arrow_e3_in.fill.solid()
    arrow_e3_in.fill.fore_color.rgb = C_GREEN
    arrow_e3_in.line.fill.background()

    arrow_e3_out = s5.shapes.add_shape(MSO_SHAPE.LEFT_ARROW, Inches(4.0), Inches(5.4), Inches(0.6), Inches(0.2))
    arrow_e3_out.fill.solid()
    arrow_e3_out.fill.fore_color.rgb = C_CYAN
    arrow_e3_out.line.fill.background()

    # External Entity 4: Medicine Supplier (Bottom-Right)
    e4 = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(9.4), Inches(4.6), Inches(3.1), Inches(1.5))
    e4.fill.solid()
    e4.fill.fore_color.rgb = C_WHITE
    e4.line.color.rgb = C_AMBER
    e4.line.width = Pt(1.5)
    tf_e4 = e4.text_frame
    tf_e4.word_wrap = True
    p = tf_e4.paragraphs[0]
    p.text = "SUPPLIER / WHOLESALER"
    p.font.bold = True
    p.font.size = Pt(10)
    p.font.color.rgb = C_AMBER
    p = tf_e4.add_paragraph()
    p.text = "• Medicine Batches & Invoices\n• Restocking Consignments\n• Purchase Orders Received"
    p.font.size = Pt(8.5)
    p.font.color.rgb = C_MUTED_TXT

    # Flow arrows E4 <-> System
    arrow_e4_in = s5.shapes.add_shape(MSO_SHAPE.LEFT_ARROW, Inches(8.7), Inches(5.0), Inches(0.6), Inches(0.2))
    arrow_e4_in.fill.solid()
    arrow_e4_in.fill.fore_color.rgb = C_AMBER
    arrow_e4_in.line.fill.background()

    arrow_e4_out = s5.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(8.7), Inches(5.4), Inches(0.6), Inches(0.2))
    arrow_e4_out.fill.solid()
    arrow_e4_out.fill.fore_color.rgb = C_TEAL
    arrow_e4_out.line.fill.background()

    # Central Output Label Note
    lbl = s5.shapes.add_textbox(Inches(3.5), Inches(6.4), Inches(6.3), Inches(0.6))
    tf_lbl = lbl.text_frame
    p_lbl = tf_lbl.paragraphs[0]
    p_lbl.text = "System Output: Scannable Thermal Receipt (JsBarcode), CSV Reorder PO, Real-Time BI Charts, Return Refunds"
    p_lbl.font.size = Pt(9.5)
    p_lbl.font.bold = True
    p_lbl.font.color.rgb = C_MUTED_TXT
    p_lbl.alignment = PP_ALIGN.CENTER

    # =========================================================================
    # SLIDE 6: DFD LEVEL 1 (FUNCTIONAL DECOMPOSITION) -- CRITICAL REQUIREMENT
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_bg(s6)
    add_header(s6, "System Modeling", "Data Flow Diagram — Level 1 (Decomposition Diagram)", "06")

    # Column 1: Core Operational Processes
    processes = [
        ("1.0", "Authentication & RBAC Control", "Validates login against User/Group models; routes to Admin, Manager, or Cashier UI.", C_NAVY_BG),
        ("2.0", "POS & Reverse GST Billing Engine", "Accepts barcode/product queries; calculates GST dynamically; creates Sale transaction.", C_TEAL),
        ("3.0", "FEFO Batch Inventory Dispatch", "Sorts stock by expiry_date; deducts sold quantities; triggers Signal replenishment on deletion.", C_GREEN),
        ("4.0", "Reverse Logistics (Returns Desk)", "Scans receipt barcode; validates bill items; restocks physical units; logs ReturnSale audit.", C_AMBER),
        ("5.0", "Smart CRM & Customer Directory", "Executes AJAX telephone lookup; links customer to doctor, prescriptions, and purchase total.", C_CYAN),
        ("6.0", "Procurement & Reorder Engine", "Evaluates batch stocks against minimum_stock_level; exports CSV reorder purchase orders.", C_DARK_TXT),
        ("7.0", "Financial BI & Analytics Engine", "Aggregates daily sales, profit margins, GST totals, and payment modes (Cash/UPI).", C_RED),
    ]

    for i, (p_num, p_title, p_desc, p_col) in enumerate(processes):
        y = 1.5 + (i * 0.77)
        card = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(y), Inches(6.8), Inches(0.70))
        card.fill.solid()
        card.fill.fore_color.rgb = C_WHITE
        card.line.color.rgb = C_BORDER

        # Process ID Badge
        b = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.9), Inches(y + 0.12), Inches(0.65), Inches(0.45))
        b.fill.solid()
        b.fill.fore_color.rgb = p_col
        b.line.fill.background()
        tf_b = b.text_frame
        p_b = tf_b.paragraphs[0]
        p_b.text = p_num
        p_b.font.bold = True
        p_b.font.size = Pt(11)
        p_b.font.color.rgb = C_WHITE
        p_b.alignment = PP_ALIGN.CENTER

        tb = s6.shapes.add_textbox(Inches(1.65), Inches(y + 0.05), Inches(5.8), Inches(0.6))
        tf = tb.text_frame
        tf.word_wrap = True
        pt = tf.paragraphs[0]
        pt.text = p_title
        pt.font.bold = True
        pt.font.size = Pt(11)
        pt.font.color.rgb = C_DARK_TXT

        pd = tf.add_paragraph()
        pd.text = p_desc
        pd.font.size = Pt(8.5)
        pd.font.color.rgb = C_MUTED_TXT

    # Column 2: Data Stores (D1 to D6)
    data_stores = [
        ("D1", "Medicine Catalog Table", "Attributes: barcode, name, category, manufacturer, pack_size, gst_percentage, min_stock."),
        ("D2", "Stock Batches Table", "Attributes: medicine_id, batch_no, expiry_date, quantity, purchase_price, mrp, supplier_id."),
        ("D3", "Sale Ledger Table", "Attributes: bill_no, stock_id, quantity, total_price, customer_id, payment_method, date."),
        ("D4", "ReturnSale Audit Table", "Attributes: sale_id, stock_id, quantity_returned, refund_amount, reason, restocked, returned_at."),
        ("D5", "Customer CRM Table", "Attributes: name, phone (unique), last_doctor, cumulative purchase history."),
        ("D6", "Supplier Directory Table", "Attributes: name, contact_person, phone, email, address.")
    ]

    # Data Store Header Banner
    ds_ban = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.0), Inches(1.5), Inches(4.5), Inches(0.4))
    ds_ban.fill.solid()
    ds_ban.fill.fore_color.rgb = C_NAVY_BG
    ds_ban.line.fill.background()
    tf_ds = ds_ban.text_frame
    p_ds = tf_ds.paragraphs[0]
    p_ds.text = "DATABASE DATA STORES (RELATIONAL REPOSITORY)"
    p_ds.font.bold = True
    p_ds.font.size = Pt(10)
    p_ds.font.color.rgb = C_CYAN
    p_ds.alignment = PP_ALIGN.CENTER

    for j, (ds_id, ds_name, ds_desc) in enumerate(data_stores):
        y = 2.05 + (j * 0.82)
        ds_box = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.0), Inches(y), Inches(4.5), Inches(0.74))
        ds_box.fill.solid()
        ds_box.fill.fore_color.rgb = C_WHITE
        ds_box.line.color.rgb = C_TEAL
        ds_box.line.width = Pt(1.5)

        b = s6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(8.1), Inches(y + 0.12), Inches(0.55), Inches(0.5))
        b.fill.solid()
        b.fill.fore_color.rgb = C_TEAL
        b.line.fill.background()
        tf_b = b.text_frame
        p_b = tf_b.paragraphs[0]
        p_b.text = ds_id
        p_b.font.bold = True
        p_b.font.size = Pt(11)
        p_b.font.color.rgb = C_WHITE
        p_b.alignment = PP_ALIGN.CENTER

        tb = s6.shapes.add_textbox(Inches(8.75), Inches(y + 0.05), Inches(3.65), Inches(0.65))
        tf = tb.text_frame
        tf.word_wrap = True
        pt = tf.paragraphs[0]
        pt.text = ds_name
        pt.font.bold = True
        pt.font.size = Pt(11)
        pt.font.color.rgb = C_DARK_TXT

        pd = tf.add_paragraph()
        pd.text = ds_desc
        pd.font.size = Pt(8.5)
        pd.font.color.rgb = C_MUTED_TXT

    # =========================================================================
    # SLIDE 7: CORE MODULES & FUNCTIONALITY
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_bg(s7)
    add_header(s7, "Proposed System", "Core Operational Modules of Pharmacy Management ERP", "07")

    modules = [
        ("POS & Dynamic Billing", "• Barcode scanner input\n• Select2 live medicine search\n• Real-time cart calculation\n• Scannable thermal receipt printing", C_TEAL),
        ("FEFO Batch Inventory", "• Batch-level tracking\n• Automatic earliest-expiry allocation\n• Visual expiry alert badges\n• Automated stock deduction", C_GREEN),
        ("Patient CRM Directory", "• Fast AJAX phone lookup\n• Prescribing doctor tracking\n• Lifetime purchases & spend\n• Returning patient loyalty", C_CYAN),
        ("Financial Analytics & BI", "• Dynamic GST tax breakdown\n• Revenue & profit margins\n• Best-selling medicine ranking\n• CSV financial export", C_AMBER),
        ("Reverse Logistics Desk", "• Receipt barcode returns\n• Return reason logging\n• Automatic shelf restocking\n• Customer refund computation", C_RED),
        ("Security & RBAC", "• Admin, Manager, Cashier roles\n• View-level access restrictions\n• Sensitive cost masking\n• Auto session timeout on close", C_NAVY_BG),
    ]

    coords_mod = [
        (0.8, 1.6), (4.85, 1.6), (8.9, 1.6),
        (0.8, 4.3), (4.85, 4.3), (8.9, 4.3)
    ]
    for (m_title, m_desc, m_col), (x, y) in zip(modules, coords_mod):
        box = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(3.6), Inches(2.4))
        box.fill.solid()
        box.fill.fore_color.rgb = C_WHITE
        box.line.color.rgb = C_BORDER

        top_bar = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(3.6), Inches(0.45))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = m_col
        top_bar.line.fill.background()
        tf_tb = top_bar.text_frame
        p_tb = tf_tb.paragraphs[0]
        p_tb.text = m_title.upper()
        p_tb.font.bold = True
        p_tb.font.size = Pt(10.5)
        p_tb.font.color.rgb = C_WHITE
        p_tb.alignment = PP_ALIGN.CENTER

        tb = s7.shapes.add_textbox(Inches(x + 0.2), Inches(y + 0.55), Inches(3.2), Inches(1.75))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = m_desc
        p.font.size = Pt(10.5)
        p.font.color.rgb = C_DARK_TXT

    # =========================================================================
    # SLIDE 8: THREE-TIER SYSTEM ARCHITECTURE
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_bg(s8)
    add_header(s8, "System Architecture", "Three-Tier Modular Web Architecture", "08")

    layers = [
        ("Presentation Layer (Client)", "HTML5  •  CSS3  •  Bootstrap 5.3  •  Vanilla JavaScript (ES6)  •  AJAX  •  Select2  •  JsBarcode  •  FontAwesome", C_TEAL),
        ("Application Layer (Business Logic)", "Python 3.14  •  Django 6.0.4  •  Django Views & Middleware  •  Django ORM  •  FEFO Engine  •  Signals  •  RBAC Engine", C_NAVY_BG),
        ("Data Layer (Persistent Storage)", "SQLite Database (Production Deployment)  •  Relational Models (Medicine, Stock, Sale, ReturnSale, Customer, Supplier)", C_DARK_TXT),
        ("Cloud Infrastructure & Security", "PythonAnywhere Cloud PaaS  •  Django WSGI  •  Session Timeout Security  •  python-dotenv Secret Vault", C_CYAN)
    ]

    for i, (l_title, l_techs, l_col) in enumerate(layers):
        y = 1.6 + (i * 1.3)
        box = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(y), Inches(11.733), Inches(1.05))
        box.fill.solid()
        box.fill.fore_color.rgb = C_WHITE
        box.line.color.rgb = C_BORDER

        # Left Accent Strip
        strip = s8.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(y), Inches(0.18), Inches(1.05))
        strip.fill.solid()
        strip.fill.fore_color.rgb = l_col
        strip.line.fill.background()

        tb = s8.shapes.add_textbox(Inches(1.2), Inches(y + 0.08), Inches(11.0), Inches(0.9))
        tf = tb.text_frame
        tf.word_wrap = True

        pt = tf.paragraphs[0]
        pt.text = l_title
        pt.font.bold = True
        pt.font.size = Pt(13)
        pt.font.color.rgb = l_col

        pd = tf.add_paragraph()
        pd.text = l_techs
        pd.font.size = Pt(10.5)
        pd.font.color.rgb = C_DARK_TXT
        pd.space_before = Pt(3)

    # =========================================================================
    # SLIDE 9: TECHNOLOGY STACK & TOOLING
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_bg(s9)
    add_header(s9, "Tools & Technologies", "Full Implementation Technology Stack", "09")

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
        y = 1.6 + (i * 0.85)
        card = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(y), Inches(5.6), Inches(0.75))
        card.fill.solid()
        card.fill.fore_color.rgb = C_WHITE
        card.line.color.rgb = C_BORDER
        tf = card.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = k
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = C_TEAL
        p2 = tf.add_paragraph()
        p2.text = v
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = C_DARK_TXT

    for i, (k, v) in enumerate(tech_right):
        y = 1.6 + (i * 0.85)
        card = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(y), Inches(5.7), Inches(0.75))
        card.fill.solid()
        card.fill.fore_color.rgb = C_WHITE
        card.line.color.rgb = C_BORDER
        tf = card.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = k
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = C_CYAN
        p2 = tf.add_paragraph()
        p2.text = v
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = C_DARK_TXT

    # =========================================================================
    # SLIDE 10: KEY TECHNICAL DEPTH & INNOVATIONS
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_bg(s10)
    add_header(s10, "Technical Depth", "Core Algorithms & Implementation Highlights", "10")

    highlights = [
        ("Automated FEFO Dispatch Algorithm", "Instead of arbitrary manual batch picking, queries evaluate all active batches ordered by expiry_date ASC. If quantity exceeds first batch, it automatically rolls to next batch without manual intervention.", C_TEAL),
        ("Dynamic Reverse GST Calculation", "Since medicine MRPs are legally tax-inclusive in India, the billing engine executes reverse calculation: Base = Total / (1 + GST/100), accurately reporting CGST and SGST on receipts.", C_GREEN),
        ("Event-Driven Django Signals", "Implemented post_delete receiver signal on Sale transactions. If a transaction is canceled or refunded, stock is automatically credited back to its exact batch without manual adjustment.", C_CYAN),
        ("Asynchronous Patient Auto-Fill", "Typing customer phone trigger debounced AJAX queries to /api/get_customer/. It returns patient name and visiting doctor instantaneously, accelerating checkout speed.", C_AMBER),
        ("Multi-Tier Role-Based Security", "Custom middleware and template permission checks verify request.user.groups. Store cashiers are blocked from seeing profit metrics and cannot create new batches.", C_RED),
        ("Enterprise POS Session Hardening", "Configured SESSION_EXPIRE_AT_BROWSER_CLOSE = True and SESSION_COOKIE_AGE = 1800, guaranteeing counter terminals auto-logout upon browser closure or inactivity.", C_NAVY_BG)
    ]

    for (title, desc, col), (x, y) in zip(highlights, coords_mod):
        box = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(3.6), Inches(2.4))
        box.fill.solid()
        box.fill.fore_color.rgb = C_WHITE
        box.line.color.rgb = C_BORDER

        top_strip = s10.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(3.6), Inches(0.08))
        top_strip.fill.solid()
        top_strip.fill.fore_color.rgb = col
        top_strip.line.fill.background()

        tb = s10.shapes.add_textbox(Inches(x + 0.2), Inches(y + 0.2), Inches(3.2), Inches(2.0))
        tf = tb.text_frame
        tf.word_wrap = True

        pt = tf.paragraphs[0]
        pt.text = title
        pt.font.bold = True
        pt.font.size = Pt(12)
        pt.font.color.rgb = col

        pd = tf.add_paragraph()
        pd.text = desc
        pd.font.size = Pt(9.5)
        pd.font.color.rgb = C_DARK_TXT
        pd.space_before = Pt(4)

    # =========================================================================
    # SLIDE 11: DATABASE SCHEMA & ENTITY RELATIONSHIPS
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_bg(s11)
    add_header(s11, "Database Design", "Relational Entity Schema & Data Relationships", "11")

    models_data = [
        ("Medicine (Product Master)", "• barcode (Unique)\n• name, category\n• manufacturer\n• gst_percentage\n• minimum_stock_level\n• pack_size\n• @property total_stock"),
        ("Stock (Batch Inventory)", "• batch_no\n• expiry_date (Date)\n• quantity (Int)\n• purchase_price (Float)\n• mrp (Float)\n• FK -> Medicine (CASCADE)\n• FK -> Supplier (SET_NULL)"),
        ("Sale (Transaction Ledger)", "• bill_no (Indexed)\n• quantity (Int)\n• total_price (Float)\n• payment_method (Cash/UPI)\n• date (DateTimeField)\n• FK -> Stock (CASCADE)\n• FK -> Customer (SET_NULL)"),
        ("ReturnSale (Audit Trail)", "• quantity_returned (Int)\n• refund_amount (Float)\n• reason (WRONG/DEFECT/EXCESS)\n• restocked (Boolean)\n• returned_at (DateTime)\n• FK -> Sale (CASCADE)\n• FK -> Stock (CASCADE)"),
        ("Customer (Smart CRM)", "• name (Char)\n• phone (Unique 15)\n• last_doctor (Char)\n• related: purchase_history\n• computed: total_spent"),
        ("Supplier (Wholesaler)", "• name (Char 200)\n• contact_person\n• phone, email\n• address (Text)\n• related: stock_set")
    ]

    for (m_name, m_fields), (x, y) in zip(models_data, coords_mod):
        box = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(3.6), Inches(2.4))
        box.fill.solid()
        box.fill.fore_color.rgb = C_WHITE
        box.line.color.rgb = C_BORDER

        hdr = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(3.6), Inches(0.42))
        hdr.fill.solid()
        hdr.fill.fore_color.rgb = C_NAVY_BG
        hdr.line.fill.background()
        tf_h = hdr.text_frame
        p_h = tf_h.paragraphs[0]
        p_h.text = m_name
        p_h.font.bold = True
        p_h.font.size = Pt(11)
        p_h.font.color.rgb = C_CYAN
        p_h.alignment = PP_ALIGN.CENTER

        tb = s11.shapes.add_textbox(Inches(x + 0.2), Inches(y + 0.5), Inches(3.2), Inches(1.8))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = m_fields
        p.font.size = Pt(9.5)
        p.font.color.rgb = C_DARK_TXT

    # =========================================================================
    # SLIDE 12: DEVELOPMENT PROGRESSION & TIMELINE
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    add_bg(s12)
    add_header(s12, "Project Progression", "Phased Development Milestones (Major Project Build)", "12")

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
        y = 1.55 + (i * 0.77)
        box = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(y), Inches(11.733), Inches(0.70))
        box.fill.solid()
        box.fill.fore_color.rgb = C_WHITE
        box.line.color.rgb = C_BORDER

        b = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.95), Inches(y + 0.12), Inches(0.7), Inches(0.45))
        b.fill.solid()
        b.fill.fore_color.rgb = C_TEAL
        b.line.fill.background()
        tf_b = b.text_frame
        p_b = tf_b.paragraphs[0]
        p_b.text = f"P{i+1}"
        p_b.font.bold = True
        p_b.font.size = Pt(11)
        p_b.font.color.rgb = C_WHITE
        p_b.alignment = PP_ALIGN.CENTER

        tb = s12.shapes.add_textbox(Inches(1.8), Inches(y + 0.05), Inches(10.5), Inches(0.6))
        tf = tb.text_frame
        tf.word_wrap = True

        pt = tf.paragraphs[0]
        pt.text = m_title
        pt.font.bold = True
        pt.font.size = Pt(11.5)
        pt.font.color.rgb = C_DARK_TXT

        pd = tf.add_paragraph()
        pd.text = m_desc
        pd.font.size = Pt(9.5)
        pd.font.color.rgb = C_MUTED_TXT

    # =========================================================================
    # SLIDE 13: REAL-WORLD APPLICATIONS
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    add_bg(s13)
    add_header(s13, "Applications & Use Cases", "Practical Deployment Scenarios for Pharmacy ERP", "13")

    apps = [
        ("Independent Retail Pharmacies", "Single-location medical stores that require quick barcode billing, automated FEFO expiry protection, and simplified daily GST bookkeeping.", C_TEAL),
        ("Hospital Outpatient Dispensaries", "High-volume hospital pharmacies that demand high-speed customer lookup, doctor-prescription tracking, and tight batch accountability.", C_NAVY_BG),
        ("Chain & Multi-Counter Stores", "Multi-terminal medical retail stores with designated cashier and store manager roles, preventing data tampering and stock leakage.", C_CYAN),
        ("Rural Healthcare Centers", "Low-overhead deployment capable of running on modest hardware and low bandwidth with reliable local SQLite storage and cloud synchronization.", C_GREEN)
    ]

    for i, (title, desc, col) in enumerate(apps):
        x = 0.8 if i % 2 == 0 else 6.8
        y = 1.6 if i < 2 else 4.2
        box = s13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(5.7), Inches(2.25))
        box.fill.solid()
        box.fill.fore_color.rgb = C_WHITE
        box.line.color.rgb = C_BORDER

        top_b = s13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(5.7), Inches(0.42))
        top_b.fill.solid()
        top_b.fill.fore_color.rgb = col
        top_b.line.fill.background()
        tf_tb = top_b.text_frame
        p_tb = tf_tb.paragraphs[0]
        p_tb.text = title.upper()
        p_tb.font.bold = True
        p_tb.font.size = Pt(11)
        p_tb.font.color.rgb = C_WHITE
        p_tb.alignment = PP_ALIGN.CENTER

        tb = s13.shapes.add_textbox(Inches(x + 0.3), Inches(y + 0.6), Inches(5.1), Inches(1.5))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = desc
        p.font.size = Pt(11)
        p.font.color.rgb = C_DARK_TXT

    # =========================================================================
    # SLIDE 14: FUTURE ROADMAP & PHASE 2
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    add_bg(s14)
    add_header(s14, "Future Scope", "Phase 2 Technological Roadmap", "14")

    future = [
        ("AI & Machine Learning", "• OCR-based doctor prescription parsing\n• Predictive medicine stock replenishment\n• Seasonal disease outbreak demand forecasting", C_TEAL),
        ("Mobile & REST API Ecosystem", "• Django REST Framework (DRF) API endpoints\n• Mobile Android/iOS apps for store owners\n• Bluetooth mobile thermal printer integration", C_CYAN),
        ("Communication Automation", "• WhatsApp Business Cloud API integration\n• Automated SMS digital receipt delivery\n• Automated low-stock email alerts to suppliers", C_AMBER),
        ("Enterprise Scalability & DevOps", "• Seamless migration from SQLite to PostgreSQL\n• Docker containerization & microservice scaling\n• Automated CI/CD pipeline deployment", C_NAVY_BG)
    ]

    for (title, desc, col), (x, y) in zip(future, [(0.8, 1.6), (6.8, 1.6), (0.8, 4.2), (6.8, 4.2)]):
        box = s14.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(5.7), Inches(2.25))
        box.fill.solid()
        box.fill.fore_color.rgb = C_WHITE
        box.line.color.rgb = C_BORDER

        top_b = s14.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(5.7), Inches(0.42))
        top_b.fill.solid()
        top_b.fill.fore_color.rgb = col
        top_b.line.fill.background()
        tf_tb = top_b.text_frame
        p_tb = tf_tb.paragraphs[0]
        p_tb.text = title.upper()
        p_tb.font.bold = True
        p_tb.font.size = Pt(11)
        p_tb.font.color.rgb = C_WHITE
        p_tb.alignment = PP_ALIGN.CENTER

        tb = s14.shapes.add_textbox(Inches(x + 0.3), Inches(y + 0.6), Inches(5.1), Inches(1.5))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = desc
        p.font.size = Pt(11)
        p.font.color.rgb = C_DARK_TXT

    # =========================================================================
    # SLIDE 15: CONCLUSION & PROJECT SUMMARY
    # =========================================================================
    s15 = prs.slides.add_slide(blank_layout)
    add_bg(s15, is_dark=True)

    c_box = s15.shapes.add_textbox(Inches(0.8), Inches(0.8), Inches(11.733), Inches(1.2))
    tf_c = c_box.text_frame
    p = tf_c.paragraphs[0]
    p.text = "CONCLUSION & SUMMARY"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = C_TEAL_LIGHT

    p2 = tf_c.add_paragraph()
    p2.text = "Transforming Retail Pharmacy into an Automated Digital Enterprise"
    p2.font.bold = True
    p2.font.size = Pt(24)
    p2.font.color.rgb = C_WHITE
    p2.space_before = Pt(4)

    concl_points = [
        ("Centralized Web Efficiency", "Successfully eliminated disjointed paper ledgers and fragmented software by consolidating POS, inventory, CRM, and analytics into one web platform."),
        ("Elimination of Expiry Losses", "Enforced automated FEFO batch allocation, preventing older stock from expiring unnoticed on shelves."),
        ("Compliance & Billing Speed", "Implemented dynamic reverse GST calculations and barcode scanning, enabling rapid, error-free checkout counter operations."),
        ("Auditability & Reverse Logistics", "Delivered barcode-verified customer returns desk with automatic shelf inventory recovery and ReturnSale audit logs."),
        ("Academic & Practical Success", "Fully implemented, tested, and cloud-deployed on PythonAnywhere with complete role-based security, ready for real-world deployment.")
    ]

    for i, (head, body) in enumerate(concl_points):
        y = 2.2 + (i * 0.95)
        card = s15.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(y), Inches(11.733), Inches(0.82))
        card.fill.solid()
        card.fill.fore_color.rgb = C_NAVY_ACCENT
        card.line.color.rgb = RGBColor(40, 80, 115)

        tb = card.text_frame
        tb.word_wrap = True
        p = tb.paragraphs[0]
        run_h = p.add_run()
        run_h.text = "✔  " + head + ": "
        run_h.font.bold = True
        run_h.font.size = Pt(12)
        run_h.font.color.rgb = C_CYAN

        run_b = p.add_run()
        run_b.text = body
        run_b.font.size = Pt(11)
        run_b.font.color.rgb = RGBColor(220, 230, 242)

    # Thank you footer
    ty = s15.shapes.add_textbox(Inches(0.8), Inches(6.4), Inches(11.733), Inches(0.6))
    tf_ty = ty.text_frame
    p_ty = tf_ty.paragraphs[0]
    p_ty.text = "THANK YOU  |  QUESTIONS & DISCUSSION"
    p_ty.font.bold = True
    p_ty.font.size = Pt(14)
    p_ty.font.color.rgb = C_TEAL
    p_ty.alignment = PP_ALIGN.CENTER

    out_file = "Pharmacy_Management_ERP_Major_Project.pptx"
    prs.save(out_file)
    print(f"SUCCESS: Saved 15 slides to {out_file}")

if __name__ == '__main__':
    create_deck()
