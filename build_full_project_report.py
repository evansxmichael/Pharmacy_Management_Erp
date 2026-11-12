"""
================================================================================
PHARMACY MANAGEMENT SYSTEM - MAJOR PROJECT COMPREHENSIVE FINAL REPORT BUILDER
================================================================================
Generates a publication-grade, academic B.Tech Final Project Report (Book / Journal)
conforming to Maulana Azad National Urdu University (MANUU) standards.

Authors:
- MD ZEESHAN (Roll No: 23BTCS026HY, Enrollment No: A230117)
- YUSUF HANZALA (Roll No: 23BTCS005HY, Enrollment No: A230093)
Supervisor: Dr. Nusrath Fathima, Assistant Professor, Dept. of CS & IT, MANUU
================================================================================
"""

import os
import sys
from PIL import Image as PILImage
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch, cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, 
    PageBreak, KeepTogether, HRFlowable, Preformatted
)
from reportlab.pdfgen import canvas

# ----------------------------------------------------------------------
# PATHS AND PALETTE CONFIGURATION
# ----------------------------------------------------------------------
BASE_DIR = r"C:\programming\erp_pharmacy_project"
ASSETS_DIR = os.path.join(BASE_DIR, "report_assets")
PDF_OUTPUT = os.path.join(BASE_DIR, "Pharmacy_Management_System_Final_Project_Report.pdf")

C_TEAL = colors.HexColor("#008B8B")
C_DARK_TEAL = colors.HexColor("#005F5F")
C_NAVY = colors.HexColor("#0C1F30")
C_SLATE = colors.HexColor("#1E293B")
C_LIGHT_BG = colors.HexColor("#F8F9FA")
C_CARD_BG = colors.HexColor("#F1F5F9")
C_BORDER = colors.HexColor("#CBD5E1")
C_TEXT_DARK = colors.HexColor("#0F172A")
C_TEXT_MUTED = colors.HexColor("#475569")
C_RED = colors.HexColor("#DC2626")
C_GREEN = colors.HexColor("#16A34A")
C_AMBER = colors.HexColor("#D97706")
C_CODE_BG = colors.HexColor("#0F172A")
C_CODE_TEXT = colors.HexColor("#F8FAFC")

PAGE_WIDTH, PAGE_HEIGHT = A4
PRINTABLE_WIDTH = PAGE_WIDTH - 108  # 54pt (0.75 in) margins each side = 487.27 pt

# ----------------------------------------------------------------------
# NUMBERED CANVAS (Academic Running Header & Dual Page Numbering)
# ----------------------------------------------------------------------
# Pages 1 to 6 are Front Matter:
#   Page 1: Cover Page (no header, no footer)
#   Page 2: Certificate (Footer: ii)
#   Page 3: Declaration (Footer: iii)
#   Page 4: Acknowledgement (Footer: iv)
#   Page 5: Abstract (Footer: v)
#   Page 6: Table of Contents (Footer: vi)
# Page 7 onwards is Main Body:
#   Chapter 1 onwards (Page 1 of N, Page 2 of N...) with top running header.

class AcademicNumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        main_body_start_page = 7
        total_main_pages = max(1, num_pages - (main_body_start_page - 1))

        roman_numerals = ["", "i", "ii", "iii", "iv", "v", "vi", "vii", "viii"]

        for state in self._saved_page_states:
            self.__dict__.update(state)
            p_num = self._pageNumber
            width, height = A4

            if p_num == 1:
                # Cover Page: Draw academic double frame
                self.saveState()
                self.setStrokeColor(C_DARK_TEAL)
                self.setLineWidth(2)
                self.rect(28, 28, width - 56, height - 56)
                self.setStrokeColor(C_TEAL)
                self.setLineWidth(0.8)
                self.rect(33, 33, width - 66, height - 66)
                self.restoreState()
            elif p_num < main_body_start_page:
                # Front Matter (Pages 2-6): Roman Numerals in bottom footer
                self.saveState()
                self.setStrokeColor(C_BORDER)
                self.setLineWidth(0.5)
                self.line(54, 45, width - 54, 45)
                self.setFont("Helvetica", 9)
                self.setFillColor(C_TEXT_MUTED)
                r_num = roman_numerals[p_num] if p_num < len(roman_numerals) else str(p_num)
                self.drawRightString(width - 54, 32, r_num)
                self.restoreState()
            else:
                # Main Body (Page 7 onwards): Running Header + Arabic Page Numbering
                main_p_num = p_num - (main_body_start_page - 1)
                self.saveState()
                # Running Header
                self.setStrokeColor(C_BORDER)
                self.setLineWidth(0.6)
                self.line(54, height - 42, width - 54, height - 42)

                self.setFont("Helvetica-Bold", 8)
                self.setFillColor(C_DARK_TEAL)
                self.drawString(54, height - 35, "PHARMACY MANAGEMENT SYSTEM — MAJOR PROJECT REPORT")

                self.setFont("Helvetica", 8)
                self.setFillColor(C_TEXT_MUTED)
                self.drawRightString(width - 54, height - 35, "MANUU · DEPT. OF CS & IT (2026-27)")

                # Running Footer
                self.setStrokeColor(C_BORDER)
                self.setLineWidth(0.6)
                self.line(54, 45, width - 54, 45)

                self.setFont("Helvetica", 8)
                self.setFillColor(C_TEXT_MUTED)
                self.drawString(54, 32, "B.Tech (Computer Science) · Centralized Web-Based ERP Platform")

                self.setFont("Helvetica-Bold", 8.5)
                self.setFillColor(C_DARK_TEAL)
                self.drawRightString(width - 54, 32, f"Page {main_p_num} of {total_main_pages}")
                self.restoreState()

            super().showPage()
        super().save()

# ----------------------------------------------------------------------
# STYLES DEFINITION
# ----------------------------------------------------------------------
styles = getSampleStyleSheet()

style_cover_title = ParagraphStyle(
    'CoverTitle',
    fontName='Helvetica-Bold',
    fontSize=22,
    leading=28,
    alignment=TA_CENTER,
    textColor=C_NAVY,
    spaceAfter=8
)

style_cover_sub = ParagraphStyle(
    'CoverSubtitle',
    fontName='Helvetica-Bold',
    fontSize=13,
    leading=18,
    alignment=TA_CENTER,
    textColor=C_TEAL,
    spaceAfter=14
)

style_cover_desc = ParagraphStyle(
    'CoverDesc',
    fontName='Helvetica',
    fontSize=9.5,
    leading=14.5,
    alignment=TA_CENTER,
    textColor=C_SLATE,
    spaceAfter=10
)

style_chap_num = ParagraphStyle(
    'ChapterNumber',
    fontName='Helvetica-Bold',
    fontSize=12,
    leading=16,
    alignment=TA_LEFT,
    textColor=C_TEAL,
    spaceAfter=4,
    spaceBefore=4
)

style_chap_title = ParagraphStyle(
    'ChapterTitle',
    fontName='Helvetica-Bold',
    fontSize=18,
    leading=23,
    alignment=TA_LEFT,
    textColor=C_NAVY,
    spaceAfter=12
)

style_sec_title = ParagraphStyle(
    'SecTitle',
    fontName='Helvetica-Bold',
    fontSize=12.5,
    leading=16.5,
    alignment=TA_LEFT,
    textColor=C_DARK_TEAL,
    spaceBefore=11,
    spaceAfter=5
)

style_subsec_title = ParagraphStyle(
    'SubSecTitle',
    fontName='Helvetica-Bold',
    fontSize=10.5,
    leading=14.5,
    alignment=TA_LEFT,
    textColor=C_SLATE,
    spaceBefore=7,
    spaceAfter=3
)

style_body = ParagraphStyle(
    'Body',
    fontName='Helvetica',
    fontSize=9.2,
    leading=14,
    alignment=TA_JUSTIFY,
    textColor=C_TEXT_DARK,
    spaceAfter=7
)

style_bullet = ParagraphStyle(
    'Bullet',
    fontName='Helvetica',
    fontSize=9,
    leading=13.5,
    alignment=TA_JUSTIFY,
    textColor=C_TEXT_DARK,
    leftIndent=14,
    firstLineIndent=-9,
    spaceAfter=3.5
)

style_caption = ParagraphStyle(
    'Caption',
    fontName='Helvetica-Bold',
    fontSize=8.2,
    leading=11.5,
    alignment=TA_CENTER,
    textColor=C_TEXT_MUTED,
    spaceBefore=5,
    spaceAfter=11
)

style_code = ParagraphStyle(
    'CodeStyle',
    fontName='Courier',
    fontSize=7.5,
    leading=10,
    textColor=C_CODE_TEXT,
    alignment=TA_LEFT
)

style_th = ParagraphStyle(
    'TH',
    fontName='Helvetica-Bold',
    fontSize=8.2,
    leading=11,
    alignment=TA_CENTER,
    textColor=colors.white
)

style_td = ParagraphStyle(
    'TD',
    fontName='Helvetica',
    fontSize=7.8,
    leading=10.5,
    alignment=TA_LEFT,
    textColor=C_TEXT_DARK
)

style_td_center = ParagraphStyle(
    'TDCenter',
    fontName='Helvetica',
    fontSize=7.8,
    leading=10.5,
    alignment=TA_CENTER,
    textColor=C_TEXT_DARK
)

# ----------------------------------------------------------------------
# HELPER FLOWABLE BUILDERS
# ----------------------------------------------------------------------
def make_callout(title, text, bg_color=C_CARD_BG, border_color=C_TEAL):
    t_style = ParagraphStyle('CTitle', fontName='Helvetica-Bold', fontSize=9, leading=12, textColor=border_color)
    p_style = ParagraphStyle('CText', fontName='Helvetica', fontSize=8.5, leading=12.5, textColor=C_TEXT_DARK)
    content = [
        Paragraph(f"<b>{title}</b>", t_style),
        Spacer(1, 2),
        Paragraph(text, p_style)
    ]
    t = Table([[content]], colWidths=[PRINTABLE_WIDTH])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), bg_color),
        ('BOX', (0,0), (-1,-1), 0.5, C_BORDER),
        ('LINELEFT', (0,0), (0,0), 3.5, border_color),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    return t

def make_code_card(code_str, filename=""):
    header_p = Paragraph(f"<b>Source Artifact:</b> <font color='#38bdf8'>{filename}</font>", 
                         ParagraphStyle('CodeH', fontName='Helvetica-Bold', fontSize=7.8, leading=10, textColor=colors.HexColor("#94a3b8")))
    code_p = Preformatted(code_str, style_code)
    
    t = Table([[header_p], [code_p]], colWidths=[PRINTABLE_WIDTH])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#09101d")),
        ('BACKGROUND', (0,1), (-1,1), C_CODE_BG),
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor("#334155")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#1e293b")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 9),
        ('RIGHTPADDING', (0,0), (-1,-1), 9),
    ]))
    return KeepTogether(t)

def make_scaled_image(rel_path, target_width=PRINTABLE_WIDTH, max_height=260):
    full_path = os.path.join(ASSETS_DIR, rel_path)
    if not os.path.exists(full_path):
        return Paragraph(f"[Image Missing: {rel_path}]", style_caption)
    with PILImage.open(full_path) as im:
        orig_w, orig_h = im.size
    
    ratio = orig_h / orig_w
    w = target_width
    h = w * ratio
    if max_height and h > max_height:
        h = max_height
        w = h / ratio
    return Image(full_path, width=w, height=h)

def make_figure_block(rel_path, caption, target_width=PRINTABLE_WIDTH, max_height=250):
    img = make_scaled_image(rel_path, target_width=target_width, max_height=max_height)
    cap = Paragraph(caption, style_caption)
    return KeepTogether([img, cap])

# ----------------------------------------------------------------------
# BUILD DOCUMENT
# ----------------------------------------------------------------------
def build_report():
    story = []
    
    # ==================================================================
    # PAGE 1: COVER PAGE
    # ==================================================================
    story.append(Spacer(1, 14))
    story.append(Paragraph("A PROJECT REPORT ON", ParagraphStyle('CR1', fontName='Helvetica-Bold', fontSize=11, alignment=TA_CENTER, textColor=C_TEXT_MUTED)))
    story.append(Spacer(1, 6))
    story.append(Paragraph("PHARMACY MANAGEMENT SYSTEM", style_cover_title))
    story.append(Paragraph("A Centralized Web-Based Enterprise Resource Planning (ERP) Platform", style_cover_sub))
    story.append(HRFlowable(width="60%", thickness=1.5, color=C_TEAL, spaceBefore=2, spaceAfter=12, hAlign='CENTER'))
    
    story.append(Paragraph(
        "Submitted in partial fulfillment of the requirements for the award of the degree of<br/>"
        "<b>BACHELOR OF TECHNOLOGY</b><br/>"
        "in<br/>"
        "<b>COMPUTER SCIENCE & INFORMATION TECHNOLOGY</b><br/>"
        "<b>Academic Session: 2026 – 2027</b>",
        style_cover_desc
    ))
    story.append(Spacer(1, 8))
    
    # Student and Supervisor Info Table
    sub_text = (
        "<b>Submitted By:</b><br/>"
        "<b>MD ZEESHAN</b> — 23BTCS026HY (Enrollment: A230117)<br/>"
        "<b>YUSUF HANZALA</b> — 23BTCS005HY (Enrollment: A230093)<br/>"
        "<i>B.Tech (CS) VII Semester</i>"
    )
    sup_text = (
        "<b>Under the Supervision of:</b><br/>"
        "<b>Dr. Nusrath Fathima</b><br/>"
        "Assistant Professor<br/>"
        "Department of CS & IT, MANUU"
    )
    t_names = Table([
        [Paragraph(sub_text, ParagraphStyle('SN', fontName='Helvetica', fontSize=8.8, leading=13.5, alignment=TA_LEFT)),
         Paragraph(sup_text, ParagraphStyle('SP', fontName='Helvetica', fontSize=8.8, leading=13.5, alignment=TA_RIGHT))]
    ], colWidths=[PRINTABLE_WIDTH*0.55, PRINTABLE_WIDTH*0.45])
    t_names.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(t_names)
    story.append(Spacer(1, 16))
    
    # Emblem
    emblem_path = os.path.join(ASSETS_DIR, "manuu_emblem.png")
    if os.path.exists(emblem_path):
        story.append(Image(emblem_path, width=82, height=121))
    story.append(Spacer(1, 14))
    
    # Institution Footer
    story.append(Paragraph("<b>DEPARTMENT OF COMPUTER SCIENCE & INFORMATION TECHNOLOGY</b>", ParagraphStyle('Inst1', fontName='Helvetica-Bold', fontSize=10.5, alignment=TA_CENTER, textColor=C_RED)))
    story.append(Paragraph("<b>SCHOOL OF TECHNOLOGY</b>", ParagraphStyle('Inst2', fontName='Helvetica-Bold', fontSize=10, alignment=TA_CENTER, textColor=C_NAVY)))
    story.append(Paragraph("<b>MAULANA AZAD NATIONAL URDU UNIVERSITY</b>", ParagraphStyle('Inst3', fontName='Helvetica-Bold', fontSize=12, alignment=TA_CENTER, textColor=C_NAVY)))
    story.append(Paragraph("(A Central University Accredited with Grade \"A+\" by NAAC)<br/>Gachibowli, Hyderabad, Telangana – 500032 (India)", ParagraphStyle('Inst4', fontName='Helvetica', fontSize=8.5, leading=12, alignment=TA_CENTER, textColor=C_TEXT_MUTED)))
    story.append(PageBreak())

    # ==================================================================
    # PAGE 2: CERTIFICATE (Page ii)
    # ==================================================================
    header_banner = os.path.join(ASSETS_DIR, "manuu_header_banner.jpg")
    if os.path.exists(header_banner):
        story.append(Image(header_banner, width=PRINTABLE_WIDTH, height=52))
        story.append(Spacer(1, 14))
    
    story.append(Paragraph("<b>Date: 13 November, 2026</b>", ParagraphStyle('D', fontName='Helvetica-Bold', fontSize=9.5, alignment=TA_RIGHT)))
    story.append(Spacer(1, 8))
    story.append(Paragraph("<u>CERTIFICATE</u>", ParagraphStyle('C', fontName='Helvetica-Bold', fontSize=15, alignment=TA_CENTER, textColor=C_NAVY)))
    story.append(Spacer(1, 16))
    
    cert_body = (
        "This is to certify that the major project report entitled <b>\"PHARMACY MANAGEMENT SYSTEM – "
        "A CENTRALIZED WEB-BASED ERP PLATFORM\"</b> submitted by <b>MD ZEESHAN</b> bearing Roll No. "
        "<b>23BTCS026HY</b> (Enrollment No. <b>A230117</b>) and <b>YUSUF HANZALA</b> bearing Roll No. "
        "<b>23BTCS005HY</b> (Enrollment No. <b>A230093</b>) in partial fulfillment of the requirements "
        "for the award of the degree of <b>Bachelor of Technology (Computer Science) - VII Semester</b> during the "
        "academic session <b>2026-27</b> in the Department of Computer Science & Information Technology, "
        "School of Technology, Maulana Azad National Urdu University, Hyderabad, is an authentic and bonafide "
        "record of work carried out by them under my guidance and supervision.<br/><br/>"
        "To the best of my knowledge, the matter embodied in this project report has not been submitted "
        "elsewhere for the award of any other degree or diploma."
    )
    story.append(Paragraph(cert_body, style_body))
    story.append(Spacer(1, 65))
    
    t_signs = Table([
        [Paragraph("<b>____________________________</b><br/><b>External Examiner</b>", ParagraphStyle('E', fontName='Helvetica', fontSize=8.8, alignment=TA_LEFT, leading=14)),
         Paragraph("<b>____________________________</b><br/><b>Dr. Nusrath Fathima</b><br/>Assistant Professor & Supervisor<br/>CS & IT, MANUU", ParagraphStyle('S', fontName='Helvetica', fontSize=8.8, alignment=TA_RIGHT, leading=14))]
    ], colWidths=[PRINTABLE_WIDTH*0.5, PRINTABLE_WIDTH*0.5])
    story.append(t_signs)
    story.append(Spacer(1, 35))
    story.append(Paragraph("<b>____________________________</b><br/><b>Prof. Pradeep Kumar</b><br/>Head of Department, CS & IT, MANUU", ParagraphStyle('HOD', fontName='Helvetica', fontSize=8.8, alignment=TA_CENTER, leading=14)))
    story.append(PageBreak())

    # ==================================================================
    # PAGE 3: DECLARATION (Page iii)
    # ==================================================================
    if os.path.exists(header_banner):
        story.append(Image(header_banner, width=PRINTABLE_WIDTH, height=52))
        story.append(Spacer(1, 14))
    
    story.append(Paragraph("<u>CANDIDATE'S DECLARATION</u>", ParagraphStyle('CD', fontName='Helvetica-Bold', fontSize=15, alignment=TA_CENTER, textColor=C_NAVY)))
    story.append(Spacer(1, 16))
    
    decl_body = (
        "We hereby declare that the project work presented in this report entitled <b>\"PHARMACY MANAGEMENT "
        "SYSTEM – A CENTRALIZED WEB-BASED ERP PLATFORM\"</b> towards the partial fulfillment of the requirement "
        "for the award of the degree of <b>BACHELOR OF TECHNOLOGY (COMPUTER SCIENCE)</b> submitted in the "
        "Department of Computer Science & Information Technology, Maulana Azad National Urdu University, Hyderabad, "
        "is an authentic and original record of our own work carried out under the esteemed guidance of "
        "<b>Dr. Nusrath Fathima</b> (Assistant Professor, Dept. CS & IT).<br/><br/>"
        "We have not submitted the matter embodied in this project report for the award of any other degree, "
        "diploma, or fellowship to any other University or Institute of higher learning."
    )
    story.append(Paragraph(decl_body, style_body))
    story.append(Spacer(1, 18))
    story.append(Paragraph("<b>Date:</b> 13 November, 2026<br/><b>Place:</b> Hyderabad", ParagraphStyle('DP', fontName='Helvetica', fontSize=9, leading=14)))
    story.append(Spacer(1, 55))
    
    t_cands = Table([
        [Paragraph("<b>MD ZEESHAN</b><br/>Roll No: 23BTCS026HY<br/>Enrollment No: A230117", ParagraphStyle('C1', fontName='Helvetica', fontSize=8.8, alignment=TA_LEFT, leading=14)),
         Paragraph("<b>YUSUF HANZALA</b><br/>Roll No: 23BTCS005HY<br/>Enrollment No: A230093", ParagraphStyle('C2', fontName='Helvetica', fontSize=8.8, alignment=TA_RIGHT, leading=14))]
    ], colWidths=[PRINTABLE_WIDTH*0.5, PRINTABLE_WIDTH*0.5])
    story.append(t_cands)
    story.append(PageBreak())

    # ==================================================================
    # PAGE 4: ACKNOWLEDGEMENT (Page iv)
    # ==================================================================
    if os.path.exists(header_banner):
        story.append(Image(header_banner, width=PRINTABLE_WIDTH, height=52))
        story.append(Spacer(1, 14))
    
    story.append(Paragraph("<u>ACKNOWLEDGEMENT</u>", ParagraphStyle('ACK', fontName='Helvetica-Bold', fontSize=15, alignment=TA_CENTER, textColor=C_NAVY)))
    story.append(Spacer(1, 16))
    
    ack_body = (
        "We express our profound and sincere gratitude towards our <b>Supervisor Dr. Nusrath Fathima</b>, "
        "Assistant Professor, Department of Computer Science and Information Technology, Maulana Azad National "
        "Urdu University, Hyderabad, for her continuous encouragement, invaluable guidance, and perceptive feedback "
        "throughout the design, development, and technical documentation of this project.<br/><br/>"
        "We are deeply indebted to our <b>Project Coordinator Dr. Ahmed Talha Siddiqui</b>, Assistant Professor, "
        "Department of Computer Science and Information Technology, for his insightful suggestions, technical advice, "
        "and administrative coordination. In spite of his demanding schedule, he was always accessible to steer us "
        "through critical project milestones.<br/><br/>"
        "We sincerely thank <b>Prof. Abdul Wahid</b>, Dean, School of Technology, and <b>Prof. Pradeep Kumar</b>, "
        "Head, Department of Computer Science and Information Technology, for providing the institutional support, "
        "computing infrastructure, and academic ambiance necessary for the successful completion of our degree requirements.<br/><br/>"
        "We also convey our sincere respect to the Honorable <b>Vice Chancellor, Prof. Syed Ainul Hasan</b>, for "
        "fostering an exemplary academic environment that inspires students to pursue excellence in technology.<br/><br/>"
        "Finally, we express our heartfelt thanks to our families, lab instructors, and fellow classmates for their "
        "unwavering moral support and collaborative spirit throughout our B.Tech journey at MANUU."
    )
    story.append(Paragraph(ack_body, style_body))
    story.append(Spacer(1, 35))
    story.append(Paragraph("<b>MD ZEESHAN (23BTCS026HY)</b><br/><b>YUSUF HANZALA (23BTCS005HY)</b>", ParagraphStyle('Signs', fontName='Helvetica-Bold', fontSize=9, alignment=TA_RIGHT, leading=15)))
    story.append(PageBreak())

    # ==================================================================
    # PAGE 5: ABSTRACT & SYSTEM OVERVIEW (Page v)
    # ==================================================================
    story.append(Paragraph("ABSTRACT", style_chap_title))
    story.append(HRFlowable(width="100%", thickness=1, color=C_TEAL, spaceBefore=2, spaceAfter=10))
    
    abs_text = (
        "The pharmaceutical retail sector operates within a high-stakes, tightly regulated environment requiring "
        "absolute accuracy in inventory tracking, dynamic tax calculations, and regulatory compliance. Traditional "
        "pharmacy operations in India predominantly rely on disparate offline accounting packages, manual paper registers, "
        "or generic retail software. This fragmentation leads to critical failure points, including overlooked medicine expiry "
        "(causing severe dead-stock financial losses), slow billing queues, calculation errors in Goods and Services Tax (GST), "
        "untraceable batch numbers during recalls, and complete absence of real-time financial visibility for store owners.<br/><br/>"
        "To overcome these operational challenges, this project presents the <b>Pharmacy Management System (Pharmacy ERP)</b>, "
        "an enterprise-grade, full-stack web-based platform specifically engineered around the operational workflows of retail medical stores. "
        "Built using a robust three-tier Model-View-Template (MVT) architecture powered by <b>Python 3.14</b>, <b>Django 6.0.4</b>, "
        "and a normalized <b>SQLite</b> relational database (PostgreSQL-ready), the system delivers six core architectural innovations: "
        "<b>(1) Algorithmic FEFO (First-Expire-First-Out) Inventory Protection</b> that automatically allocates sales from the earliest expiring "
        "batches; <b>(2) Dynamic Reverse GST Calculation</b> compliant with Indian pharmaceutical HSN slabs; <b>(3) Asynchronous Patient CRM</b> "
        "via AJAX for sub-second returning customer lookups; <b>(4) High-Speed POS Counter</b> supporting USB/Bluetooth barcode guns and "
        "instant CODE128 thermal receipt generation; <b>(5) Reverse Logistics & Return Desk</b> with audit trails; and <b>(6) Executive Business "
        "Intelligence Dashboards</b> offering real-time profit tracking, asset valuation, and automated CSV Purchase Order reorder generation.<br/><br/>"
        "The system has been production-hardened with three-level Role-Based Access Control (RBAC), banking-grade session security, "
        "environment variable isolation (.env), and complete mobile responsiveness across all viewports. The application is successfully "
        "deployed in the cloud via <b>PythonAnywhere</b> PaaS with WSGI interfacing, establishing a production-ready foundation for commercial pharmacy operations."
    )
    story.append(Paragraph(abs_text, style_body))
    story.append(Spacer(1, 8))
    story.append(make_callout(
        "Key Project Metrics & Innovations",
        "• <b>Full Architecture:</b> Django 6.0.4 MVT · SQLite ORM · Bootstrap 5.3 · Vanilla JS ES6 · Select2 · JsBarcode · Chart.js<br/>"
        "• <b>Algorithmic Modules:</b> Dynamic FEFO Batch Depletion · Indian GST Reverse Calculator · Event-Driven Django Signals<br/>"
        "• <b>Production Footprint:</b> Cloud hosted on PythonAnywhere Linux PaaS · 100% Mobile Responsive UI · Banking Session Timeout (1800s)"
    ))
    story.append(PageBreak())

    # ==================================================================
    # PAGE 6: TABLE OF CONTENTS (Single-Page Fit - Page vi)
    # ==================================================================
    story.append(Paragraph("TABLE OF CONTENTS", style_chap_title))
    story.append(HRFlowable(width="100%", thickness=1, color=C_TEAL, spaceBefore=2, spaceAfter=8))
    
    # Accurate page numbers mapped to Main Body starting on page 7 (which is Chapter 1 = Page 1 of Main Body)
    toc_data = [
        [Paragraph("<b>Certificate of Authenticity</b>", style_td), Paragraph("<b>ii</b>", style_td_center)],
        [Paragraph("<b>Candidate's Declaration</b>", style_td), Paragraph("<b>iii</b>", style_td_center)],
        [Paragraph("<b>Acknowledgement</b>", style_td), Paragraph("<b>iv</b>", style_td_center)],
        [Paragraph("<b>Abstract</b>", style_td), Paragraph("<b>v</b>", style_td_center)],
        [Paragraph("<b>Chapter 1: Introduction & Domain Context</b>", style_td), Paragraph("<b>1</b>", style_td_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;1.1 Project Overview & Significance · 1.2 Problem Statement", style_td), Paragraph("1", style_td_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;1.3 Project Objectives · 1.4 Scope · 1.5 Report Organization", style_td), Paragraph("2", style_td_center)],
        [Paragraph("<b>Chapter 2: Feasibility Study & System Requirements</b>", style_td), Paragraph("<b>3</b>", style_td_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;2.1 Technical · 2.2 Operational · 2.3 Economic Feasibility", style_td), Paragraph("3", style_td_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;2.4 Hardware Specs · 2.5 Software Technology Stack Table", style_td), Paragraph("4", style_td_center)],
        [Paragraph("<b>Chapter 3: System Analysis & Engineering Methodology</b>", style_td), Paragraph("<b>5</b>", style_td_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;3.1 Requirements · 3.2 Waterfall SDLC · 3.3 Three-Tier Architecture", style_td), Paragraph("5", style_td_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;3.4 Billing Workflow Loop · 3.5 Deployment Strategy", style_td), Paragraph("5", style_td_center)],
        [Paragraph("<b>Chapter 4: System Design & Visual Modeling</b>", style_td), Paragraph("<b>6</b>", style_td_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;4.1 Functional Module Breakdown · 4.2 Level 0 Context DFD", style_td), Paragraph("6", style_td_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;4.3 Level 1 Decomposition DFD & Functional Processes", style_td), Paragraph("7", style_td_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;4.4 Database Schema & Entity Relationship (ER) Diagram", style_td), Paragraph("8", style_td_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;4.5 Data Dictionary & Relational Tables Specification", style_td), Paragraph("8", style_td_center)],
        [Paragraph("<b>Chapter 5: Technical Implementation & Core Algorithms</b>", style_td), Paragraph("<b>11</b>", style_td_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;5.1 Django MVT Engine · 5.2 Algorithmic FEFO Engine", style_td), Paragraph("11", style_td_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;5.3 Dynamic Reverse GST · 5.4 Event-Driven Signals · 5.5 AJAX", style_td), Paragraph("12", style_td_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;5.6 Barcode CODE128 · 5.7 Mobile Viewports · 5.8 Source Code", style_td), Paragraph("13", style_td_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;5.9 User Interface Snapshots & Operational Walkthrough", style_td), Paragraph("14", style_td_center)],
        [Paragraph("<b>Chapter 6: System Verification & Quality Assurance</b>", style_td), Paragraph("<b>18</b>", style_td_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;6.1 Quality Assurance Strategy · 6.2 Formal Test Matrix Table", style_td), Paragraph("18", style_td_center)],
        [Paragraph("<b>Chapter 7: Security Architecture & Cloud Deployment</b>", style_td), Paragraph("<b>19</b>", style_td_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;7.1 RBAC · 7.2 Session Timeout · 7.3 PythonAnywhere Deployment", style_td), Paragraph("19", style_td_center)],
        [Paragraph("<b>Chapter 8: Conclusion & Future Scope</b>", style_td), Paragraph("<b>20</b>", style_td_center)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;8.1 Concluding Remarks · 8.2 Phase 2 Strategic Roadmap", style_td), Paragraph("20", style_td_center)],
        [Paragraph("<b>Chapter 9: References & Bibliography</b>", style_td), Paragraph("<b>21</b>", style_td_center)],
    ]
    t_toc = Table(toc_data, colWidths=[PRINTABLE_WIDTH*0.9, PRINTABLE_WIDTH*0.1])
    t_toc.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.2),
        ('TOPPADDING', (0,0), (-1,-1), 1.2),
        ('LINEBELOW', (0,0), (-1,-1), 0.3, colors.HexColor("#E2E8F0")),
    ]))
    story.append(t_toc)
    story.append(PageBreak())

    # ==================================================================
    # CHAPTER 1: INTRODUCTION & DOMAIN CONTEXT (Main Body Page 1)
    # ==================================================================
    story.append(Paragraph("CHAPTER 1", style_chap_num))
    story.append(Paragraph("INTRODUCTION & PROBLEM DEFINITION", style_chap_title))
    story.append(HRFlowable(width="100%", thickness=1.5, color=C_TEAL, spaceBefore=2, spaceAfter=10))
    
    # 3D Hero Poster
    story.append(make_figure_block("project_hero_poster.jpg", "<b>Figure 1.1:</b> Architectural Overview of the Centralized Pharmacy Management ERP System", target_width=PRINTABLE_WIDTH, max_height=175))
    story.append(Spacer(1, 4))

    story.append(Paragraph("1.1 Project Overview & Significance", style_sec_title))
    story.append(Paragraph(
        "The retail pharmaceutical enterprise is fundamentally distinct from general fast-moving consumer goods (FMCG) "
        "retail. Every medicine unit sold is legally tied to strict regulatory compliances: it possesses a unique <b>batch number</b>, "
        "a non-negotiable <b>expiry date</b>, specific <b>manufacturer details</b>, and a mandated <b>Goods and Services Tax (GST) slab</b>. "
        "Furthermore, pharmacists do not merely sell merchandise; they dispense health-critical consumables that require "
        "prescriptions, patient tracking, and verified physician details.<br/><br/>"
        "The <b>Pharmacy Management System (Pharmacy ERP)</b> is an enterprise-grade web application created to transition "
        "medical stores from fragmented, manual record-keeping to a unified, automated digital command center. By centralizing "
        "Point of Sale (POS) billing, batch-wise stock control, patient relationship management, and financial reporting into "
        "one cohesive cloud platform, the system eliminates operational errors, safeguards inventory value, and provides store owners "
        "with complete transparency into their business health.",
        style_body
    ))

    story.append(Paragraph("1.2 Problem Statement & Industry Bottlenecks", style_sec_title))
    story.append(Paragraph(
        "Field investigations into traditional standalone pharmacy operations reveal severe operational bottlenecks that "
        "consistently impair efficiency and cause financial losses:",
        style_body
    ))
    
    bottlenecks = [
        "<b>Inventory Decay & Expired Stock Losses:</b> Medical stores stock thousands of stock-keeping units (SKUs). Without batch-level tracking, older batches sit hidden at the back of shelves while newer consignments are inadvertently dispensed. When expired items are eventually discovered, they represent an absolute financial write-off.",
        "<b>Billing Bottlenecks & Human Calculation Error:</b> During peak evening footfalls, manual calculation of discounts, taxes, and itemized totals creates long queues. Counter staff frequently miscalculate complex reverse GST percentages.",
        "<b>Lack of Customer Continuity & History:</b> Returning patients frequently request prescription refills without remembering the exact trade names of their medicines. Disconnected systems force cashiers to re-enter patient profiles on every single visit.",
        "<b>Absence of Real-Time Financial Visibility:</b> Store owners rarely know their exact daily gross revenue, net margin, or physical cash drawer balance until hours after closing, preventing proactive inventory procurement.",
        "<b>Security Loopholes & Insider Shrinkage:</b> Generic software lacks strict Role-Based Access Control (RBAC). Cashiers often possess access to sensitive financial metrics, margins, and deletion controls, leaving the pharmacy vulnerable to data manipulation."
    ]
    for b in bottlenecks:
        story.append(Paragraph(f"• {b}", style_bullet))
    story.append(Spacer(1, 6))

    story.append(Paragraph("1.3 Project Objectives", style_sec_title))
    story.append(Paragraph(
        "To decisively overcome the aforementioned industry challenges, this project was developed with the following primary objectives:",
        style_body
    ))
    objectives = [
        "<b>Centralized Web-Based ERP:</b> Architect a secure, multi-user web portal accessible across local terminals and cloud platforms.",
        "<b>Automated FEFO Inventory Engine:</b> Implement an algorithmic First-Expire-First-Out dispatcher that systematically sells nearest-expiry batches first.",
        "<b>High-Velocity POS Terminal:</b> Build an intuitive counter terminal supporting substring medicine searches and instant barcode scanner inputs.",
        "<b>Compliant Indian GST Billing:</b> Engineer a dynamic reverse-tax calculation engine that separates base taxable value from CGST and SGST.",
        "<b>Smart Patient CRM:</b> Enable sub-second asynchronous customer lookup via telephone numbers to auto-populate patient records.",
        "<b>Reverse Logistics & Returns Desk:</b> Provide scannable bill barcode verification with audit trails and optional batch restocking.",
        "<b>Executive BI Dashboards:</b> Deliver live visual charts for revenue, gross margin, cash vs. UPI collection, and one-click purchase order CSV generation.",
        "<b>Multi-Layered Security & Mobile Ergonomics:</b> Enforce 3-tier Role-Based Access Control and full multi-viewport mobile responsiveness."
    ]
    for o in objectives:
        story.append(Paragraph(f"✓ {o}", style_bullet))
    story.append(Spacer(1, 6))

    story.append(Paragraph("1.4 Scope of the System", style_sec_title))
    story.append(Paragraph(
        "The scope of this project encompasses the complete operational spectrum of single and multi-counter retail medical stores. "
        "The software caters to three primary operational personas: (1) <b>Store Owners / Administrators</b> who require high-level "
        "financial intelligence and master schema authority; (2) <b>Store Managers</b> who oversee wholesale consignments, batch entries, "
        "and inventory audits; and (3) <b>Counter Cashiers</b> who operate the high-speed POS billing terminal.",
        style_body
    ))

    story.append(Paragraph("1.5 Report Organization", style_sec_title))
    story.append(Paragraph(
        "This project documentation is organized into nine structured chapters: Chapter 1 outlines domain context; Chapter 2 covers feasibility "
        "and technology stack; Chapter 3 details system analysis and methodology; Chapter 4 provides DFDs, ER modeling, and schemas; Chapter 5 "
        "thoroughly documents implementation, algorithms, and code; Chapter 6 reports testing and QA results; Chapter 7 examines security and deployment; "
        "Chapter 8 presents conclusions; and Chapter 9 lists references.",
        style_body
    ))
    story.append(PageBreak())

    # ==================================================================
    # CHAPTER 2: FEASIBILITY STUDY & SYSTEM REQUIREMENTS
    # ==================================================================
    story.append(Paragraph("CHAPTER 2", style_chap_num))
    story.append(Paragraph("FEASIBILITY STUDY & SYSTEM REQUIREMENTS", style_chap_title))
    story.append(HRFlowable(width="100%", thickness=1.5, color=C_TEAL, spaceBefore=2, spaceAfter=10))

    story.append(Paragraph("2.1 Technical Feasibility Analysis", style_sec_title))
    story.append(Paragraph(
        "Technical feasibility assesses whether the proposed solution can be successfully constructed using proven, reliable, and "
        "readily available computing technologies. The technical feasibility of this project is established through the following framework:",
        style_body
    ))
    tech_points = [
        "<b>Python 3.14 Programming Language:</b> Selected for its mature ecosystem, concise syntax, high reliability, and exceptional community support. Python offers native mathematical precision required for pharmaceutical ledger computations.",
        "<b>Django 6.0.4 Web Framework:</b> Django adheres strictly to the 'batteries-included' philosophy, providing built-in protection against SQL injection, XSS, and CSRF, alongside an industrial-grade ORM and robust authentication.",
        "<b>SQLite Relational Database Engine:</b> Used as the transactional datastore during prototyping and cloud demonstration. SQLite is embedded directly within Python, requires zero daemon overhead, supports full ACID transactions, and provides seamless migration to PostgreSQL via Django ORM.",
        "<b>Bootstrap 5.3.0 & Mobile Grid:</b> Eliminates fragile custom CSS by utilizing an industry-standard, mobile-first responsive grid that scales effortlessly from smartphone viewports to desktop command centers.",
        "<b>Asynchronous Client Extensions:</b> Employs Vanilla JavaScript ES6 and AJAX for background data fetching, Select2 for substring search indexing, JsBarcode for client-side CODE128 vector generation, and Chart.js for hardware-accelerated charts."
    ]
    for tp in tech_points:
        story.append(Paragraph(f"• {tp}", style_bullet))
    story.append(Spacer(1, 6))

    story.append(Paragraph("2.2 Operational Feasibility Analysis", style_sec_title))
    story.append(Paragraph(
        "Operational feasibility measures how comfortably end-users can operate the software within their daily workplace context. "
        "The software addresses operational feasibility through a single-screen POS terminal, hardware barcode gun auto-trapping, "
        "and intuitive visual traffic-light alerts for expiring batches.",
        style_body
    ))

    story.append(Paragraph("2.3 Economic Feasibility & ROI Analysis", style_sec_title))
    story.append(Paragraph(
        "Economic feasibility examines the cost-benefit balance of development and ongoing maintenance. "
        "The Pharmacy ERP utilizes an entirely open-source software stack, completely eliminating recurring proprietary licensing fees. "
        "The return on investment (ROI) is immediately realized through: (1) Elimination of expired medicine write-offs via FEFO; "
        "(2) Prevention of cashier tax miscalculations; and (3) Labor savings achieved by automated one-click purchase order generation.",
        style_body
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("2.4 Hardware Requirements", style_sec_title))
    hw_data = [
        [Paragraph("<b>Hardware Component</b>", style_th), Paragraph("<b>Minimum Specification (Client)</b>", style_th), Paragraph("<b>Recommended Specification (Server/Host)</b>", style_th)],
        [Paragraph("Processor", style_td), Paragraph("Intel Celeron / Core i3 Dual-Core (2.0 GHz)", style_td), Paragraph("Intel Core i5 / AMD Ryzen 5 Quad-Core (3.0 GHz+)", style_td)],
        [Paragraph("System Memory (RAM)", style_td), Paragraph("4 GB DDR4", style_td), Paragraph("8 GB / 16 GB DDR4", style_td)],
        [Paragraph("Hard Disk Storage", style_td), Paragraph("128 GB SSD / HDD", style_td), Paragraph("256 GB NVMe SSD", style_td)],
        [Paragraph("Display Resolution", style_td), Paragraph("1024 x 768 (XGA)", style_td), Paragraph("1920 x 1080 (Full HD, 100% Scale)", style_td)],
        [Paragraph("Peripherals", style_td), Paragraph("Standard Keyboard & Mouse, USB Barcode Gun", style_td), Paragraph("58mm/80mm Thermal Receipt Printer, Barcode Gun", style_td)],
        [Paragraph("Network Connectivity", style_td), Paragraph("1 Mbps Broadband / Mobile Hotspot", style_td), Paragraph("10 Mbps+ Stable Fiber / Cloud Server Connection", style_td)]
    ]
    t_hw = Table(hw_data, colWidths=[PRINTABLE_WIDTH*0.25, PRINTABLE_WIDTH*0.375, PRINTABLE_WIDTH*0.375])
    t_hw.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_DARK_TEAL),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, C_LIGHT_BG])
    ]))
    story.append(t_hw)
    story.append(Paragraph("<b>Table 2.1:</b> Hardware Specifications for Client Terminals and Host Deployment", style_caption))
    story.append(Spacer(1, 6))

    story.append(Paragraph("2.5 Software Technology Stack", style_sec_title))
    sw_data = [
        [Paragraph("<b>Architectural Layer</b>", style_th), Paragraph("<b>Chosen Technology</b>", style_th), Paragraph("<b>Version / Specification</b>", style_th), Paragraph("<b>Operational Role</b>", style_th)],
        [Paragraph("Programming Language", style_td), Paragraph("Python", style_td), Paragraph("3.14 (Local) / 3.13 (Cloud)", style_td), Paragraph("Core runtime and business logic", style_td)],
        [Paragraph("Backend Framework", style_td), Paragraph("Django", style_td), Paragraph("6.0.4", style_td), Paragraph("MVT server, routing, ORM, CSRF, auth", style_td)],
        [Paragraph("Database Engine", style_td), Paragraph("SQLite (Postgres-Ready)", style_td), Paragraph("3.4x Relational", style_td), Paragraph("Transactional and master data persistence", style_td)],
        [Paragraph("Frontend Presentation", style_td), Paragraph("HTML5 & CSS3", style_td), Paragraph("W3C Compliant", style_td), Paragraph("Semantic page structure & styling", style_td)],
        [Paragraph("UI Responsive Grid", style_td), Paragraph("Bootstrap", style_td), Paragraph("5.3.0", style_td), Paragraph("Mobile-first layout and responsive utilities", style_td)],
        [Paragraph("Client Scripting", style_td), Paragraph("Vanilla JavaScript", style_td), Paragraph("ECMAScript 2022 (ES6)", style_td), Paragraph("DOM manipulation, key traps, AJAX calls", style_td)],
        [Paragraph("Search Engine", style_td), Paragraph("Select2 jQuery Plugin", style_td), Paragraph("4.1.0-rc.0", style_td), Paragraph("Instant substring medicine filtering", style_td)],
        [Paragraph("Barcode Renderer", style_td), Paragraph("JsBarcode", style_td), Paragraph("3.11.5", style_td), Paragraph("Client-side CODE128 vector barcode generation", style_td)],
        [Paragraph("Business Intelligence", style_td), Paragraph("Chart.js", style_td), Paragraph("4.x CDN", style_td), Paragraph("HTML5 canvas bar and doughnut charts", style_td)],
        [Paragraph("Environment Vault", style_td), Paragraph("python-dotenv", style_td), Paragraph("1.2.2+", style_td), Paragraph("Cryptographic isolation of SECRET_KEY", style_td)],
        [Paragraph("Cloud Hosting PaaS", style_td), Paragraph("PythonAnywhere", style_td), Paragraph("Linux WSGI Server", style_td), Paragraph("Public production serving across the web", style_td)]
    ]
    t_sw = Table(sw_data, colWidths=[PRINTABLE_WIDTH*0.22, PRINTABLE_WIDTH*0.24, PRINTABLE_WIDTH*0.22, PRINTABLE_WIDTH*0.32])
    t_sw.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_DARK_TEAL),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, C_LIGHT_BG])
    ]))
    story.append(t_sw)
    story.append(Paragraph("<b>Table 2.2:</b> Comprehensive Software Technology Stack Matrix", style_caption))
    story.append(PageBreak())

    # ==================================================================
    # CHAPTER 3: SYSTEM ANALYSIS & ENGINEERING METHODOLOGY
    # ==================================================================
    story.append(Paragraph("CHAPTER 3", style_chap_num))
    story.append(Paragraph("SYSTEM ANALYSIS & ENGINEERING METHODOLOGY", style_chap_title))
    story.append(HRFlowable(width="100%", thickness=1.5, color=C_TEAL, spaceBefore=2, spaceAfter=10))

    story.append(Paragraph("3.1 Requirement Engineering & Feature Categorization", style_sec_title))
    story.append(Paragraph(
        "Requirements engineering was executed by analyzing real-world pharmacy counter interactions, wholesale supplier delivery "
        "consignments, and retail billing laws in India. System features were prioritized into Essential Core (Auth, RBAC, Batch Inventory, "
        "FEFO Engine, POS Billing, GST Reverse Engine) and Supplementary Value-Adds (Smart CRM, Visual Alerts, One-Click PO Export, Signals).",
        style_body
    ))

    story.append(Paragraph("3.2 Software Development Lifecycle (Waterfall Model)", style_sec_title))
    story.append(Paragraph(
        "The project was engineered using the structured <b>Classic Waterfall Development Lifecycle</b> with iterative verification loops. "
        "Because pharmaceutical applications handle legally binding financial transactions and health-critical drug expiries, a sequential "
        "model ensures thorough architectural clarity before code execution.",
        style_body
    ))
    
    wf_steps = [
        "<b>Phase 1 — Requirement Analysis & Elicitation:</b> Domain analysis of retail pharmacy pain points, HSN tax brackets, and user role specifications.",
        "<b>Phase 2 — System Architecture & Database Design:</b> Formalization of Data Flow Diagrams (DFDs), Entity-Relationship (ER) schemas, and relational integrity constraints.",
        "<b>Phase 3 — Technical Implementation:</b> Coding of Django models, algorithmic views (FEFO, reverse GST), AJAX API endpoints, and responsive HTML5/Bootstrap templates.",
        "<b>Phase 4 — System Testing & Verification:</b> Unit testing of mathematical algorithms, integration testing of inventory signals, and cross-device browser validation.",
        "<b>Phase 5 — Production Deployment:</b> Cloud hosting on PythonAnywhere, WSGI server configuration, environment variable isolation, and static collection."
    ]
    for wfs in wf_steps:
        story.append(Paragraph(f"• {wfs}", style_bullet))
    story.append(Spacer(1, 6))

    story.append(Paragraph("3.3 Three-Tier Modular Architecture", style_sec_title))
    story.append(Paragraph(
        "To guarantee high maintainability and clean Separation of Concerns (SoC), the software adopts an enterprise <b>Three-Tier Modular Architecture</b>:<br/>"
        "• <b>Presentation Layer (Frontend Client):</b> Rendered via HTML5, CSS3, JavaScript ES6, and Bootstrap 5.3. Handles barcode scanner keypress traps, live cart previews, and Chart.js graphs.<br/>"
        "• <b>Application Logic Layer (Django Controller):</b> The core Python engine (store/views.py) executing business rules, user authentication, role-based clearance checks, FEFO batch sorting, reverse tax computations, and JSON responses.<br/>"
        "• <b>Data Persistence Layer (Relational Storage):</b> Managed by SQLite through Django ORM. Stores master records (Medicines, Suppliers, Customers) and transactional ledgers (Stock, Sales, Returns) while enforcing foreign key cascades.",
        style_body
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("3.4 Working Model & Billing Workflow Loop", style_sec_title))
    story.append(Paragraph(
        "The typical transactional lifecycle within the Pharmacy ERP follows a synchronized 7-stage workflow loop: "
        "(1) Cashier scans/selects medicine; (2) Django queries active batches; (3) FEFO engine sorts batches by expiry date ASC; "
        "(4) Reverse GST calculates base price and CGST/SGST splits; (5) Customer phone lookup auto-fills patient profile; "
        "(6) Sale is committed and stock deducted; and (7) Thermal receipt is printed with scannable CODE128 barcode.",
        style_body
    ))
    story.append(PageBreak())

    # ==================================================================
    # CHAPTER 4: SYSTEM DESIGN & VISUAL MODELING
    # ==================================================================
    story.append(Paragraph("CHAPTER 4", style_chap_num))
    story.append(Paragraph("SYSTEM DESIGN & VISUAL MODELING", style_chap_title))
    story.append(HRFlowable(width="100%", thickness=1.5, color=C_TEAL, spaceBefore=2, spaceAfter=10))

    story.append(Paragraph("4.1 Functional Module Breakdown", style_sec_title))
    story.append(Paragraph(
        "The system is decomposed into seven cohesive functional modules designed for high interoperability and minimal coupling: "
        "<b>(1) Auth & RBAC</b>; <b>(2) Medicine Catalog</b>; <b>(3) Batch Inventory Vault</b>; <b>(4) POS Billing Counter</b>; "
        "<b>(5) Smart CRM & Patient Memory</b>; <b>(6) Reverse Logistics Desk</b>; and <b>(7) BI Command Center</b>.",
        style_body
    ))
    story.append(Spacer(1, 4))

    # Level 0 DFD
    story.append(Paragraph("4.2 Data Flow Modeling: Level 0 Context DFD", style_sec_title))
    story.append(Paragraph(
        "The <b>Level 0 Data Flow Diagram (Context Diagram)</b> defines the external boundary of the Pharmacy Management System, "
        "visualizing the four external entities: Customers/Patients, Cashiers/Pharmacists, Wholesalers, and Administrators.",
        style_body
    ))
    story.append(Spacer(1, 4))
    story.append(make_figure_block("dfd_level_0.png", "<b>Figure 4.1:</b> Level 0 Context Data Flow Diagram (DFD) for Pharmacy Management ERP", target_width=PRINTABLE_WIDTH, max_height=240))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "• <b>Customer / Patient:</b> Provides prescriptions, phone number, and payment tender; receives thermal invoices and return refunds.<br/>"
        "• <b>Pharmacist / Cashier:</b> Scans barcodes, manages cart, performs CRM lookups, and prints thermal receipts.<br/>"
        "• <b>Medicine Supplier / Wholesaler:</b> Supplies consignments with batch metadata; receives automated reorder PO CSVs.<br/>"
        "• <b>Administrator / Store Owner:</b> Manages roles, catalogs, audits stock, and inspects profit analytics.",
        style_body
    ))
    story.append(PageBreak())

    # Level 1 DFD
    story.append(Paragraph("4.3 Data Flow Modeling: Level 1 Decomposition DFD", style_sec_title))
    story.append(Paragraph(
        "The <b>Level 1 Data Flow Diagram</b> decomposes the system into seven operational processes and seven relational datastores (D1 to D7):",
        style_body
    ))
    story.append(Spacer(1, 4))
    story.append(make_figure_block("dfd_level_1.png", "<b>Figure 4.2:</b> Level 1 Functional Decomposition DFD (Gane & Sarson Notation)", target_width=PRINTABLE_WIDTH, max_height=250))
    story.append(Spacer(1, 4))

    p_data = [
        [Paragraph("<b>Process ID & Name</b>", style_th), Paragraph("<b>Input Streams</b>", style_th), Paragraph("<b>Target Datastores</b>", style_th), Paragraph("<b>Output Deliverables</b>", style_th)],
        [Paragraph("1.0 Auth & RBAC", style_td), Paragraph("Staff credentials", style_td), Paragraph("D1 Users & Roles", style_td), Paragraph("Session tokens & clearance", style_td)],
        [Paragraph("2.0 POS Billing & GST", style_td), Paragraph("Barcode, Qty, Phone", style_td), Paragraph("D2 Catalog, D3 Stock, D4 Sales", style_td), Paragraph("Tax invoice & stock deduction", style_td)],
        [Paragraph("3.0 Batch Inventory (FEFO)", style_td), Paragraph("Consignments, PO items", style_td), Paragraph("D2 Catalog, D3 Stock", style_td), Paragraph("Sorted batch availability", style_td)],
        [Paragraph("4.0 Smart CRM", style_td), Paragraph("10-digit mobile number", style_td), Paragraph("D5 Customer Records", style_td), Paragraph("AJAX autofill name & doctor", style_td)],
        [Paragraph("5.0 Reverse Logistics", style_td), Paragraph("Bill barcode, return qty", style_td), Paragraph("D4 Sales, D6 ReturnSale, D3 Stock", style_td), Paragraph("Refund slip & restock credit", style_td)],
        [Paragraph("6.0 Procurement Engine", style_td), Paragraph("Stock levels vs thresholds", style_td), Paragraph("D2 Catalog, D3 Stock, D7 Supplier", style_td), Paragraph("Downloadable PO CSV", style_td)],
        [Paragraph("7.0 Financial BI Analytics", style_td), Paragraph("Date range parameters", style_td), Paragraph("D4 Sales Ledger, D3 Stock", style_td), Paragraph("Chart.js visual KPI graphs", style_td)]
    ]
    t_dfd = Table(p_data, colWidths=[PRINTABLE_WIDTH*0.25, PRINTABLE_WIDTH*0.22, PRINTABLE_WIDTH*0.25, PRINTABLE_WIDTH*0.28])
    t_dfd.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_DARK_TEAL),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, C_LIGHT_BG])
    ]))
    story.append(t_dfd)
    story.append(Paragraph("<b>Table 4.1:</b> Mapping of Level 1 Processes, Data Inputs, and Relational Datastores", style_caption))
    story.append(PageBreak())

    # ER Diagram
    story.append(Paragraph("4.4 Database Schema & Entity Relationship (ER) Diagram", style_sec_title))
    story.append(Paragraph(
        "The relational database schema is structured to mirror real-world pharmacy operations, strictly bifurcating "
        "Master Entities (permanent catalogs) from Transactional Entities (dynamic events). Primary-to-foreign key bridges "
        "maintain complete referential integrity across the data lifecycle.",
        style_body
    ))
    story.append(Spacer(1, 4))
    story.append(make_figure_block("er_diagram.png", "<b>Figure 4.3:</b> Complete Entity-Relationship (ER) Schema for the Pharmacy Management System", target_width=PRINTABLE_WIDTH, max_height=260))
    story.append(Spacer(1, 4))

    story.append(Paragraph("4.5 Data Dictionary & Relational Tables Specification", style_sec_title))
    story.append(Paragraph(
        "Below are the detailed technical specifications of the core tables implemented in <code>store/models.py</code>:",
        style_body
    ))

    # Medicine & Stock Tables
    story.append(Paragraph("<b>Table 4.2: Medicine (Master Drug Catalog)</b>", style_subsec_title))
    med_schema = [
        [Paragraph("<b>Field Name</b>", style_th), Paragraph("<b>Data Type</b>", style_th), Paragraph("<b>Constraints</b>", style_th), Paragraph("<b>Description</b>", style_th)],
        [Paragraph("id", style_td), Paragraph("AutoField", style_td), Paragraph("PRIMARY KEY", style_td), Paragraph("Unique internal system medicine identifier", style_td)],
        [Paragraph("name", style_td), Paragraph("CharField(100)", style_td), Paragraph("NOT NULL", style_td), Paragraph("Brand/Trade name of medicine (e.g. Dolo 650)", style_td)],
        [Paragraph("category", style_td), Paragraph("CharField(100)", style_td), Paragraph("NOT NULL", style_td), Paragraph("Formulation type (Tablet, Capsule, Syrup, Injection)", style_td)],
        [Paragraph("manufacturer", style_td), Paragraph("CharField(200)", style_td), Paragraph("NULL, BLANK", style_td), Paragraph("Pharmaceutical manufacturing company name", style_td)],
        [Paragraph("minimum_stock_level", style_td), Paragraph("IntegerField", style_td), Paragraph("DEFAULT=10", style_td), Paragraph("Threshold below which reorder alerts trigger", style_td)],
        [Paragraph("gst_percentage", style_td), Paragraph("IntegerField", style_td), Paragraph("DEFAULT=12", style_td), Paragraph("Mandated Indian GST slab (0%, 5%, 12%, 18%)", style_td)],
        [Paragraph("barcode", style_td), Paragraph("CharField(100)", style_td), Paragraph("UNIQUE, NULL", style_td), Paragraph("EAN/UPC barcode number for hardware scanning", style_td)],
        [Paragraph("pack_size", style_td), Paragraph("CharField(50)", style_td), Paragraph("DEFAULT='10 Tabs'", style_td), Paragraph("Packaging specification (e.g. 15 Tabs, 100ml)", style_td)]
    ]
    t_med = Table(med_schema, colWidths=[PRINTABLE_WIDTH*0.22, PRINTABLE_WIDTH*0.18, PRINTABLE_WIDTH*0.22, PRINTABLE_WIDTH*0.38])
    t_med.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_DARK_TEAL),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, C_LIGHT_BG])
    ]))
    story.append(t_med)
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Table 4.3: Stock (Batch-Level Inventory Vault)</b>", style_subsec_title))
    stock_schema = [
        [Paragraph("<b>Field Name</b>", style_th), Paragraph("<b>Data Type</b>", style_th), Paragraph("<b>Constraints</b>", style_th), Paragraph("<b>Description</b>", style_th)],
        [Paragraph("id", style_td), Paragraph("AutoField", style_td), Paragraph("PRIMARY KEY", style_td), Paragraph("Unique stock consignment identifier", style_td)],
        [Paragraph("medicine", style_td), Paragraph("ForeignKey(Medicine)", style_td), Paragraph("CASCADE", style_td), Paragraph("Relational link to master drug catalog", style_td)],
        [Paragraph("supplier", style_td), Paragraph("ForeignKey(Supplier)", style_td), Paragraph("SET_NULL, NULL", style_td), Paragraph("Relational link to wholesale distributor", style_td)],
        [Paragraph("batch_no", style_td), Paragraph("CharField(50)", style_td), Paragraph("NOT NULL", style_td), Paragraph("Manufacturer batch consignment code", style_td)],
        [Paragraph("expiry_date", style_td), Paragraph("DateField", style_td), Paragraph("NOT NULL", style_td), Paragraph("Batch expiration date (governs FEFO sorting)", style_td)],
        [Paragraph("purchase_price", style_td), Paragraph("DecimalField(10,2)", style_td), Paragraph("DEFAULT=0.0", style_td), Paragraph("Wholesale acquisition cost per pack", style_td)],
        [Paragraph("mrp", style_td), Paragraph("DecimalField(10,2)", style_td), Paragraph("DEFAULT=0.0", style_td), Paragraph("Maximum Retail Price inclusive of GST", style_td)],
        [Paragraph("quantity", style_td), Paragraph("IntegerField", style_td), Paragraph("NOT NULL", style_td), Paragraph("Currently available sellable physical units", style_td)],
        [Paragraph("date_added", style_td), Paragraph("DateTimeField", style_td), Paragraph("auto_now_add=True", style_td), Paragraph("Timestamp of warehouse consignment receipt", style_td)]
    ]
    t_stk = Table(stock_schema, colWidths=[PRINTABLE_WIDTH*0.22, PRINTABLE_WIDTH*0.22, PRINTABLE_WIDTH*0.2, PRINTABLE_WIDTH*0.36])
    t_stk.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_DARK_TEAL),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, C_LIGHT_BG])
    ]))
    story.append(t_stk)
    story.append(PageBreak())

    # Customer and Sale Tables
    story.append(Paragraph("<b>Table 4.4: Customer (Smart CRM Directory)</b>", style_subsec_title))
    cust_schema = [
        [Paragraph("<b>Field Name</b>", style_th), Paragraph("<b>Data Type</b>", style_th), Paragraph("<b>Constraints</b>", style_th), Paragraph("<b>Description</b>", style_th)],
        [Paragraph("id", style_td), Paragraph("AutoField", style_td), Paragraph("PRIMARY KEY", style_td), Paragraph("Unique patient profile identifier", style_td)],
        [Paragraph("name", style_td), Paragraph("CharField(200)", style_td), Paragraph("NOT NULL", style_td), Paragraph("Full legal name of patient", style_td)],
        [Paragraph("phone", style_td), Paragraph("CharField(15)", style_td), Paragraph("UNIQUE, NOT NULL", style_td), Paragraph("10-digit primary contact phone (Indexed for AJAX)", style_td)],
        [Paragraph("last_doctor", style_td), Paragraph("CharField(200)", style_td), Paragraph("NULL, BLANK", style_td), Paragraph("Attending physician / prescribing doctor name", style_td)]
    ]
    t_cust = Table(cust_schema, colWidths=[PRINTABLE_WIDTH*0.22, PRINTABLE_WIDTH*0.2, PRINTABLE_WIDTH*0.22, PRINTABLE_WIDTH*0.36])
    t_cust.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_DARK_TEAL),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, C_LIGHT_BG])
    ]))
    story.append(t_cust)
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Table 4.5: Sale (Transactional POS Ledger)</b>", style_subsec_title))
    sale_schema = [
        [Paragraph("<b>Field Name</b>", style_th), Paragraph("<b>Data Type</b>", style_th), Paragraph("<b>Constraints</b>", style_th), Paragraph("<b>Description</b>", style_th)],
        [Paragraph("id", style_td), Paragraph("AutoField", style_td), Paragraph("PRIMARY KEY", style_td), Paragraph("Unique transactional line-item ID", style_td)],
        [Paragraph("bill_no", style_td), Paragraph("CharField(20)", style_td), Paragraph("NOT NULL, INDEXED", style_td), Paragraph("Human-readable alphanumeric bill number (e.g. 15489WS6630)", style_td)],
        [Paragraph("stock", style_td), Paragraph("ForeignKey(Stock)", style_td), Paragraph("CASCADE", style_td), Paragraph("Exact batch from which units were deducted", style_td)],
        [Paragraph("quantity", style_td), Paragraph("IntegerField", style_td), Paragraph("NOT NULL", style_td), Paragraph("Number of packs sold in this transaction", style_td)],
        [Paragraph("total_price", style_td), Paragraph("DecimalField(10,2)", style_td), Paragraph("NOT NULL", style_td), Paragraph("Gross billed amount inclusive of GST", style_td)],
        [Paragraph("customer", style_td), Paragraph("ForeignKey(Customer)", style_td), Paragraph("NULL, SET_NULL", style_td), Paragraph("Associated patient profile (Foreign Key bridge)", style_td)],
        [Paragraph("payment_method", style_td), Paragraph("CharField(20)", style_td), Paragraph("DEFAULT='Cash'", style_td), Paragraph("Tender type (Cash vs UPI / QR Code)", style_td)],
        [Paragraph("date", style_td), Paragraph("DateTimeField", style_td), Paragraph("auto_now_add=True", style_td), Paragraph("Exact timestamp of transaction completion", style_td)]
    ]
    t_sale = Table(sale_schema, colWidths=[PRINTABLE_WIDTH*0.22, PRINTABLE_WIDTH*0.22, PRINTABLE_WIDTH*0.2, PRINTABLE_WIDTH*0.36])
    t_sale.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_DARK_TEAL),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, C_LIGHT_BG])
    ]))
    story.append(t_sale)
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Table 4.6: ReturnSale (Reverse Logistics Audit Trail)</b>", style_subsec_title))
    ret_schema = [
        [Paragraph("<b>Field Name</b>", style_th), Paragraph("<b>Data Type</b>", style_th), Paragraph("<b>Constraints</b>", style_th), Paragraph("<b>Description</b>", style_th)],
        [Paragraph("id", style_td), Paragraph("AutoField", style_td), Paragraph("PRIMARY KEY", style_td), Paragraph("Unique refund audit identifier", style_td)],
        [Paragraph("sale", style_td), Paragraph("ForeignKey(Sale)", style_td), Paragraph("CASCADE", style_td), Paragraph("Original line-item transaction reference", style_td)],
        [Paragraph("stock", style_td), Paragraph("ForeignKey(Stock)", style_td), Paragraph("CASCADE", style_td), Paragraph("Batch associated with the returned product", style_td)],
        [Paragraph("quantity_returned", style_td), Paragraph("IntegerField", style_td), Paragraph("NOT NULL", style_td), Paragraph("Number of returned units", style_td)],
        [Paragraph("refund_amount", style_td), Paragraph("DecimalField(10,2)", style_td), Paragraph("NOT NULL", style_td), Paragraph("Monetary cash/credit refunded to patient", style_td)],
        [Paragraph("reason", style_td), Paragraph("CharField(50)", style_td), Paragraph("NOT NULL", style_td), Paragraph("WRONG_ITEM, DEFECTIVE, or EXCESS", style_td)],
        [Paragraph("restocked", style_td), Paragraph("BooleanField", style_td), Paragraph("DEFAULT=True", style_td), Paragraph("Flags if physical stock was returned to shelf", style_td)],
        [Paragraph("date_returned", style_td), Paragraph("DateTimeField", style_td), Paragraph("auto_now_add=True", style_td), Paragraph("Timestamp when return was processed", style_td)]
    ]
    t_ret = Table(ret_schema, colWidths=[PRINTABLE_WIDTH*0.22, PRINTABLE_WIDTH*0.22, PRINTABLE_WIDTH*0.2, PRINTABLE_WIDTH*0.36])
    t_ret.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_DARK_TEAL),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, C_LIGHT_BG])
    ]))
    story.append(t_ret)
    story.append(PageBreak())

    # ==================================================================
    # CHAPTER 5: TECHNICAL IMPLEMENTATION & CORE ALGORITHMS
    # ==================================================================
    story.append(Paragraph("CHAPTER 5", style_chap_num))
    story.append(Paragraph("TECHNICAL IMPLEMENTATION & CORE ALGORITHMS", style_chap_title))
    story.append(HRFlowable(width="100%", thickness=1.5, color=C_TEAL, spaceBefore=2, spaceAfter=10))

    story.append(Paragraph("5.1 Django Backend Engine & MVT Architecture", style_sec_title))
    story.append(Paragraph(
        "The application leverages the <b>Model-View-Template (MVT)</b> architectural pattern. In Django's MVT, the "
        "<b>Model</b> encapsulates database entities and integrity constraints; the <b>View</b> serves as the algorithmic "
        "controller processing business logic, security permissions, and HTTP transactions; and the <b>Template</b> forms "
        "the presentation layer. The default Django admin entrance was obfuscated to a secure vault route to thwart bot scans.",
        style_body
    ))

    story.append(Paragraph("5.2 Algorithmic FEFO (First-Expire-First-Out) Engine", style_sec_title))
    story.append(Paragraph(
        "In pharmaceutical retail, traditional FIFO (First-In, First-Out) inventory is dangerously inadequate. A distributor may deliver "
        "a batch of amoxicillin manufactured 6 months ago alongside a freshly manufactured consignment. Selling by delivery sequence risks "
        "letting older batches decay. To prevent expired inventory losses, a custom <b>FEFO (First-Expire-First-Out)</b> algorithm was "
        "engineered directly into the checkout pipeline.",
        style_body
    ))
    story.append(Paragraph(
        "<b>Mathematical Formulation & Spill-Over Mechanics:</b><br/>"
        "Let a requested drug purchase have quantity <b>Q<sub>req</sub></b>. The system queries all active batches for medicine <b>M</b> where "
        "quantity <b>q<sub>i</sub> &gt; 0</b> and sorts them chronologically: <b>B = {b<sub>1</sub>, b<sub>2</sub>, ..., b<sub>n</sub>}</b> such that "
        "<b>Expiry(b<sub>1</sub>) &le; Expiry(b<sub>2</sub>) &le; ... &le; Expiry(b<sub>n</sub>)</b>.<br/>"
        "For each batch <b>b<sub>i</sub></b>:<br/>"
        "• If <b>q<sub>i</sub> &ge; Q<sub>req</sub></b>, the algorithm deducts <b>q<sub>i</sub> &larr; q<sub>i</sub> - Q<sub>req</sub></b> and terminates.<br/>"
        "• If <b>q<sub>i</sub> &lt; Q<sub>req</sub></b>, the algorithm completely exhausts batch <b>b<sub>i</sub></b> (<b>q<sub>i</sub> &larr; 0</b>), decrements "
        "the remaining demand <b>Q<sub>req</sub> &larr; Q<sub>req</sub> - q<sub>i</sub></b>, and seamlessly 'spills over' into batch <b>b<sub>i+1</sub></b>.",
        style_body
    ))
    
    code_fefo = (
        "# ------------------------------------------------------------\n"
        "# ALGORITHMIC FEFO INVENTORY DISPATCHER (store/views.py)\n"
        "# ------------------------------------------------------------\n"
        "batches = Stock.objects.filter(\n"
        "    medicine_id=item['id'], \n"
        "    quantity__gt=0\n"
        ").order_by('expiry_date')  # Chronological FEFO sorting\n"
        "\n"
        "remaining_qty = item['qty']\n"
        "for batch in batches:\n"
        "    if batch.quantity >= remaining_qty:\n"
        "        batch.quantity -= remaining_qty\n"
        "        batch.save()\n"
        "        Sale.objects.create(\n"
        "            bill_no=bill_no, stock=batch, quantity=remaining_qty,\n"
        "            total_price=item['price'] * remaining_qty, customer=customer_obj,\n"
        "            payment_method=payment_method\n"
        "        )\n"
        "        remaining_qty = 0\n"
        "        break\n"
        "    else:\n"
        "        # Spill-Over: Exhaust current batch and continue to next\n"
        "        deduct = batch.quantity\n"
        "        remaining_qty -= deduct\n"
        "        batch.quantity = 0\n"
        "        batch.save()\n"
        "        Sale.objects.create(\n"
        "            bill_no=bill_no, stock=batch, quantity=deduct,\n"
        "            total_price=item['price'] * deduct, customer=customer_obj,\n"
        "            payment_method=payment_method\n"
        "        )"
    )
    story.append(make_code_card(code_fefo, "store/views.py — FEFO Implementation"))
    story.append(PageBreak())

    # Reverse GST & Signals
    story.append(Paragraph("5.3 Dynamic Reverse GST Calculation Engine", style_sec_title))
    story.append(Paragraph(
        "Under Indian commercial tax statutes (Central Goods and Services Tax Act), pharmaceutical Maximum Retail Prices (MRPs) "
        "printed on packaging are legally inclusive of all applicable taxes. The system implements a dynamic <b>Reverse GST Engine</b>:<br/>"
        "<font face='Helvetica-Bold' color='#005f5f'>Base Taxable Value = MRP ÷ (1 + (GST% / 100))</font><br/>"
        "<font face='Helvetica-Bold' color='#005f5f'>Total Tax Component = MRP - Base Taxable Value</font><br/>"
        "<font face='Helvetica-Bold' color='#005f5f'>CGST (Central Tax) = Total Tax / 2, &nbsp;&nbsp; SGST (State Tax) = Total Tax / 2</font><br/>"
        "Because each medicine carries its own configured <code>gst_percentage</code> (0%, 5%, 12%, 18%), the system computes tax splits "
        "on a line-item basis, aggregating a formal tax breakdown table on the thermal receipt.",
        style_body
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("5.4 Event-Driven Inventory Synchronization via Django Signals", style_sec_title))
    story.append(Paragraph(
        "To safeguard the digital ledger against manual admin deletions, an event-driven <code>post_delete</code> signal was implemented "
        "that automatically restores deducted quantities back to the physical batch consignment:",
        style_body
    ))
    code_signal = (
        "# ------------------------------------------------------------\n"
        "# EVENT-DRIVEN INVENTORY RESTORATION SIGNAL (store/views.py)\n"
        "# ------------------------------------------------------------\n"
        "from django.db.models.signals import post_delete\n"
        "from django.dispatch import receiver\n"
        "\n"
        "@receiver(post_delete, sender=Sale)\n"
        "def restore_stock_on_sale_delete(sender, instance, **kwargs):\n"
        "    \"\"\"\n"
        "    Failsafe: Automatically restores deducted stock units back to\n"
        "    the physical batch if a sale record is purged or voided.\n"
        "    \"\"\"\n"
        "    stock = instance.stock\n"
        "    stock.quantity += instance.quantity\n"
        "    stock.save()"
    )
    story.append(make_code_card(code_signal, "store/views.py — Signal Failsafe"))
    story.append(Spacer(1, 6))

    story.append(Paragraph("5.5 Asynchronous Client-Server Bridge (AJAX)", style_sec_title))
    story.append(Paragraph(
        "The system employs asynchronous JSON bridges across two critical workflows:<br/>"
        "• <b>Real-Time Patient Recognition:</b> As the cashier types a 10-digit mobile number, a keyup event dispatches a background request to "
        "<code>/api/get_customer/?phone=...</code>. If matched, patient name and attending physician auto-populate instantly, with the input box turning green.<br/>"
        "• <b>Non-Blocking Master Data Injection:</b> When receiving a new drug consignment, clicking '+' opens a modal that sends an AJAX POST payload to "
        "<code>/ajax-add-medicine/</code>. The backend saves the record and injects the new Option directly into the active Select2 dropdown without refreshing.",
        style_body
    ))
    story.append(PageBreak())

    # Barcode & Mobile Overhaul
    story.append(Paragraph("5.6 Hardware Barcode Integration & Dynamic CODE128 Rendering", style_sec_title))
    story.append(Paragraph(
        "The POS terminal natively interfaces with standard USB/Bluetooth hardware barcode guns by maintaining autofocus on the scan input. "
        "Upon transaction finalization, the system invokes <code>JsBarcode</code> to render a retail-grade <b>CODE128</b> barcode vector on the receipt. "
        "This barcode encodes the unique Bill Number (e.g., <code>15489WS6630</code>), allowing the Reverse Logistics desk to retrieve the entire bill "
        "with a single click of the scanner gun.",
        style_body
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("5.7 Mobile-Responsive Multi-Device UI/UX Overhaul", style_sec_title))
    story.append(Paragraph(
        "Recognizing that pharmacy managers frequently monitor store metrics from personal smartphones, every single template was refactored "
        "with mobile-first ergonomics: (1) Replaced rigid <code>100vh</code> on the login page with <code>min-height: 100vh</code> to prevent virtual keyboard cutoff; "
        "(2) Formatted POS Add-Item rows so Qty and Add buttons sit side-by-side on mobile screens; (3) Added horizontal scroll wrapping (<code>table-responsive</code> "
        "and <code>white-space: nowrap</code>) across all tables to prevent word breaks; and (4) Ensured all action buttons expand to full touch targets.",
        style_body
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("5.8 Core Python Source Code Implementations", style_sec_title))
    code_models = (
        "# ------------------------------------------------------------\n"
        "# CORE DATA MODELS DEFINITION (store/models.py)\n"
        "# ------------------------------------------------------------\n"
        "class Medicine(models.Model):\n"
        "    name = models.CharField(max_length=100)\n"
        "    category = models.CharField(max_length=100)\n"
        "    minimum_stock_level = models.IntegerField(default=10)\n"
        "    gst_percentage = models.IntegerField(default=12)\n"
        "    barcode = models.CharField(max_length=100, unique=True, null=True, blank=True)\n"
        "    pack_size = models.CharField(max_length=50, default=\"10 Tabs\")\n"
        "\n"
        "class Stock(models.Model):\n"
        "    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)\n"
        "    batch_no = models.CharField(max_length=50)\n"
        "    expiry_date = models.DateField()\n"
        "    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)\n"
        "    mrp = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)\n"
        "    quantity = models.IntegerField()"
    )
    story.append(make_code_card(code_models, "store/models.py — Data Schema"))
    story.append(PageBreak())

    # Visual Snapshots Section
    story.append(Paragraph("5.9 User Interface Snapshots & Operational Walkthrough", style_sec_title))
    story.append(Paragraph(
        "The following screenshots illustrate the functional screens of the running Pharmacy Management ERP platform:",
        style_body
    ))
    story.append(Spacer(1, 4))

    # POS Terminal Screenshot
    story.append(make_figure_block("ui_pos_home.png", "<b>Figure 5.1:</b> High-Speed POS Counter Terminal with Select2 Search, Barcode Input, and Terminal Navigation", target_width=PRINTABLE_WIDTH, max_height=200))
    story.append(Spacer(1, 6))

    # Login Screenshot
    story.append(make_figure_block("ui_login.png", "<b>Figure 5.2:</b> Secure 256-Bit Encrypted Authentication Portal with Mobile Brand Banner", target_width=PRINTABLE_WIDTH*0.85, max_height=170))
    story.append(PageBreak())

    # Current Cart & Inventory Dashboard
    story.append(make_figure_block("ui_cart_items.png", "<b>Figure 5.3:</b> Interactive Live Cart Preview with Pack Sizes, Dynamic MRPs, and Inline Item Deletion", target_width=PRINTABLE_WIDTH*0.85, max_height=170))
    story.append(Spacer(1, 6))

    story.append(make_figure_block("ui_inventory_dashboard.png", "<b>Figure 5.4:</b> Inventory Command Center featuring Traffic-Light Alerts, Batch Tracking, and Reorder PO Export", target_width=PRINTABLE_WIDTH, max_height=185))
    story.append(PageBreak())

    # Returns Desk & CRM
    story.append(make_figure_block("ui_returns_desk.png", "<b>Figure 5.5:</b> Reverse Logistics & Returns Desk with Instant Bill Barcode Scanner Lookup", target_width=PRINTABLE_WIDTH, max_height=185))
    story.append(Spacer(1, 6))

    story.append(make_figure_block("ui_patient_crm.png", "<b>Figure 5.6:</b> Patient Directory & Smart CRM with Asynchronous Phone Search and Collapsible Medical History", target_width=PRINTABLE_WIDTH, max_height=185))
    story.append(PageBreak())

    # Thermal Receipt
    story.append(make_figure_block("ui_thermal_receipt.png", "<b>Figure 5.7:</b> Standard 58mm/80mm Thermal Tax Invoice with HSN Reverse GST Breakdown & Scannable CODE128 Barcode", target_width=235, max_height=300))
    story.append(PageBreak())

    # ==================================================================
    # CHAPTER 6: SYSTEM VERIFICATION & QUALITY ASSURANCE
    # ==================================================================
    story.append(Paragraph("CHAPTER 6", style_chap_num))
    story.append(Paragraph("SYSTEM VERIFICATION & QUALITY ASSURANCE", style_chap_title))
    story.append(HRFlowable(width="100%", thickness=1.5, color=C_TEAL, spaceBefore=2, spaceAfter=10))

    story.append(Paragraph("6.1 Quality Assurance Strategy & Test Levels", style_sec_title))
    story.append(Paragraph(
        "Software testing was conducted across multiple tiers to verify algorithm accuracy, database consistency, security boundaries, "
        "and client-side responsiveness. The testing methodology encompasses four structured phases: (1) <b>Unit Testing</b> targeting isolated "
        "mathematical functions (reverse GST, FEFO sorting); (2) <b>Integration Testing</b> verifying data flow between the web interface, "
        "Django controller, signals, and database; (3) <b>Boundary Value Analysis (BVA)</b> testing edge conditions (zero stock, negative values, "
        "leap-year expiries); and (4) <b>User Acceptance Testing (UAT)</b> validating end-to-end pharmacy workflows.",
        style_body
    ))

    story.append(Paragraph("6.2 Formal Test Execution Matrix Table", style_sec_title))
    story.append(Paragraph(
        "The following matrix details the formal test cases executed against the Pharmacy Management ERP system:",
        style_body
    ))
    
    test_cases = [
        [Paragraph("<b>TC-ID</b>", style_th), Paragraph("<b>Module Under Test</b>", style_th), Paragraph("<b>Test Condition / Input Data</b>", style_th), Paragraph("<b>Expected System Output</b>", style_th), Paragraph("<b>Actual Result</b>", style_th), Paragraph("<b>Verdict</b>", style_th)],
        [Paragraph("TC-01", style_td), Paragraph("Authentication", style_td), Paragraph("Submit invalid username/password", style_td), Paragraph("Display error; deny access to system", style_td), Paragraph("Error alert shown; redirected to login", style_td), Paragraph("<font color='#16a34a'><b>PASS</b></font>", style_td_center)],
        [Paragraph("TC-02", style_td), Paragraph("RBAC Security", style_td), Paragraph("Cashier attempts URL <code>/inventory/</code>", style_td), Paragraph("Block access; redirect with warning", style_td), Paragraph("Access Denied message; redirected to billing", style_td), Paragraph("<font color='#16a34a'><b>PASS</b></font>", style_td_center)],
        [Paragraph("TC-03", style_td), Paragraph("FEFO Algorithm", style_td), Paragraph("Sell 15 units of drug with 2 batches (10 exp Jan, 10 exp Dec)", style_td), Paragraph("Deduct 10 from Jan batch; spill over 5 to Dec batch", style_td), Paragraph("Jan batch=0; Dec batch=5; exact quantities deducted", style_td), Paragraph("<font color='#16a34a'><b>PASS</b></font>", style_td_center)],
        [Paragraph("TC-04", style_td), Paragraph("Reverse GST", style_td), Paragraph("Medicine MRP=₹112.00, GST slab=12%", style_td), Paragraph("Base Price=₹100.00; CGST=₹6.00; SGST=₹6.00", style_td), Paragraph("Calculated Base=100.00, CGST=6.00, SGST=6.00", style_td), Paragraph("<font color='#16a34a'><b>PASS</b></font>", style_td_center)],
        [Paragraph("TC-05", style_td), Paragraph("Smart CRM AJAX", style_td), Paragraph("Enter registered 10-digit phone <code>9829054321</code>", style_td), Paragraph("Fetch customer name & doctor; turn border green", style_td), Paragraph("Fields auto-filled in 45ms; border turned green", style_td), Paragraph("<font color='#16a34a'><b>PASS</b></font>", style_td_center)],
        [Paragraph("TC-06", style_td), Paragraph("Master Data AJAX", style_td), Paragraph("Submit new medicine in modal during stock entry", style_td), Paragraph("Save to DB; inject into select dropdown without reload", style_td), Paragraph("Item added to dropdown; modal closed smoothly", style_td), Paragraph("<font color='#16a34a'><b>PASS</b></font>", style_td_center)],
        [Paragraph("TC-07", style_td), Paragraph("Django Signals", style_td), Paragraph("Delete a Sale row of 5 units from admin", style_td), Paragraph("Signal intercepts event; adds 5 units back to batch", style_td), Paragraph("Stock quantity increased by 5 automatically", style_td), Paragraph("<font color='#16a34a'><b>PASS</b></font>", style_td_center)],
        [Paragraph("TC-08", style_td), Paragraph("Barcode Scanner", style_td), Paragraph("Hardware scanner scans barcode and emits Enter", style_td), Paragraph("Trap Enter event; retain cursor in input without reload", style_td), Paragraph("Barcode captured; item added to cart preview", style_td), Paragraph("<font color='#16a34a'><b>PASS</b></font>", style_td_center)],
        [Paragraph("TC-09", style_td), Paragraph("Returns Desk", style_td), Paragraph("Scan bill barcode; return 2 units with restock=True", style_td), Paragraph("Create ReturnSale row; restore 2 units to batch", style_td), Paragraph("Return logged; stock shelf quantity restored", style_td), Paragraph("<font color='#16a34a'><b>PASS</b></font>", style_td_center)],
        [Paragraph("TC-10", style_td), Paragraph("Mobile Responsiveness", style_td), Paragraph("Open billing & inventory on 375px mobile viewport", style_td), Paragraph("No horizontal overflow; cards stack cleanly; touch OK", style_td), Paragraph("All tables scroll horizontally; clean app bar", style_td), Paragraph("<font color='#16a34a'><b>PASS</b></font>", style_td_center)]
    ]
    t_tests = Table(test_cases, colWidths=[PRINTABLE_WIDTH*0.1, PRINTABLE_WIDTH*0.18, PRINTABLE_WIDTH*0.25, PRINTABLE_WIDTH*0.25, PRINTABLE_WIDTH*0.14, PRINTABLE_WIDTH*0.08])
    t_tests.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_DARK_TEAL),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, C_LIGHT_BG])
    ]))
    story.append(t_tests)
    story.append(Paragraph("<b>Table 6.1:</b> Formal Quality Assurance Test Execution Matrix & Verdicts", style_caption))
    story.append(PageBreak())

    # ==================================================================
    # CHAPTER 7: SECURITY ARCHITECTURE & CLOUD DEPLOYMENT
    # ==================================================================
    story.append(Paragraph("CHAPTER 7", style_chap_num))
    story.append(Paragraph("SECURITY ARCHITECTURE & CLOUD DEPLOYMENT", style_chap_title))
    story.append(HRFlowable(width="100%", thickness=1.5, color=C_TEAL, spaceBefore=2, spaceAfter=10))

    story.append(Paragraph("7.1 Role-Based Access Control (RBAC) Hardening", style_sec_title))
    story.append(Paragraph(
        "The application enforces strict data segregation using Django's built-in group and permissions registry, creating "
        "three explicit tiers of operational clearance:<br/>"
        "• <b>Tier 1 — Store Owner / Superuser:</b> Full system authority. Can modify database models, view gross profit metrics, "
        "inspect net margin charts, view lifetime patient spending aggregates, and export sales ledgers.<br/>"
        "• <b>Tier 2 — Store Manager (Staff):</b> Authorized to manage wholesale supplier consignments, log stock batches, and operate the POS counter. "
        "Strictly blocked from raw admin backdoors and executive revenue/profit charts.<br/>"
        "• <b>Tier 3 — Counter Cashier:</b> Operates the high-speed POS billing terminal, processes sales, and looks up customer contact details. "
        "Financial metrics, unit margins, and lifetime customer spending totals are dynamically redacted from the template DOM via "
        "<code>{% if request.user.is_superuser %}</code> conditional filters.",
        style_body
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("7.2 Session Timeout & Administrative Obfuscation", style_sec_title))
    story.append(Paragraph(
        "To protect counter terminals during shift handovers, banking-grade session security parameters were enforced in <code>settings.py</code>:<br/>"
        "• <code>SESSION_EXPIRE_AT_BROWSER_CLOSE = True</code>: Invalidates the cryptographic session token upon tab/browser closure.<br/>"
        "• <code>SESSION_COOKIE_AGE = 1800</code>: Automatically terminates inactive sessions after exactly 30 minutes of counter idle time.<br/>"
        "• <b>Admin Route Obfuscation:</b> Standard Django deployments leave <code>/admin/</code> open to brute-force bot attacks. The master gateway "
        "was obfuscated to a custom cryptographic route, preventing automated script targeting.",
        style_body
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("7.3 Cloud Deployment on PythonAnywhere PaaS", style_sec_title))
    story.append(Paragraph(
        "The application is deployed live in the cloud via <b>PythonAnywhere</b> PaaS under the Linux WSGI execution environment. "
        "The deployment pipeline incorporates environment variable isolation (.env), DEBUG lockout, and static pre-compilation via collectstatic.",
        style_body
    ))
    story.append(PageBreak())

    # ==================================================================
    # CHAPTER 8: CONCLUSION & FUTURE SCOPE
    # ==================================================================
    story.append(Paragraph("CHAPTER 8", style_chap_num))
    story.append(Paragraph("CONCLUSION & FUTURE SCOPE", style_chap_title))
    story.append(HRFlowable(width="100%", thickness=1.5, color=C_TEAL, spaceBefore=2, spaceAfter=10))

    story.append(Paragraph("8.1 Concluding Remarks & Realized Value", style_sec_title))
    story.append(Paragraph(
        "The <b>Pharmacy Management System (Pharmacy ERP)</b> demonstrates the successful engineering of an enterprise web application "
        "specifically tailored to solve the structural and operational challenges of pharmaceutical retail. By moving beyond generic "
        "CRUD software, the platform delivers real clinical and commercial value through algorithmic FEFO inventory optimization, "
        "statutory reverse GST billing, asynchronous patient memory, and real-time business intelligence dashboards.<br/><br/>"
        "The project rigorously satisfies the academic standards of the Department of Computer Science & Information Technology, "
        "School of Technology, Maulana Azad National Urdu University. From initial requirement engineering through visual DFD/ER modeling, "
        "robust Python/Django implementation, thorough quality assurance testing, and live cloud deployment, the system exemplifies the "
        "practical application of modern software engineering methodologies to a mission-critical domain.",
        style_body
    ))
    story.append(Spacer(1, 8))

    story.append(Paragraph("8.2 Phase 2 Strategic Roadmap", style_sec_title))
    story.append(Paragraph(
        "The modular architecture established in Version 1.0 provides an ideal launching pad for Phase 2 commercial expansions:",
        style_body
    ))
    roadmap_items = [
        "<b>Optical Character Recognition (OCR) Prescription Parsing:</b> Integrating Tesseract OCR / Google Vision AI to extract medicine names and dosages directly from physician prescription photos.",
        "<b>Machine Learning Demand Forecasting:</b> Implementing ARIMA / Prophet models in scikit-learn to predict seasonal drug shortages (e.g. anti-malarials during monsoon) based on historical sales curves.",
        "<b>WhatsApp Business API Dispatch:</b> Automatically dispatching digital tax invoices and medication refill reminders directly to patients' WhatsApp accounts.",
        "<b>Flutter Cross-Platform Mobile App:</b> Developing native iOS and Android apps connected to Django REST Framework (DRF) endpoints for remote owner monitoring.",
        "<b>PostgreSQL Migration & Dockerization:</b> Transitioning the persistence layer to enterprise PostgreSQL with Docker containerization and automated CI/CD pipelines."
    ]
    for rmi in roadmap_items:
        story.append(Paragraph(f"• {rmi}", style_bullet))
    story.append(PageBreak())

    # ==================================================================
    # CHAPTER 9: REFERENCES & BIBLIOGRAPHY
    # ==================================================================
    story.append(Paragraph("CHAPTER 9", style_chap_num))
    story.append(Paragraph("REFERENCES & BIBLIOGRAPHY", style_chap_title))
    story.append(HRFlowable(width="100%", thickness=1.5, color=C_TEAL, spaceBefore=2, spaceAfter=10))

    story.append(Paragraph("9.1 Academic Textbooks", style_subsec_title))
    books = [
        "Pressman, R. S., & Maxim, B. R. (2019). <i>Software Engineering: A Practitioner's Approach</i> (9th ed.). McGraw-Hill Education.",
        "Elmasri, R., & Navathe, S. B. (2016). <i>Fundamentals of Database Systems</i> (7th ed.). Pearson Education.",
        "Lutz, M. (2013). <i>Learning Python</i> (5th ed.). O'Reilly Media.",
        "Duckett, J. (2014). <i>HTML and CSS: Design and Build Websites</i>. John Wiley & Sons.",
        "Duckett, J. (2014). <i>JavaScript and JQuery: Interactive Front-End Web Development</i>. John Wiley & Sons."
    ]
    for bk in books:
        story.append(Paragraph(f"[1] {bk}" if bk == books[0] else f"[{books.index(bk)+1}] {bk}", style_bullet))
    story.append(Spacer(1, 6))

    story.append(Paragraph("9.2 World Health Organization (WHO) & Regulatory Guidelines", style_subsec_title))
    who_refs = [
        "World Health Organization. (2019). <i>Good Storage and Distribution Practices for Medical Products</i>. WHO Technical Report Series No. 1025, Annex 7.",
        "World Health Organization. (2011). <i>Model Guidance for the Storage and Transport of Time- and Temperature-Sensitive Pharmaceutical Products</i>. WHO Technical Report Series No. 961, Annex 9.",
        "Central Board of Indirect Taxes and Customs (CBIC), Government of India. (2020). <i>GST Rates on Pharmaceutical Products & HSN Classification Guidelines</i>."
    ]
    for wr in who_refs:
        story.append(Paragraph(f"[{len(books)+who_refs.index(wr)+1}] {wr}", style_bullet))
    story.append(Spacer(1, 6))

    story.append(Paragraph("9.3 Technical & Framework Documentation", style_subsec_title))
    doc_refs = [
        "Django Software Foundation. (2026). <i>Django 6.0 Documentation: Models, Views, Templates, and Signals</i>. Available at: https://docs.djangoproject.com/",
        "Python Software Foundation. (2026). <i>Python 3.14 Language Reference and Standard Library</i>. Available at: https://docs.python.org/3/",
        "Bootstrap Core Team. (2026). <i>Bootstrap 5.3 Framework Reference & Responsive Grid Architecture</i>. Available at: https://getbootstrap.com/",
        "Chart.js Community. (2026). <i>Chart.js: Open Source HTML5 Canvas Charting Library</i>. Available at: https://www.chartjs.org/",
        "Lindell, J. (2025). <i>JsBarcode: JavaScript Barcode Generator Documentation</i>. Available at: https://github.com/lindell/JsBarcode",
        "Select2 Team. (2025). <i>Select2: The jQuery Replacement for Select Boxes</i>. Available at: https://select2.org/"
    ]
    for dr in doc_refs:
        story.append(Paragraph(f"[{len(books)+len(who_refs)+doc_refs.index(dr)+1}] {dr}", style_bullet))

    # Build Document
    print(f"Building PDF document: {PDF_OUTPUT}...")
    doc = SimpleDocTemplate(
        PDF_OUTPUT,
        pagesize=A4,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    doc.build(story, canvasmaker=AcademicNumberedCanvas)
    print("Build completed successfully!")

if __name__ == "__main__":
    build_report()
