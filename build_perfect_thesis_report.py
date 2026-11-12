"""
================================================================================
PHARMACY MANAGEMENT SYSTEM - MAJOR PROJECT THESIS REPORT BUILDER
Department of Computer Science & Information Technology
Maulana Azad National Urdu University (MANUU), Hyderabad
Authors: MD Zeeshan (23BTCS026HY) & Yusuf Hanzala (23BTCS005HY)
Supervisor: Dr. Nusrath Fathima
Coordinator: Dr. Ahmed Talha Siddiqui | Head of Dept: Prof. Pradeep Kumar
================================================================================
"""

import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, 
    KeepTogether, PageBreak, HRFlowable, Preformatted
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from PIL import Image as PILImage

BASE_DIR = r"c:\programming\erp_pharmacy_project"
ASSETS_DIR = os.path.join(BASE_DIR, "report_assets")
OUTPUT_PDF = os.path.join(BASE_DIR, "Pharmacy_Management_System_Final_Project_Report.pdf")

# Page Dimensions (Letter: 612 x 792 pt)
PAGE_WIDTH, PAGE_HEIGHT = letter
BORDER_MARGIN = 26.0
LEFT_MARGIN = 56.0
RIGHT_MARGIN = 56.0
TOP_MARGIN = 50.0
BOTTOM_MARGIN = 62.0
CONTENT_WIDTH = PAGE_WIDTH - LEFT_MARGIN - RIGHT_MARGIN # 500 pt

# Colors
C_TEXT = colors.HexColor("#111827")
C_MUTED = colors.HexColor("#4b5563")
C_BORDER = colors.HexColor("#1f2937")
C_LINE = colors.HexColor("#9ca3af")
C_BG_CODE = colors.HexColor("#f8fafc")
C_BORDER_CODE = colors.HexColor("#cbd5e1")
C_NAVY = colors.HexColor("#0f172a")
C_MAROON = colors.HexColor("#991b1b")
C_DARK_BLUE = colors.HexColor("#1e3a8a")

# ----------------------------------------------------------------------
# TWO-PASS CANVAS WITH ACADEMIC BORDER & DUAL PAGINATION
# ----------------------------------------------------------------------
class AcademicReportCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pages = []

    def showPage(self):
        self.pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        total_pages = len(self.pages)
        for idx, page_state in enumerate(self.pages):
            self.__dict__.update(page_state)
            p_num = idx + 1
            self.draw_decorations(p_num, total_pages)
            super().showPage()
        super().save()

    def draw_decorations(self, p_num, total_pages):
        self.saveState()
        
        # 1. Outer Academic Border Frame on ALL pages
        self.setStrokeColor(C_BORDER)
        self.setLineWidth(1.0)
        self.rect(BORDER_MARGIN, BORDER_MARGIN, PAGE_WIDTH - 2 * BORDER_MARGIN, PAGE_HEIGHT - 2 * BORDER_MARGIN)
        
        # Double border on Cover Page
        if p_num == 1:
            self.setLineWidth(0.5)
            self.rect(BORDER_MARGIN + 3.5, BORDER_MARGIN + 3.5, PAGE_WIDTH - 2 * (BORDER_MARGIN + 3.5), PAGE_HEIGHT - 2 * (BORDER_MARGIN + 3.5))
            self.restoreState()
            return
            
        # Subtle horizontal rule above footer
        self.setStrokeColor(C_LINE)
        self.setLineWidth(0.6)
        self.line(LEFT_MARGIN, 48, PAGE_WIDTH - RIGHT_MARGIN, 48)
        
        # 2. Footers: Front Matter vs Body
        # Front matter pages: 2, 3, 4, 5, 6
        if p_num in [2, 3, 4, 5, 6]:
            roman = ["", "i", "ii", "iii", "iv", "v", "vi"][p_num]
            self.setFont("Times-Roman", 10)
            self.setFillColor(C_TEXT)
            self.drawRightString(PAGE_WIDTH - RIGHT_MARGIN, 34, f"{roman} | P a g e")
        elif p_num == 7:
            # Title Poster Page (Transition)
            self.setFont("Times-Roman", 9)
            self.setFillColor(C_MUTED)
            self.drawString(LEFT_MARGIN, 34, "PHARMACY MANAGEMENT SYSTEM — MAJOR PROJECT REPORT")
        else:
            # Main Body (Chapter 1 onwards, where p_num >= 8)
            body_p = p_num - 7
            self.setFont("Times-Roman", 9)
            self.setFillColor(C_MUTED)
            self.drawString(LEFT_MARGIN, 34, "PHARMACY MANAGEMENT SYSTEM — MAJOR PROJECT REPORT")
            
            self.setFont("Times-Roman", 10)
            self.setFillColor(C_TEXT)
            self.drawRightString(PAGE_WIDTH - RIGHT_MARGIN, 34, f"{body_p} | P a g e")
            
        self.restoreState()

# ----------------------------------------------------------------------
# TYPOGRAPHY & PARAGRAPH STYLES (ACADEMIC TIMES NEW ROMAN)
# ----------------------------------------------------------------------
styles = getSampleStyleSheet()

style_cover_super = ParagraphStyle('CoverSuper', fontName='Times-Bold', fontSize=11, leading=15, alignment=TA_CENTER, textColor=C_MUTED)
style_cover_title = ParagraphStyle('CoverTitle', fontName='Times-Bold', fontSize=21, leading=26, alignment=TA_CENTER, textColor=C_NAVY)
style_cover_sub = ParagraphStyle('CoverSub', fontName='Times-Bold', fontSize=13, leading=17, alignment=TA_CENTER, textColor=C_DARK_BLUE)
style_cover_body = ParagraphStyle('CoverBody', fontName='Times-Roman', fontSize=11, leading=16, alignment=TA_CENTER, textColor=C_TEXT)

style_chap_num = ParagraphStyle('ChapNum', fontName='Times-Bold', fontSize=15, leading=18, alignment=TA_LEFT, textColor=C_TEXT, spaceAfter=2)
style_chap_title = ParagraphStyle('ChapTitle', fontName='Times-Bold', fontSize=15, leading=19, alignment=TA_LEFT, textColor=C_TEXT, spaceAfter=6)

style_h1 = ParagraphStyle('H1', fontName='Times-Bold', fontSize=12.5, leading=16.5, textColor=C_TEXT, spaceBefore=12, spaceAfter=5, keepWithNext=True)
style_h2 = ParagraphStyle('H2', fontName='Times-Bold', fontSize=11.5, leading=15, textColor=C_TEXT, spaceBefore=9, spaceAfter=3, keepWithNext=True)

style_body = ParagraphStyle('Body', fontName='Times-Roman', fontSize=11, leading=16, textColor=C_TEXT, alignment=TA_JUSTIFY, spaceAfter=8)
style_bullet = ParagraphStyle('Bullet', fontName='Times-Roman', fontSize=11, leading=15.5, textColor=C_TEXT, alignment=TA_JUSTIFY, leftIndent=22, firstLineIndent=-12, spaceAfter=4)
style_bullet_sub = ParagraphStyle('BulletSub', fontName='Times-Roman', fontSize=10.5, leading=15, textColor=C_TEXT, alignment=TA_JUSTIFY, leftIndent=38, firstLineIndent=-12, spaceAfter=3)

style_table_header = ParagraphStyle('TH', fontName='Times-Bold', fontSize=10, leading=13, alignment=TA_CENTER, textColor=colors.white)
style_table_cell = ParagraphStyle('TD', fontName='Times-Roman', fontSize=9.5, leading=13, textColor=C_TEXT)
style_table_cell_bold = ParagraphStyle('TDBold', fontName='Times-Bold', fontSize=9.5, leading=13, textColor=C_TEXT)

style_code = ParagraphStyle('Code', fontName='Courier', fontSize=7.8, leading=10.2, textColor=colors.HexColor("#0f172a"))
style_caption = ParagraphStyle('Caption', fontName='Times-Bold', fontSize=10.5, leading=14, alignment=TA_CENTER, textColor=C_BORDER, spaceBefore=6, spaceAfter=10)
style_banner_title = ParagraphStyle('BannerTitle', fontName='Times-Bold', fontSize=11, leading=14, alignment=TA_CENTER, textColor=colors.white)

# ----------------------------------------------------------------------
# HELPER FLOWABLE BUILDERS
# ----------------------------------------------------------------------
def make_chapter_header(chap_num_str, chap_title_str):
    return [
        Paragraph(chap_num_str, style_chap_num),
        Paragraph(chap_title_str, style_chap_title),
        HRFlowable(width="100%", thickness=1.0, color=C_BORDER, spaceBefore=2, spaceAfter=14, hAlign='LEFT')
    ]

def make_scaled_image(rel_path, target_width=CONTENT_WIDTH, max_height=None):
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

def make_figure_block(rel_path, caption, target_width=CONTENT_WIDTH, max_height=320):
    img = make_scaled_image(rel_path, target_width=target_width, max_height=max_height)
    cap = Paragraph(caption, style_caption)
    return KeepTogether([img, Spacer(1, 4), cap])

def make_snapshot_card(rel_path, banner_text, caption, target_width=CONTENT_WIDTH, max_height=260):
    header_p = Paragraph(f"<b>{banner_text}</b>", style_banner_title)
    img = make_scaled_image(rel_path, target_width=target_width - 16, max_height=max_height)
    
    t = Table([[header_p], [img]], colWidths=[target_width])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_BORDER),
        ('BACKGROUND', (0,1), (-1,1), colors.white),
        ('BOX', (0,0), (-1,-1), 1.0, C_BORDER),
        ('TOPPADDING', (0,0), (-1,0), 5),
        ('BOTTOMPADDING', (0,0), (-1,0), 5),
        ('TOPPADDING', (0,1), (-1,1), 8),
        ('BOTTOMPADDING', (0,1), (-1,1), 8),
        ('LEFTPADDING', (0,1), (-1,1), 8),
        ('RIGHTPADDING', (0,1), (-1,1), 8),
        ('ALIGN', (0,1), (-1,1), 'CENTER'),
    ]))
    cap = Paragraph(caption, style_caption)
    return KeepTogether([t, Spacer(1, 4), cap])

def make_code_card(code_str, filename=""):
    header_p = Paragraph(f"<b>Source File:</b> <font color='#1e3a8a'>{filename}</font>", 
                         ParagraphStyle('CodeH', fontName='Courier-Bold', fontSize=8.5, leading=11, textColor=C_TEXT))
    code_p = Preformatted(code_str, style_code)
    
    t = Table([[header_p], [code_p]], colWidths=[CONTENT_WIDTH])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#e2e8f0")),
        ('BACKGROUND', (0,1), (-1,1), C_BG_CODE),
        ('BOX', (0,0), (-1,-1), 0.75, C_BORDER_CODE),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER_CODE),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    return KeepTogether(t)

# ----------------------------------------------------------------------
# DOCUMENT STORY BUILDER
# ----------------------------------------------------------------------
def build_story():
    story = []
    
    header_banner = os.path.join(ASSETS_DIR, "manuu_header_banner.jpg")
    emblem_img = os.path.join(ASSETS_DIR, "manuu_emblem.png")
    
    # ==================================================================
    # PAGE 1: FORMAL UNIVERSITY COVER PAGE
    # ==================================================================
    if os.path.exists(header_banner):
        story.append(Image(header_banner, width=CONTENT_WIDTH, height=52))
        story.append(Spacer(1, 14))
    else:
        story.append(Spacer(1, 20))
        
    story.append(Paragraph("A PROJECT REPORT ON", style_cover_super))
    story.append(Spacer(1, 6))
    story.append(Paragraph("PHARMACY MANAGEMENT SYSTEM", style_cover_title))
    story.append(Spacer(1, 4))
    story.append(Paragraph("A Centralized Web-Based Enterprise Resource Planning (ERP) Platform", style_cover_sub))
    story.append(HRFlowable(width="65%", thickness=1.2, color=C_NAVY, spaceBefore=4, spaceAfter=14, hAlign='CENTER'))
    
    story.append(Paragraph(
        "Submitted in partial fulfillment of the requirements for the award of the degree of<br/>"
        "<b>BACHELOR OF TECHNOLOGY</b><br/>"
        "in<br/>"
        "<b>COMPUTER SCIENCE</b>",
        style_cover_body
    ))
    story.append(Spacer(1, 10))
    
    if os.path.exists(emblem_img):
        story.append(Image(emblem_img, width=82, height=121))
        story.append(Spacer(1, 12))
    else:
        story.append(Spacer(1, 30))
        
    t_meta = Table([
        [Paragraph("<b>Submitted By:</b>", ParagraphStyle('SB', fontName='Times-Bold', fontSize=10.5, leading=14)),
         Paragraph("<b>Under the Supervision of:</b>", ParagraphStyle('SB2', fontName='Times-Bold', fontSize=10.5, leading=14))],
        [Paragraph("<b>MD ZEESHAN</b> (Roll No: 23BTCS026HY)<br/>Enrollment No: A230117<br/>"
                   "<b>YUSUF HANZALA</b> (Roll No: 23BTCS005HY)<br/>Enrollment No: A230093",
                   ParagraphStyle('SBD', fontName='Times-Roman', fontSize=9.5, leading=14)),
         Paragraph("<b>Dr. Nusrath Fathima</b><br/>Assistant Professor<br/>Dept. of CS &amp; IT, MANUU",
                   ParagraphStyle('SBD2', fontName='Times-Roman', fontSize=9.5, leading=14))]
    ], colWidths=[CONTENT_WIDTH*0.52, CONTENT_WIDTH*0.48])
    t_meta.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 16))
    
    story.append(Paragraph(
        "<b>DEPARTMENT OF COMPUTER SCIENCE &amp; INFORMATION TECHNOLOGY</b><br/>"
        "<b>SCHOOL OF TECHNOLOGY</b><br/>"
        "<b>MAULANA AZAD NATIONAL URDU UNIVERSITY</b><br/>"
        "<font size='9'>(A Central University Accredited \"A+\" Grade by NAAC)</font><br/>"
        "<font size='9'>Gachibowli, Hyderabad, Telangana - 500032 (India)</font><br/>"
        "<b>Academic Year: 2026-27</b>",
        ParagraphStyle('DeptFoot', fontName='Times-Roman', fontSize=9.5, leading=13.5, alignment=TA_CENTER)
    ))
    story.append(PageBreak())

    # ==================================================================
    # PAGE 2: CERTIFICATE OF AUTHENTICITY (Page ii)
    # ==================================================================
    if os.path.exists(header_banner):
        story.append(Image(header_banner, width=CONTENT_WIDTH, height=52))
        story.append(Spacer(1, 14))
    
    story.append(Paragraph("<u>CERTIFICATE</u>", ParagraphStyle('CertHead', fontName='Times-Bold', fontSize=15, leading=19, alignment=TA_CENTER, textColor=C_NAVY)))
    story.append(Spacer(1, 18))
    
    cert_text = (
        "This is to certify that the project report entitled <b>\"PHARMACY MANAGEMENT SYSTEM – A CENTRALIZED "
        "WEB-BASED ERP PLATFORM\"</b> submitted by <b>MD ZEESHAN</b> (Roll No: <b>23BTCS026HY</b>, Enrollment No: "
        "<b>A230117</b>) and <b>YUSUF HANZALA</b> (Roll No: <b>23BTCS005HY</b>, Enrollment No: <b>A230093</b>) "
        "in partial fulfillment of the requirements for the award of the degree of <b>Bachelor of Technology (Computer Science) "
        "- VII Semester</b> during the academic year <b>2026-27</b> in the Department of Computer Science &amp; Information "
        "Technology, Maulana Azad National Urdu University, Hyderabad, is a bonafide record of authentic project work "
        "carried out under my direct supervision and guidance.<br/><br/>"
        "The results embodied in this report have not been submitted to any other University or Institute for the award "
        "of any other degree or diploma."
    )
    story.append(Paragraph(cert_text, style_body))
    story.append(Spacer(1, 18))
    story.append(Paragraph("<b>Date:</b> 13 November, 2026<br/><b>Place:</b> Hyderabad", ParagraphStyle('DatePlace', fontName='Times-Roman', fontSize=10, leading=15)))
    story.append(Spacer(1, 55))
    
    t_signs = Table([
        [Paragraph("<b>External Examiner</b>", ParagraphStyle('S1', fontName='Times-Bold', fontSize=10, alignment=TA_LEFT)),
         Paragraph("<b>Dr. Nusrath Fathima</b><br/>Supervisor / Assistant Professor<br/>Dept. of CS &amp; IT, MANUU", ParagraphStyle('S2', fontName='Times-Roman', fontSize=9.5, alignment=TA_CENTER, leading=13)),
         Paragraph("<b>Prof. Pradeep Kumar</b><br/>Head of Department<br/>Dept. of CS &amp; IT, MANUU", ParagraphStyle('S3', fontName='Times-Roman', fontSize=9.5, alignment=TA_RIGHT, leading=13))]
    ], colWidths=[CONTENT_WIDTH*0.28, CONTENT_WIDTH*0.42, CONTENT_WIDTH*0.30])
    t_signs.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(t_signs)
    story.append(PageBreak())

    # ==================================================================
    # PAGE 3: CANDIDATE'S DECLARATION (Page iii)
    # ==================================================================
    if os.path.exists(header_banner):
        story.append(Image(header_banner, width=CONTENT_WIDTH, height=52))
        story.append(Spacer(1, 14))
    
    story.append(Paragraph("<u>CANDIDATE'S DECLARATION</u>", ParagraphStyle('DeclHead', fontName='Times-Bold', fontSize=15, leading=19, alignment=TA_CENTER, textColor=C_NAVY)))
    story.append(Spacer(1, 18))
    
    decl_text = (
        "We hereby declare that the project work presented in this report entitled <b>\"PHARMACY MANAGEMENT "
        "SYSTEM – A CENTRALIZED WEB-BASED ERP PLATFORM\"</b> submitted towards the partial fulfillment of the requirements "
        "for the award of the degree of <b>BACHELOR OF TECHNOLOGY (COMPUTER SCIENCE)</b> in the Department of Computer "
        "Science &amp; Information Technology, Maulana Azad National Urdu University, Hyderabad, is an authentic and "
        "original record of our own work carried out under the guidance of <b>Dr. Nusrath Fathima</b> (Assistant Professor, "
        "Dept. of CS &amp; IT).<br/><br/>"
        "We further declare that the matter embodied in this project report has not been submitted by us for the award "
        "of any other degree, diploma, associateship, or fellowship to any other University or Institution of higher learning."
    )
    story.append(Paragraph(decl_text, style_body))
    story.append(Spacer(1, 18))
    story.append(Paragraph("<b>Date:</b> 13 November, 2026<br/><b>Place:</b> Hyderabad", ParagraphStyle('DatePlace2', fontName='Times-Roman', fontSize=10, leading=15)))
    story.append(Spacer(1, 60))
    
    t_cands = Table([
        [Paragraph("<b>MD ZEESHAN</b><br/>Roll No: 23BTCS026HY<br/>Enrollment No: A230117", ParagraphStyle('C1', fontName='Times-Roman', fontSize=10, alignment=TA_LEFT, leading=15)),
         Paragraph("<b>YUSUF HANZALA</b><br/>Roll No: 23BTCS005HY<br/>Enrollment No: A230093", ParagraphStyle('C2', fontName='Times-Roman', fontSize=10, alignment=TA_RIGHT, leading=15))]
    ], colWidths=[CONTENT_WIDTH*0.5, CONTENT_WIDTH*0.5])
    story.append(t_cands)
    story.append(PageBreak())

    # ==================================================================
    # PAGE 4: ACKNOWLEDGEMENT (Page iv)
    # ==================================================================
    if os.path.exists(header_banner):
        story.append(Image(header_banner, width=CONTENT_WIDTH, height=52))
        story.append(Spacer(1, 14))
    
    story.append(Paragraph("<u>ACKNOWLEDGEMENT</u>", ParagraphStyle('AckHead', fontName='Times-Bold', fontSize=15, leading=19, alignment=TA_CENTER, textColor=C_NAVY)))
    story.append(Spacer(1, 18))
    
    ack_text = (
        "We express our profound and sincere gratitude towards our <b>Supervisor Dr. Nusrath Fathima</b>, "
        "Assistant Professor, Department of Computer Science and Information Technology, Maulana Azad National "
        "Urdu University, Hyderabad, for her continuous encouragement, invaluable guidance, and perceptive feedback "
        "throughout the design, development, and technical documentation of this project.<br/><br/>"
        "We are deeply indebted to our <b>Project Coordinator Dr. Ahmed Talha Siddiqui</b>, Assistant Professor, "
        "Department of Computer Science and Information Technology, for his insightful suggestions, technical advice, "
        "and administrative support. In spite of his demanding schedule, he was always accessible to provide valuable "
        "counsel and steer our development towards standard industry best practices.<br/><br/>"
        "We sincerely thank <b>Prof. Abdul Wahid</b>, Dean, School of Technology, and <b>Prof. Pradeep Kumar</b>, "
        "Head, Department of Computer Science and Information Technology, Maulana Azad National Urdu University, "
        "for granting the requisite institutional facilities, lab resources, and continuous academic encouragement.<br/><br/>"
        "We extend our heartfelt gratitude to the <b>Hon'ble Vice Chancellor Prof. Syed Ainul Hasan</b>, Maulana "
        "Azad National Urdu University, for establishing an outstanding scholarly environment that motivates innovation "
        "and technological excellence across student endeavors.<br/><br/>"
        "Lastly, we convey our warm appreciation to our parents, family members, classmates, and friends whose unwavering "
        "moral support and constructive discussions helped us overcome technical hurdles and complete this work successfully."
    )
    story.append(Paragraph(ack_text, style_body))
    story.append(Spacer(1, 24))
    
    story.append(Table([
        [Paragraph("<b>MD ZEESHAN</b> (23BTCS026HY)", ParagraphStyle('AC1', fontName='Times-Bold', fontSize=10, alignment=TA_LEFT)),
         Paragraph("<b>YUSUF HANZALA</b> (23BTCS005HY)", ParagraphStyle('AC2', fontName='Times-Bold', fontSize=10, alignment=TA_RIGHT))]
    ], colWidths=[CONTENT_WIDTH*0.5, CONTENT_WIDTH*0.5]))
    story.append(PageBreak())

    # ==================================================================
    # PAGE 5: ABSTRACT (Page v)
    # ==================================================================
    if os.path.exists(header_banner):
        story.append(Image(header_banner, width=CONTENT_WIDTH, height=52))
        story.append(Spacer(1, 14))
    
    story.append(Paragraph("<u>ABSTRACT</u>", ParagraphStyle('AbsHead', fontName='Times-Bold', fontSize=15, leading=19, alignment=TA_CENTER, textColor=C_NAVY)))
    story.append(Spacer(1, 16))
    
    abs_text = (
        "The retail pharmaceutical sector operates within a demanding, highly regulated environment that requires "
        "absolute precision in batch inventory tracking, medicine expiry management, Goods and Services Tax (GST) "
        "calculations, and regulatory compliance. Traditional pharmacy operations in India frequently depend on manual "
        "paper registers, fragmented desktop accounting packages, or generic retail software. This fragmentation introduces "
        "severe vulnerabilities, including medicine expiry before sale (leading to heavy dead-stock financial losses), "
        "slow billing queues during peak hours, human calculation errors in statutory tax breakdowns, untraceable batches "
        "during regulatory drug recalls, and a complete lack of real-time operational visibility for pharmacy owners.<br/><br/>"
        "To decisively solve these operational challenges, this project presents the <b>Pharmacy Management System (Pharmacy ERP)</b>, "
        "an enterprise-grade, centralized web-based platform engineered specifically around the daily workflows of retail pharmacies "
        "and medical stores. Developed using a robust three-tier Model-View-Template (MVT) architecture powered by <b>Python 3.14</b>, "
        "<b>Django 6.0.4</b>, and a normalized <b>SQLite</b> relational database (PostgreSQL-ready), the system integrates ten "
        "cohesive functional modules.<br/><br/>"
        "Key capabilities include: <b>(1) Algorithmic First-Expire-First-Out (FEFO) Inventory Handling</b>, which automatically "
        "prioritizes the dispensing of medicines with the nearest expiration date; <b>(2) Dynamic Reverse GST Calculation</b>, "
        "which extracts base taxable value and CGST/SGST amounts from statutory Maximum Retail Prices (MRP); <b>(3) High-Speed "
        "Point of Sale (POS) Counter</b> with native USB/Bluetooth barcode scanning and dynamic CODE128 thermal receipt generation; "
        "<b>(4) Asynchronous Patient CRM</b> using AJAX for sub-second telephone number lookups and collapsible medication histories; "
        "<b>(5) Reverse Logistics Desk</b> for secure medicine returns, refund calculations, and automated stock restoration; and "
        "<b>(6) Business Intelligence Dashboards</b> providing real-time revenue summaries, profit metrics, low-stock warnings, and "
        "automated CSV Purchase Order reorder generation.<br/><br/>"
        "The system incorporates three-tier Role-Based Access Control (RBAC), banking-grade session timeout security (1800 seconds), "
        "environment variable isolation, and complete cross-device mobile responsiveness across smartphones, tablets, and desktop terminals. "
        "The platform has been successfully deployed in a production cloud environment on <b>PythonAnywhere</b> PaaS with WSGI interfacing, "
        "delivering a secure, modern, and reliable digital transformation solution for retail pharmacies."
    )
    story.append(Paragraph(abs_text, style_body))
    story.append(PageBreak())

    # ==================================================================
    # PAGE 6: TABLE OF CONTENTS (Page vi)
    # ==================================================================
    story.append(Paragraph("<u>TABLE OF CONTENTS</u>", ParagraphStyle('TOCHead', fontName='Times-Bold', fontSize=15, leading=19, alignment=TA_CENTER, textColor=C_NAVY)))
    story.append(Spacer(1, 14))
    
    # Dotted TOC rows matched with 100% precision to actual page generation
    toc_rows = [
        ("Certificate of Authenticity", "ii", True),
        ("Candidate's Declaration", "iii", True),
        ("Acknowledgement", "iv", True),
        ("Abstract", "v", True),
        ("Chapter 1: Introduction", "1", True),
        ("    1.1 Overview · 1.2 Problem Statement", "1", False),
        ("    1.3 Project Objectives · 1.4 Report Layout", "2", False),
        ("Chapter 2: Feasibility Study", "4", True),
        ("    2.1 Technical · 2.2 Operational · 2.3 Economic Feasibility", "4", False),
        ("    2.4 System Requirement (Hardware & Software Tables)", "6", False),
        ("Chapter 3: System Analysis", "7", True),
        ("    3.1 Methodology · 3.2 Development Methodology", "7", False),
        ("    3.3 Development Model (Waterfall SDLC) · 3.4 Deployment", "8", False),
        ("    3.5 Training and User Support", "9", False),
        ("Chapter 4: System Design", "10", True),
        ("    4.1 Module Description (10 Core Modules)", "10", False),
        ("    4.2.1 Data Flow Diagram (Level 0 Context DFD)", "11", False),
        ("    4.2.2 Data Flow Diagram (Level 1 Decomposition DFD)", "12", False),
        ("    4.3 Entity Relationship (ER) Diagram", "13", False),
        ("    4.4 Database Schema & Relational Data Dictionary", "13", False),
        ("Chapter 5: System Implementation", "15", True),
        ("    5.1 Django Backend · 5.2 Frontend Technologies", "15", False),
        ("    5.3 SQLite Database · 5.4 Authentication & RBAC", "16", False),
        ("    5.5 Django ORM (Object Relational Mapping)", "17", False),
        ("    5.6 Source Code Implementations (Templates, Views, Models)", "18", False),
        ("    5.7 User Interface Snapshots (7 Operational Figures)", "22", False),
        ("Chapter 6: System Testing", "29", True),
        ("    6.1 Testing Methodologies · 6.2 Testing Under Various States", "29", False),
        ("    6.3 Formal Test Execution Matrix Table · Current Status", "30", False),
        ("Chapter 7: Conclusion and Future Scope", "31", True),
        ("    7.1 Conclusion · 7.2 Ten Strategic Enhancements", "31", False),
        ("Chapter 8: References & Bibliography", "33", True),
        ("    8.1 Books · 8.2 Research Papers · 8.3 Websites · 8.4 Documentation", "33", False),
    ]
    
    t_toc_data = []
    for title, p_str, is_major in toc_rows:
        f_name = 'Times-Bold' if is_major else 'Times-Roman'
        f_size = 10 if is_major else 9.5
        p_title = Paragraph(f"<b>{title}</b>" if is_major else title, ParagraphStyle('T1', fontName=f_name, fontSize=f_size, leading=13))
        p_page = Paragraph(f"<b>{p_str}</b>" if is_major else p_str, ParagraphStyle('T2', fontName=f_name, fontSize=f_size, leading=13, alignment=TA_RIGHT))
        t_toc_data.append([p_title, p_page])
        
    t_toc = Table(t_toc_data, colWidths=[CONTENT_WIDTH*0.88, CONTENT_WIDTH*0.12])
    t_toc.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 1.2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.2),
        ('LINEBELOW', (0,0), (-1,-1), 0.3, colors.HexColor("#e5e7eb")),
    ]))
    story.append(t_toc)
    story.append(PageBreak())

    # ==================================================================
    # PAGE 7: PROJECT POSTER TITLE PAGE (Source Page 1 Style)
    # ==================================================================
    story.append(Spacer(1, 14))
    story.append(Paragraph("TITLE OF THE PROJECT", ParagraphStyle('TP1', fontName='Times-Bold', fontSize=14, leading=18, alignment=TA_CENTER, textColor=colors.black)))
    story.append(Spacer(1, 12))
    story.append(HRFlowable(width="80%", thickness=1.5, color=C_DARK_BLUE, spaceBefore=4, spaceAfter=14, hAlign='CENTER'))
    story.append(Paragraph("PHARMACY MANAGEMENT SYSTEM", ParagraphStyle('TP2', fontName='Times-Bold', fontSize=18, leading=22, alignment=TA_CENTER, textColor=C_MAROON)))
    story.append(Spacer(1, 4))
    story.append(Paragraph("A CENTRALIZED WEB BASED ERP PLATFORM", ParagraphStyle('TP3', fontName='Times-Bold', fontSize=13, leading=17, alignment=TA_CENTER, textColor=C_MAROON)))
    story.append(HRFlowable(width="80%", thickness=1.5, color=C_DARK_BLUE, spaceBefore=14, spaceAfter=20, hAlign='CENTER'))
    story.append(Spacer(1, 10))
    
    poster_img = os.path.join(ASSETS_DIR, "project_hero_poster.jpg")
    if os.path.exists(poster_img):
        story.append(Image(poster_img, width=470, height=313))
    story.append(PageBreak())

    # ==================================================================
    # CHAPTER 1: INTRODUCTION (Body Page 1)
    # ==================================================================
    story.extend(make_chapter_header("CHAPTER 1", "INTRODUCTION"))
    
    story.append(Paragraph(
        "The <b>Pharmacy Management System</b> is a web-based application developed to simplify and manage the "
        "daily operations of pharmacies and medical stores. It provides a centralized platform where pharmacy staff "
        "can handle medicine details, inventory, billing, customer records, supplier information, and sales activities "
        "in an organized manner. The system helps maintain accurate records and makes pharmacy operations easier and more efficient.",
        style_body
    ))
    story.append(Paragraph(
        "This project aims to reduce the time-consuming manual process of managing pharmacy activities, which can lead to "
        "errors and difficulties in maintaining records. By automating inventory management, billing, and sales operations, "
        "the system improves accuracy, helps monitor medicine expiry dates, and provides better control over stock. The project "
        "demonstrates the practical implementation of web development, database management, and user-friendly design principles "
        "in building an efficient pharmacy management solution.",
        style_body
    ))
    
    story.append(Paragraph("1.1 Overview", style_h1))
    story.append(Paragraph(
        "The <b>Pharmacy Management System</b> is a modern pharmacy management platform developed to provide pharmacies "
        "with a smooth and efficient way of handling their daily operations. The system focuses on improving user experience "
        "through an intuitive interface, centralized data management, and integrated pharmacy operations. It reduces the "
        "difficulties of traditional manual procedures and helps pharmacy staff manage business activities more effectively.",
        style_body
    ))
    story.append(Paragraph(
        "The platform enables authorized users such as Owners, Managers, and Cashiers to manage medicine details, batch-wise "
        "inventory, supplier information, customer records, sales, and billing. It also provides barcode-based medicine search, "
        "GST calculations, expiry monitoring, and the First-Expire-First-Out (FEFO) mechanism for better stock management. "
        "Business intelligence dashboards help users monitor revenue, profit, sales performance, and inventory information.",
        style_body
    ))
    story.append(Paragraph(
        "To ensure controlled access and reliable operations, the system incorporates Role-Based Access Control (RBAC) "
        "and automated inventory updates. It also provides organized record keeping and easy access to important pharmacy "
        "information. This project highlights the practical implementation of web application development, database integration, "
        "and automation in modern pharmacy management.",
        style_body
    ))
    
    story.append(Paragraph("1.2 Problem Statement", style_h1))
    story.append(Paragraph(
        "Traditional methods of managing pharmacy operations are often manual, time-consuming, and inefficient. Pharmacies "
        "may rely on paper-based records or separate systems for handling medicine inventory, sales, billing, customer details, "
        "and supplier information. This creates several challenges, such as difficulty in tracking stock quantities, monitoring "
        "medicine expiry dates, managing multiple batches, calculating GST, and maintaining accurate sales records.",
        style_body
    ))
    story.append(Paragraph(
        "Manual processes are also prone to human errors, duplication of data, incorrect billing, and delays in updating inventory. "
        "Managing medicine returns, identifying low-stock items, and analyzing business performance can become difficult without "
        "a centralized system. In addition, the absence of proper access control may create security concerns related to pharmacy "
        "records and business information.",
        style_body
    ))
    story.append(Paragraph(
        "Therefore, there is a need for an integrated and reliable Pharmacy Management System that simplifies daily pharmacy "
        "operations, improves billing accuracy, provides efficient inventory management, and ensures organized and secure handling "
        "of pharmacy data.",
        style_body
    ))
    
    story.append(Paragraph("1.3 Project Objectives", style_h1))
    story.append(Paragraph(
        "By addressing these challenges, the primary goal of this project is to develop a user-friendly <b>Pharmacy Management "
        "System</b> that streamlines daily pharmacy operations and provides an efficient experience for pharmacy owners, managers, "
        "and cashiers. The system aims to automate billing and inventory management, improve stock handling, enhance data security, "
        "and reduce manual workload.",
        style_body
    ))
    story.append(Paragraph("<b>The key objectives are:</b>", style_h2))
    
    objectives_list = [
        "To improve efficiency, accuracy, inventory control, business visibility, and secure management of pharmacy operations through a centralized web-based platform.",
        "To develop an intuitive and user-friendly pharmacy management platform.",
        "To implement an interactive Point of Sale (POS) system for medicine billing.",
        "To maintain batch-wise medicine inventory and stock records efficiently.",
        "To implement FEFO (First-Expire-First-Out) for better expiry-based stock handling.",
        "To automate GST-based billing calculations and sales record management.",
        "To maintain customer information and purchase history.",
        "To monitor low-stock medicines and expiry-related risks.",
        "To provide business intelligence dashboards for revenue, profit, and sales analysis.",
        "To implement Role-Based Access Control (RBAC) for secure system access.",
        "To manage supplier information and pharmacy transactions in a centralized system.",
        "To reduce manual work, save time, and minimize operational errors.",
        "To deploy the application in a cloud-hosted environment for accessibility."
    ]
    for obj in objectives_list:
        story.append(Paragraph(f"• &nbsp;{obj}", style_bullet))
        
    story.append(Spacer(1, 8))
    story.append(Paragraph("1.4 Report Layout", style_h1))
    report_layout_list = [
        "<b>Chapter 1: Introduction</b> – Provides an overview of the Pharmacy Management System, its background, problem statement, project objectives, and overall significance. It explains the need for the system and how it helps improve traditional pharmacy operations.",
        "<b>Chapter 2: Feasibility Study</b> – Evaluates the technical, operational, and economic feasibility of the Pharmacy Management System. It also describes the hardware and software requirements needed for successful development and implementation.",
        "<b>Chapter 3: System Analysis</b> – Explores the project methodology, development approach, and system development model. It also explains the deployment process and the training and support required for effective system usage.",
        "<b>Chapter 4: System Design</b> – Explains the major modules and structural design of the system. It includes Data Flow Diagrams (DFDs) and the Entity Relationship (ER) Diagram to represent data movement, database structure, and interactions between different components.",
        "<b>Chapter 5: System Implementation</b> – Discusses the practical implementation of the Pharmacy Management System, including the technologies, programming tools, frameworks, and database operations used. It also presents important code components and application screenshots.",
        "<b>Chapter 6: System Testing</b> – Describes the testing methodologies used to verify the functionality and reliability of the application. It covers different testing approaches to identify errors, check individual modules, and ensure proper integration of system components.",
        "<b>Chapter 7: Conclusion and Future Scope</b> – Summarizes the overall project outcomes, major features, and achievements of the Pharmacy Management System. It also highlights the limitations of the current system and discusses possible future improvements and enhancements.",
        "<b>Chapter 8: References</b> – Lists the books, research papers, websites, technical documentation, and other online resources referred to during the study, design, and development of the project."
    ]
    for r_item in report_layout_list:
        story.append(Paragraph(f"• &nbsp;{r_item}", style_bullet))
    story.append(PageBreak())

    # ==================================================================
    # CHAPTER 2: FEASIBILITY STUDY
    # ==================================================================
    story.extend(make_chapter_header("CHAPTER 2", "FEASIBILITY STUDY"))
    
    story.append(Paragraph(
        "A feasibility study is conducted to evaluate the practicality and viability of implementing a proposed project. "
        "In the context of the <b>Pharmacy Management System</b>, the feasibility study examines various factors to ensure "
        "the successful development and deployment of the application. It helps determine whether the project can be effectively "
        "developed using the available resources, time, budget, and technology.",
        style_body
    ))
    
    story.append(Paragraph("2.1 Technical Feasibility:", style_h1))
    story.append(Paragraph(
        "The Pharmacy Management System is technically feasible, as it utilizes modern, reliable, and easily available "
        "web development technologies:",
        style_body
    ))
    tech_items = [
        "<b>Python:</b> Used as the primary programming language to implement the application logic and backend operations.",
        "<b>Django:</b> A Python-based web framework used to handle server-side operations, application logic, authentication, and request processing.",
        "<b>SQLite:</b> A relational database used to store medicine details, inventory records, customer information, supplier details, and sales transactions.",
        "<b>Django ORM:</b> Provides an efficient way to interact with the database and manage records using Python objects.",
        "<b>HTML5 and CSS3:</b> Used to structure and style the application pages, providing a clean and user-friendly interface.",
        "<b>Bootstrap 5:</b> Helps create responsive layouts and improve the overall design of the application.",
        "<b>JavaScript:</b> Adds interactivity and supports dynamic operations within the application.",
        "<b>AJAX:</b> Enables asynchronous data retrieval and customer-related operations without reloading the entire webpage.",
        "<b>JsBarcode and Chart.js:</b> Used for barcode generation and visual representation of business data through charts and dashboards."
    ]
    for item in tech_items:
        story.append(Paragraph(f"• &nbsp;{item}", style_bullet))
        
    story.append(Spacer(1, 6))
    story.append(Paragraph("2.2 Operational Feasibility:", style_h1))
    story.append(Paragraph(
        "Operational feasibility evaluates how well the proposed system meets the day-to-day operational requirements of "
        "users and the organization. The Pharmacy Management System is operationally feasible due to its user-friendly interface, "
        "centralized data management, and automated pharmacy operations:",
        style_body
    ))
    ops_items = [
        "<b>User-Friendly Interface:</b> The system provides a simple and interactive interface that allows pharmacy owners, managers, and cashiers to perform daily tasks easily.",
        "<b>Automated Billing:</b> The POS module simplifies medicine selection, cart management, GST calculation, and bill generation.",
        "<b>Inventory Management:</b> The system maintains batch-wise medicine records and helps monitor stock quantities and expiry dates.",
        "<b>FEFO Management:</b> The First-Expire-First-Out mechanism prioritizes medicines with earlier expiry dates to improve stock handling.",
        "<b>Customer Management:</b> Customer information and purchase history can be maintained and accessed efficiently.",
        "<b>Business Intelligence:</b> Dashboards provide useful insights into sales, revenue, profit, and inventory status.",
        "<b>Role-Based Access Control:</b> Different access permissions are provided to Owners, Managers, and Cashiers according to their responsibilities.",
        "<b>Reduced Manual Work:</b> Automated operations minimize repetitive tasks, save time, and help reduce human errors."
    ]
    for item in ops_items:
        story.append(Paragraph(f"• &nbsp;{item}", style_bullet))
        
    story.append(Paragraph(
        "These operational features ensure that the Pharmacy Management System can function effectively in a real pharmacy "
        "environment by providing an organized, reliable, and efficient solution for managing daily activities.",
        style_body
    ))
    
    story.append(Paragraph("2.3 Economic Feasibility:", style_h1))
    story.append(Paragraph(
        "Economic feasibility evaluates the financial viability of the project by considering development costs, implementation "
        "expenses, maintenance requirements, and long-term benefits. The Pharmacy Management System is economically feasible "
        "because it provides significant advantages such as reduced manual work, time savings, improved billing accuracy, "
        "efficient inventory management, and better business monitoring. These benefits make the system a cost-effective "
        "solution for pharmacy operations.",
        style_body
    ))
    story.append(Paragraph("<b>Key economic indicators include:</b>", style_h2))
    econ_items = [
        "<b>Open-Source Technologies:</b> Tools such as Python, Django, SQLite, Bootstrap, JavaScript, and supporting libraries are freely available, which significantly reduces software development costs.",
        "<b>Low Implementation Cost:</b> The system can be developed and operated using existing computers and internet facilities, reducing the need for expensive specialized hardware.",
        "<b>No Licensing Costs:</b> Since the major development technologies used in the project are open-source, recurring software licensing charges are not required.",
        "<b>Reduced Operational Expenses:</b> Automated billing, inventory tracking, and record management reduce manual effort, paperwork, and the time required for daily pharmacy activities.",
        "<b>Minimal Hardware Requirements:</b> The application can run on standard office computers without requiring high-end server hardware, making it suitable for small and medium-sized pharmacies.",
        "<b>Scalable for Future Growth:</b> The system can be upgraded with additional features and capacity as pharmacy requirements and business operations expand.",
        "<b>Low Maintenance Cost:</b> The selected technologies are widely adopted, easy to maintain, and supported by large global developer communities.",
        "<b>Reduced Paperwork Cost:</b> The system minimizes reliance on paper ledgers, printing registers, and physical archival, resulting in ongoing savings.",
        "<b>Improved Productivity:</b> Automation of billing, stock management, and customer records frees pharmacy staff to focus on customer service and patient care."
    ]
    for item in econ_items:
        story.append(Paragraph(f"• &nbsp;{item}", style_bullet))
        
    story.append(Spacer(1, 6))
    story.append(Paragraph("2.4 System Requirement:", style_h1))
    story.append(Paragraph(
        "System requirements are derived from the technical, operational, and economic feasibility study to ensure smooth "
        "development, deployment, and maintenance of the proposed platform.",
        style_body
    ))
    
    story.append(Paragraph("2.4.1 Hardware Requirements:", style_h2))
    story.append(Paragraph("To ensure smooth development and deployment of the Pharmacy Management System, the following hardware components are required:", style_body))
    
    hw_table_data = [
        [Paragraph("<b>Component</b>", style_table_header), Paragraph("<b>Specification</b>", style_table_header)],
        [Paragraph("<b>Processor</b>", style_table_cell_bold), Paragraph("Intel Core i3/i5/i7 or AMD Ryzen 3/5/7 (or higher)", style_table_cell)],
        [Paragraph("<b>RAM</b>", style_table_cell_bold), Paragraph("Minimum 4GB (8GB or above recommended for multitasking)", style_table_cell)],
        [Paragraph("<b>Storage</b>", style_table_cell_bold), Paragraph("Minimum 256GB HDD/SSD (512GB SSD recommended for rapid disk I/O)", style_table_cell)],
        [Paragraph("<b>Internet Connectivity</b>", style_table_cell_bold), Paragraph("Stable broadband connection for cloud deployment, sync, and browser access", style_table_cell)],
        [Paragraph("<b>Peripheral Hardware</b>", style_table_cell_bold), Paragraph("Standard USB/Bluetooth 1D/2D Barcode Gun, 58mm/80mm Thermal Receipt Printer", style_table_cell)],
    ]
    t_hw = Table(hw_table_data, colWidths=[CONTENT_WIDTH*0.35, CONTENT_WIDTH*0.65])
    t_hw.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_BORDER),
        ('GRID', (0,0), (-1,-1), 0.5, C_LINE),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_hw)
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("2.4.2 Software Requirements:", style_h2))
    story.append(Paragraph("The project requires frontend, backend, database technologies, and development tools for implementation:", style_body))
    
    sw_table_data = [
        [Paragraph("<b>Category</b>", style_table_header), Paragraph("<b>Software / Technology</b>", style_table_header)],
        [Paragraph("<b>Operating System</b>", style_table_cell_bold), Paragraph("Windows 10/11, Linux (Ubuntu), or macOS", style_table_cell)],
        [Paragraph("<b>Frontend Technologies</b>", style_table_cell_bold), Paragraph("HTML5, CSS3, JavaScript (ES6+), Bootstrap 5.3", style_table_cell)],
        [Paragraph("<b>Backend Technologies</b>", style_table_cell_bold), Paragraph("Django 6.0.4 Web Framework", style_table_cell)],
        [Paragraph("<b>Database</b>", style_table_cell_bold), Paragraph("SQLite (Development &amp; Lightweight Production) / PostgreSQL-ready", style_table_cell)],
        [Paragraph("<b>Programming Language</b>", style_table_cell_bold), Paragraph("Python 3.14", style_table_cell)],
        [Paragraph("<b>Object Relational Mapping (ORM)</b>", style_table_cell_bold), Paragraph("Django Native ORM", style_table_cell)],
        [Paragraph("<b>Supporting Client Libraries</b>", style_table_cell_bold), Paragraph("AJAX, Select2 (v4.1.0), JsBarcode (CODE128), Chart.js (v4.4.0)", style_table_cell)],
        [Paragraph("<b>Configuration &amp; Security</b>", style_table_cell_bold), Paragraph("python-dotenv (Environment Variable Isolation)", style_table_cell)],
        [Paragraph("<b>Development &amp; Version Control</b>", style_table_cell_bold), Paragraph("Visual Studio Code, Git, GitHub", style_table_cell)],
        [Paragraph("<b>Cloud Deployment Platform</b>", style_table_cell_bold), Paragraph("PythonAnywhere Linux PaaS (WSGI Web Server Interface)", style_table_cell)],
    ]
    t_sw = Table(sw_table_data, colWidths=[CONTENT_WIDTH*0.35, CONTENT_WIDTH*0.65])
    t_sw.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_BORDER),
        ('GRID', (0,0), (-1,-1), 0.5, C_LINE),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4.5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_sw)
    story.append(PageBreak())

    # ==================================================================
    # CHAPTER 3: SYSTEM ANALYSIS
    # ==================================================================
    story.extend(make_chapter_header("CHAPTER 3", "SYSTEM ANALYSIS"))
    
    story.append(Paragraph(
        "This chapter presents the detailed system analysis for the <b>Pharmacy Management System</b>. It explains the "
        "approach used to understand pharmacy requirements, define system functionalities, and adopt a suitable development "
        "strategy to build an efficient, reliable, and user-friendly web-based application.",
        style_body
    ))
    
    story.append(Paragraph("3.1 Methodology:", style_h1))
    story.append(Paragraph("<b>• &nbsp;Requirement Analysis:</b>", style_h2))
    story.append(Paragraph(
        "<b>o &nbsp;User Requirements:</b> The system requirements were identified based on the daily activities of pharmacy "
        "users, including Owners, Managers, and Cashiers. The main focus was on simplifying billing, inventory management, "
        "customer records, and sales operations.",
        style_bullet
    ))
    story.append(Paragraph(
        "<b>o &nbsp;Feature Prioritization:</b> System features were categorized based on operational priority and business importance:",
        style_bullet
    ))
    story.append(Paragraph(
        "<b>o &nbsp;Essential Features:</b> User Authentication, Role-Based Access Control (RBAC), Medicine Management, "
        "Batch-Wise Inventory, Point of Sale (POS) and Billing, Dynamic GST Calculation, FEFO Stock Handling, Customer Management, "
        "Supplier Management, Sales Returns, and Business Intelligence Dashboard.",
        style_bullet_sub
    ))
    story.append(Paragraph(
        "<b>o &nbsp;Supplementary Features:</b> Barcode-Based Medicine Search, Low-Stock Alerts, Expiry Monitoring, CSV Data Export, "
        "Sales Analytics, Customer Purchase History, and Cloud Deployment.",
        style_bullet_sub
    ))
    
    story.append(Paragraph("<b>• &nbsp;System Design:</b>", style_h2))
    story.append(Paragraph(
        "<b>o &nbsp;User Interface Design:</b> Page layouts and application interfaces were designed to provide a clean, "
        "responsive, and user-friendly experience for pharmacy owners, managers, and cashiers. The interface focuses on simple "
        "navigation and easy access to different pharmacy operations.",
        style_bullet
    ))
    story.append(Paragraph(
        "<b>o &nbsp;Database Design:</b> A structured relational database was designed to store medicine details, stock batches, "
        "customer records, supplier information, sales transactions, and user details. Proper relationships between database "
        "entities were established to maintain data consistency and support efficient data retrieval.",
        style_bullet
    ))
    
    story.append(Paragraph("3.2 Development Methodology:", style_h1))
    story.append(Paragraph(
        "<b>• &nbsp;User Interface Design:</b> Intuitive interface creation was performed using HTML5, CSS3, Bootstrap 5, "
        "and JavaScript to ensure smooth interaction, simple navigation, and responsive layouts. The interface provides "
        "easy access to important features such as dashboards, medicine management, billing, inventory, customer records, and sales reports.",
        style_body
    ))
    story.append(Paragraph(
        "<b>• &nbsp;Database Design:</b> SQLite is used as a relational database to create a structured database schema that "
        "efficiently manages pharmacy records including: (1) User accounts and roles; (2) Medicine details; (3) Stock batch records; "
        "(4) Customer information; (5) Supplier details; (6) Sales and billing records; (7) Sales return records; and (8) Inventory "
        "and transaction details. The database ensures organized data storage, consistency, and easy retrieval through Django ORM.",
        style_body
    ))
    story.append(Paragraph("<b>• &nbsp;Development Phases:</b>", style_h2))
    story.append(Paragraph(
        "<b>o &nbsp;Frontend Development:</b> HTML5, CSS3, Bootstrap 5, and JavaScript are used to build interactive and responsive "
        "interfaces such as login pages, dashboards, medicine management pages, POS billing screens, inventory pages, and customer management sections.",
        style_bullet
    ))
    story.append(Paragraph(
        "<b>o &nbsp;Backend Development:</b> Django handles server-side logic, user authentication, data processing, billing "
        "operations, inventory management, and role-based access control.",
        style_bullet
    ))
    story.append(Paragraph(
        "<b>o &nbsp;Database Implementation:</b> SQLite and Django ORM manage records, stock batches, customer details, supplier "
        "information, and transactions efficiently while maintaining data consistency and relational integrity.",
        style_bullet
    ))
    
    story.append(Paragraph("3.3 Development Model:", style_h1))
    story.append(Paragraph("<b>Waterfall Model:</b>", style_h2))
    story.append(Paragraph(
        "The Pharmacy Management System follows a sequential development approach, where each phase of development is completed "
        "systematically. The project requirements are identified first, followed by system design, implementation, testing, and deployment. "
        "Each stage contributes to the successful development of the application:",
        style_body
    ))
    wf_steps = [
        "<b>1. Requirement Gathering and Analysis:</b> Identify the requirements of pharmacy users, including Owners, Managers, and Cashiers. Define features such as medicine management, inventory tracking, POS billing, customer records, and sales management.",
        "<b>2. System Design:</b> Design the user interface, database structure, Data Flow Diagrams (DFDs), Entity Relationship schemas, and overall system architecture based on the identified requirements.",
        "<b>3. Implementation:</b> Develop the frontend, backend, and database components using Python, Django, SQLite, HTML, CSS, JavaScript, and Bootstrap.",
        "<b>4. Testing:</b> Test different modules, including login, billing, inventory management, sales transactions, and customer records, to identify errors and verify system functionality.",
        "<b>5. Deployment and Maintenance:</b> Deploy the application using the selected cloud hosting platform (PythonAnywhere) and provide updates, improvements, and technical support whenever required."
    ]
    for step in wf_steps:
        story.append(Paragraph(step, style_bullet))
        
    story.append(Spacer(1, 6))
    story.append(Paragraph("3.4 Deployment:", style_h1))
    story.append(Paragraph(
        "<b>Deployment Planning:</b> A structured deployment strategy is followed to ensure the smooth implementation of the "
        "Pharmacy Management System. This includes setting up the development environment, configuring the database, verifying "
        "application functionality, and preparing the final application for deployment. PythonAnywhere is used as the cloud hosting "
        "platform to make the application accessible through any standard web browser.",
        style_body
    ))
    story.append(Paragraph(
        "<b>Secure Deployment:</b> Security measures are implemented to protect pharmacy records and user accounts. These include: "
        "(1) Secure login authentication; (2) Password protection using Django's PBKDF2 algorithm; (3) Role-Based Access Control (RBAC); "
        "(4) Restricted access to sensitive administrative operations; (5) Proper database management and data protection; (6) Application "
        "testing prior to production launch; and (7) Multi-browser compatibility testing across Chrome, Firefox, Edge, and Safari.",
        style_body
    ))
    
    story.append(Paragraph("3.5 Training and User Support", style_h1))
    story.append(Paragraph(
        "<b>User Training:</b> Basic training and guidance are provided to pharmacy users, including Owners, Managers, and Cashiers, "
        "to help them operate the Pharmacy Management System effectively. Users are guided on system login, medicine catalog management, "
        "inventory handling, billing operations, customer lookup, sales returns, and viewing business reports.",
        style_body
    ))
    story.append(Paragraph(
        "<b>User Support System:</b> Technical support and guidance are provided to resolve issues related to application usage, login, "
        "billing, inventory updates, and database operations. User feedback can also be collected to identify problems, improve system "
        "usability, and introduce future enhancements.",
        style_body
    ))
    story.append(PageBreak())

    # ==================================================================
    # CHAPTER 4: SYSTEM DESIGN
    # ==================================================================
    story.extend(make_chapter_header("CHAPTER 4", "SYSTEM DESIGN"))
    
    story.append(Paragraph(
        "This chapter explains the system design of the <b>Pharmacy Management System</b>, describing the major components "
        "and modules required for the smooth functioning of the application. The design focuses on user-friendly operations, "
        "secure access, organized data management, efficient inventory handling, and automated billing processes.",
        style_body
    ))
    
    story.append(Paragraph("4.1 Module Description", style_h1))
    story.append(Paragraph(
        "The module description includes the breakdown of the system into major functional units and explains their roles "
        "within the application. Each module is designed to perform specific tasks and interact efficiently with other modules:",
        style_body
    ))
    modules_desc = [
        "<b>Login &amp; Registration:</b> Handles secure login for different users such as Owners, Managers, and Cashiers. Authentication ensures that only authorized users can access the application.",
        "<b>User Management:</b> Allows the management of user accounts, roles, and access permissions through Role-Based Access Control (RBAC).",
        "<b>Medicine Management:</b> Stores and manages medicine details such as medicine name, barcode, category, pack size, GST percentage, and minimum stock level.",
        "<b>Inventory Management:</b> Maintains batch-wise medicine stock records, including batch numbers, quantities, purchase prices, and expiry dates. It also supports FEFO-based stock handling and low-stock monitoring.",
        "<b>Report Generation Module:</b> Automatically generates operational and regulatory reports based on stock status, sales summaries, and reorder lists in standard printable formats.",
        "<b>POS &amp; Billing Module:</b> Provides an interactive Point of Sale system for medicine search, barcode input, cart management, dynamic GST calculation, and thermal bill generation.",
        "<b>Customer Management:</b> Maintains customer information, contact details, and purchase history. AJAX-based lookup helps retrieve customer information efficiently.",
        "<b>Supplier Management:</b> Stores and manages supplier details such as name, contact person, phone number, email, and address for better vendor record management.",
        "<b>Sales &amp; Returns Management:</b> Maintains sales transactions and handles medicine returns, refund calculations, and automated inventory restocking.",
        "<b>Financial &amp; Business Intelligence Module:</b> Provides dashboards and charts to monitor sales, revenue, profit, and inventory-related information for better business decisions."
    ]
    for m in modules_desc:
        story.append(Paragraph(f"• &nbsp;{m}", style_bullet))
        
    story.append(Spacer(1, 10))
    story.append(Paragraph("4.2 Data Flow Diagram", style_h1))
    story.append(Paragraph(
        "The <b>Data Flow Diagram (DFD)</b> illustrates how data moves within the Pharmacy Management System. It identifies "
        "the flow of information between users, system processes, database storage, and generated outputs. It explains how operations "
        "such as medicine management, billing, inventory updates, customer records, and sales transactions interact with one another.",
        style_body
    ))
    story.append(Spacer(1, 8))
    
    story.append(Paragraph("4.2.1 Level 0 Context DFD", style_h2))
    story.append(Paragraph(
        "The Level 0 Context Diagram represents the highest-level operational abstraction of the Pharmacy Management System, "
        "depicting boundary interactions between external entities (Customers, Pharmacy Staff, and Suppliers) and the centralized ERP platform.",
        style_body
    ))
    story.append(Spacer(1, 6))
    dfd0_img = os.path.join(ASSETS_DIR, "dfd_level_0.png")
    if os.path.exists(dfd0_img):
        story.append(make_figure_block("dfd_level_0.png", "Figure- 4.2.1: Level 0 Context Data Flow Diagram", target_width=470, max_height=300))
    story.append(PageBreak())

    # Level 1 DFD on its own dedicated page
    story.append(Paragraph("4.2.2 Level 1 Decomposition DFD", style_h1))
    story.append(Paragraph(
        "The Level 1 Data Flow Diagram decomposes the centralized ERP engine into seven primary functional processes "
        "(P1: Login &amp; User Management, P2: Medicine &amp; Inventory, P3: Billing &amp; Sales, P4: Customer &amp; Returns, "
        "P5: Purchase &amp; Supplier, P6: Reports &amp; Dashboard) and seven relational datastores (D1: Users &amp; Roles, "
        "D2: Medicine Catalog, D3: Stock Batches, D4: Sale Ledger, D5: Customer Records, D6: Return Records, D7: Supplier Details).",
        style_body
    ))
    story.append(Spacer(1, 8))
    dfd1_img = os.path.join(ASSETS_DIR, "dfd_level_1.png")
    if os.path.exists(dfd1_img):
        story.append(make_figure_block("dfd_level_1.png", "Figure- 4.2.2: Level 1 Decomposition Data Flow Diagram", target_width=470, max_height=320))
    story.append(PageBreak())

    # ER Diagram on its own dedicated page
    story.append(Paragraph("4.3 Entity Relationship (ER) Diagram", style_h1))
    story.append(Paragraph(
        "The <b>Entity Relationship (ER) Diagram</b> represents the relationships between different entities in the "
        "Pharmacy Management System, such as users, medicine catalog, stock batches, sales records, customer details, suppliers, "
        "and sales return records. It provides a clear visualization of the database structure and the associations among various "
        "entities, helping in effective database design, implementation, data organization, and management.",
        style_body
    ))
    story.append(Spacer(1, 8))
    er_img = os.path.join(ASSETS_DIR, "er_diagram.png")
    if os.path.exists(er_img):
        story.append(make_figure_block("er_diagram.png", "Figure- 4.3.1: Relational Entity Relationship (ER) Diagram", target_width=470, max_height=320))
    story.append(Spacer(1, 14))

    # Data Dictionary / Relational Schemas
    story.append(Paragraph("4.4 Database Schema &amp; Relational Data Dictionary", style_h1))
    story.append(Paragraph(
        "The relational database schema is normalized to 3NF (Third Normal Form) to eliminate data redundancy while maintaining "
        "referential integrity. The principal database tables and their structural specifications are detailed below:",
        style_body
    ))
    
    # Table specifications
    def make_schema_table(table_title, columns_data):
        rows = [[Paragraph(f"<b>{c}</b>", style_table_header) for c in ["Field Name", "Data Type", "Constraints / Description"]]]
        for f, dt, desc in columns_data:
            rows.append([Paragraph(f, style_table_cell_bold), Paragraph(dt, style_table_cell), Paragraph(desc, style_table_cell)])
        t = Table(rows, colWidths=[CONTENT_WIDTH*0.30, CONTENT_WIDTH*0.30, CONTENT_WIDTH*0.40])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), C_BORDER),
            ('GRID', (0,0), (-1,-1), 0.5, C_LINE),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
            ('LEFTPADDING', (0,0), (-1,-1), 6),
            ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ]))
        return KeepTogether([
            Paragraph(f"<b>Table Specification: {table_title}</b>", style_h2),
            Spacer(1, 3),
            t,
            Spacer(1, 8)
        ])

    story.append(make_schema_table("Medicine (Product Master Catalog)", [
        ("id", "AutoField (PK)", "Primary Key, auto-incrementing"),
        ("name", "CharField(100)", "Generic &amp; brand name of medicine"),
        ("category", "CharField(100)", "Therapeutic category (e.g. Antibiotic)"),
        ("manufacturer", "CharField(200)", "Pharmaceutical company / brand"),
        ("minimum_stock_level", "IntegerField", "Threshold for automated low-stock alert"),
        ("gst_percentage", "IntegerField", "Applicable statutory GST rate (5%, 12%, 18%)"),
        ("barcode", "CharField(100)", "Unique product barcode (CODE128/EAN)"),
        ("pack_size", "CharField(50)", "Standard packaging units (e.g. '10 Tabs')"),
    ]))
    
    story.append(make_schema_table("Stock (Batch Inventory Vault)", [
        ("id", "AutoField (PK)", "Primary Key, auto-incrementing"),
        ("medicine_id", "ForeignKey", "References Medicine.id (CASCADE)"),
        ("supplier_id", "ForeignKey", "References Supplier.id (SET_NULL)"),
        ("batch_no", "CharField(50)", "Manufacturer batch identification code"),
        ("quantity", "IntegerField", "Current available physical stock units"),
        ("purchase_price", "DecimalField(10,2)", "Cost price per pack from wholesaler"),
        ("mrp", "DecimalField(10,2)", "Maximum Retail Price (tax-inclusive)"),
        ("expiry_date", "DateField", "Product expiration date for FEFO sorting"),
        ("date_added", "DateTimeField", "Timestamp of consignment inventory entry"),
    ]))
    
    story.append(make_schema_table("Sale (Transaction Master Ledger)", [
        ("id", "AutoField (PK)", "Primary Key, auto-incrementing"),
        ("bill_no", "CharField(50)", "Unique fiscal invoice serial number"),
        ("customer_id", "ForeignKey", "References Customer.id (NULL for walk-in)"),
        ("total_price", "DecimalField(10,2)", "Final net payable amount after taxes"),
        ("payment_method", "CharField(20)", "Settlement mode (Cash, UPI, Card)"),
        ("date", "DateTimeField", "Transaction commit timestamp (auto_now_add)"),
    ]))
    story.append(PageBreak())

    # ==================================================================
    # CHAPTER 5: SYSTEM IMPLEMENTATION
    # ==================================================================
    story.extend(make_chapter_header("CHAPTER 5", "SYSTEM IMPLEMENTATION"))
    
    story.append(Paragraph(
        "This chapter explains the system implementation of the <b>Pharmacy Management System</b>, a web-based application "
        "developed to simplify and automate pharmacy operations such as medicine management, inventory tracking, billing, "
        "customer management, and sales processing. The chapter describes the technologies and tools used during development "
        "and explains how each component contributes to the successful functioning of the system.",
        style_body
    ))
    
    story.append(Paragraph("5.1 Django", style_h1))
    django_points = [
        "<b>Use Case:</b> Django is a Python-based web framework used as the backend technology for the Pharmacy Management System. It handles application logic, database operations, user authentication, and pharmacy-related functionalities.",
        "<b>MVT Architecture:</b> Django follows the Model-View-Template (MVT) architectural pattern, which separates database models, application logic, and user interface components for organized development.",
        "<b>Database Management:</b> Django ORM provides an easy way to interact with the SQLite database using Python classes and objects. It manages medicine records, stock batches, customer details, suppliers, and sales transactions.",
        "<b>Authentication:</b> Django provides built-in authentication features for user login, password management, and session handling to ensure secure access to the application.",
        "<b>URL Routing:</b> Django URL routing manages different application paths such as login, dashboard, medicine management, inventory, POS billing, customer management, and sales reports.",
        "<b>Form Handling and Validation:</b> Django supports form processing and data validation to ensure that users enter correct and meaningful information while performing pharmacy operations.",
        "<b>Security Features:</b> Django provides built-in security mechanisms such as password hashing (PBKDF2), CSRF protection, session management, and permission handling to protect application data.",
        "<b>Scalability and Maintenance:</b> Django follows a modular development structure, making the application easier to maintain, update, and extend with additional features in the future."
    ]
    for p in django_points:
        story.append(Paragraph(f"• &nbsp;{p}", style_bullet))
        
    story.append(Spacer(1, 6))
    story.append(Paragraph("5.2 HTML, CSS3, JavaScript, Bootstrap 5", style_h1))
    story.append(Paragraph(
        "HTML5, CSS3, JavaScript, and Bootstrap 5 are used to develop the frontend interface of the Pharmacy Management System. "
        "These technologies help create a user-friendly, interactive, and responsive interface for managing pharmacy operations:",
        style_body
    ))
    front_points = [
        "<b>HTML5:</b> Used to structure web pages, forms, tables, navigation menus, and dashboard elements.",
        "<b>CSS3:</b> Used to style the application, improve its visual appearance, and maintain a consistent layout across different pages.",
        "<b>JavaScript:</b> Adds interactivity to the application and handles dynamic operations such as form interactions, user actions, and data updates.",
        "<b>Bootstrap 5:</b> Provides responsive layouts, pre-designed components, buttons, forms, tables, and navigation elements for a consistent user interface.",
        "<b>Responsive Design:</b> Bootstrap helps the application adjust its layout for different screen sizes, including desktops, laptops, tablets, and smartphones.",
        "<b>AJAX Integration:</b> AJAX is used to perform asynchronous operations, such as customer phone lookup and data retrieval, without reloading the entire webpage.",
        "<b>Dynamic Search:</b> JavaScript and Select2 support interactive search and selection features, making medicine and customer lookup rapid and intuitive.",
        "<b>User Experience:</b> These frontend technologies work together to provide simple navigation and smooth interaction across all pharmacy management modules."
    ]
    for p in front_points:
        story.append(Paragraph(f"▪ &nbsp;{p}", style_bullet))
        
    story.append(Spacer(1, 6))
    story.append(Paragraph("5.3 SQLite", style_h1))
    story.append(Paragraph(
        "SQLite is a lightweight, file-based relational database management system used in the Pharmacy Management System to "
        "store and manage application data. It is integrated with Django ORM to handle database operations efficiently:",
        style_body
    ))
    sqlite_points = [
        "<b>Data Storage:</b> SQLite stores important records such as medicine details, stock batches, customer information, supplier records, sales, and return transactions.",
        "<b>Django ORM Integration:</b> Django ORM provides an easy way to create, retrieve, update, and delete database records using Python models.",
        "<b>Relational Database:</b> SQLite organizes information into structured tables and maintains relationships between different records.",
        "<b>Lightweight and Fast:</b> SQLite does not require a separate database server, making it suitable for small and medium-sized applications.",
        "<b>Data Management:</b> It supports efficient storage and retrieval of pharmacy records, helping maintain organized and consistent information.",
        "<b>Easy Configuration:</b> SQLite requires minimal setup and is integrated with Django out-of-the-box, reducing database configuration requirements.",
        "<b>Backup and Portability:</b> The database is stored in a single file (db.sqlite3), making it easy to copy, transfer, and back up.",
        "<b>Cost-Effective:</b> SQLite is open-source and freely available, reducing database licensing and hosting costs."
    ]
    for p in sqlite_points:
        story.append(Paragraph(f"▪ &nbsp;{p}", style_bullet))
        
    story.append(Spacer(1, 6))
    story.append(Paragraph("5.4 Django Authentication and Authorization", style_h1))
    story.append(Paragraph(
        "In the Pharmacy Management System, Django's built-in authentication and authorization system is used to manage user login, "
        "access permissions, and account security. It helps ensure that only authorized users can access the application and perform "
        "operations according to their assigned roles:",
        style_body
    ))
    auth_points = [
        "<b>User Authentication:</b> Django verifies user credentials during login to ensure that only registered users can access the system.",
        "<b>Password Security:</b> Django uses secure PBKDF2 password hashing techniques to protect user passwords stored in the database.",
        "<b>Session Management:</b> Django manages user sessions to maintain login status while users navigate through different pages of the application.",
        "<b>Role-Based Access Control (RBAC):</b> Different roles, such as Owner, Manager, and Cashier, are used to control access to specific pharmacy operations.",
        "<b>Authorization:</b> Django permissions help restrict access to sensitive operations and ensure that users can perform only permitted actions.",
        "<b>Secure Logout:</b> The logout functionality terminates the user's active session and prevents unauthorized access through that session.",
        "<b>CSRF Protection:</b> Django provides Cross-Site Request Forgery protection to secure forms and prevent unauthorized requests.",
        "<b>Access Control:</b> These features help protect pharmacy records, billing information, inventory details, and other critical business data."
    ]
    for p in auth_points:
        story.append(Paragraph(f"▪ &nbsp;{p}", style_bullet))
        
    story.append(Spacer(1, 6))
    story.append(Paragraph("5.5 Django ORM (Object Relational Mapping)", style_h1))
    story.append(Paragraph(
        "Django ORM (Object Relational Mapping) is a built-in feature of Django that allows developers to interact with databases "
        "using Python classes and objects instead of writing raw SQL queries manually. In the Pharmacy Management System, Django ORM "
        "is used to manage and organize application data stored in the SQLite database:",
        style_body
    ))
    orm_points = [
        "<b>Database Interaction:</b> Django ORM handles database operations such as creating, retrieving, updating, and deleting records.",
        "<b>Medicine Records:</b> It manages medicine details, categories, manufacturers, barcode information, and GST percentages.",
        "<b>Inventory Management:</b> It maintains stock batches, quantities, expiry dates, purchase prices, and supplier information.",
        "<b>Customer and Supplier Records:</b> It stores and retrieves customer details, contact information, and supplier records.",
        "<b>Sales Management:</b> Django ORM manages sales transactions, billing information, payment details, and return records.",
        "<b>Model Relationships:</b> It establishes relationships between different database tables using primary keys and foreign keys.",
        "<b>Data Validation:</b> It supports model-level validation to maintain data consistency and reduce incorrect entries.",
        "<b>Easy Maintenance:</b> Django ORM simplifies database management and makes the application easier to maintain and extend."
    ]
    for p in orm_points:
        story.append(Paragraph(f"• &nbsp;{p}", style_bullet))
    story.append(PageBreak())

    # ==================================================================
    # 5.6 CODE LISTINGS
    # ==================================================================
    story.append(Paragraph("5.6 Code Implementations", style_h1))
    story.append(Paragraph(
        "The following source code excerpts represent the actual production implementations of key frontend templates, "
        "backend view controllers, and relational database models within the Pharmacy Management System:",
        style_body
    ))
    story.append(Spacer(1, 6))
    
    # 1. Frontend Dashboard: store/templates/inventory.html
    inv_html_snippet = (
        '<!-- Frontend: Inventory Command Center -->\n'
        '<!-- Source File: store/templates/inventory.html -->\n'
        '<!DOCTYPE html>\n'
        '<html lang="en">\n'
        '<head>\n'
        '    <meta charset="UTF-8">\n'
        '    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        '    <title>Inventory Dashboard | Command Center</title>\n'
        '    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">\n'
        '    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">\n'
        '    <style>\n'
        '        body { background-color: #f8f9fa; }\n'
        '        .dashboard-header { background-color: #2c3e50; color: white; padding: 20px; border-radius: 8px; }\n'
        '        .alert-card { border-left: 5px solid; transition: transform 0.2s ease; }\n'
        '        .border-red { border-color: #dc3545; }\n'
        '        .border-yellow { border-color: #ffc107; }\n'
        '        .border-orange { border-color: #fd7e14; }\n'
        '    </style>\n'
        '</head>\n'
        '<body>\n'
        '<div class="container-fluid mt-4 px-4">\n'
        '    <div class="dashboard-header d-flex justify-content-between align-items-center flex-wrap gap-2">\n'
        '        <h2><i class="fas fa-boxes me-2"></i>Inventory Command Center</h2>\n'
        '        <div>\n'
        '            <a href="?export=po" class="btn btn-warning text-dark fw-bold">Export Reorder List</a>\n'
        '            <a href="{% url \'add_stock\' %}" class="btn btn-success fw-bold">Add Stock</a>\n'
        '            <a href="{% url \'billing\' %}" class="btn btn-outline-light">Go to POS</a>\n'
        '        </div>\n'
        '    </div>\n'
        '    <div class="row mb-4">\n'
        '        <div class="col-md-4">\n'
        '            <div class="card alert-card border-red" onclick="filterTable(\'expired\')">\n'
        '                <div class="card-body">\n'
        '                    <h5 class="text-danger fw-bold">Expired Batches</h5>\n'
        '                    <h2>{{ expired_stock|length }}</h2>\n'
        '                </div>\n'
        '            </div>\n'
        '        </div>\n'
        '    </div>\n'
        '</div>'
    )
    story.append(make_code_card(inv_html_snippet, "store/templates/inventory.html (Dashboard Interface)"))
    story.append(Spacer(1, 10))
    
    # 2. Frontend Billing: store/templates/billing.html
    billing_html_snippet = (
        '<!-- Frontend: POS Billing Terminal -->\n'
        '<!-- Source File: store/templates/billing.html -->\n'
        '<div class="row g-4">\n'
        '    <div class="col-lg-8">\n'
        '        <div class="card shadow-sm border-0">\n'
        '            <div class="pos-header d-flex justify-content-between align-items-center">\n'
        '                <h4 class="mb-0"><i class="fas fa-pills me-2"></i>New Sale</h4>\n'
        '                <span class="badge bg-light text-dark">Terminal 01</span>\n'
        '            </div>\n'
        '            <div class="card-body">\n'
        '                <!-- Hardware Barcode Gun Scanner Form -->\n'
        '                <form method="POST" action="{% url \'billing\' %}" class="mb-3">\n'
        '                    {% csrf_token %}\n'
        '                    <div class="input-group">\n'
        '                        <span class="input-group-text"><i class="fas fa-barcode"></i></span>\n'
        '                        <input type="hidden" name="action" value="scan">\n'
        '                        <input type="text" name="barcode" class="form-control"\n'
        '                               placeholder="Scan Barcode Here..." autofocus required>\n'
        '                        <button type="submit" class="btn btn-primary fw-bold">Scan</button>\n'
        '                    </div>\n'
        '                </form>\n'
        '                <!-- Dynamic Select2 Medicine Search Dropdown -->\n'
        '                <select name="medicine" id="medicine-search" class="form-select" required>\n'
        '                    <option value="">Search by Medicine Name or Salt...</option>\n'
        '                </select>\n'
        '            </div>\n'
        '        </div>\n'
        '    </div>\n'
        '</div>'
    )
    story.append(make_code_card(billing_html_snippet, "store/templates/billing.html (POS Counter)"))
    story.append(PageBreak())

    # 3. Backend Views: store/views.py
    views_snippet = (
        '# Backend Logic: Authentication & Inventory Management\n'
        '# Source File: store/views.py\n'
        'from django.shortcuts import render, redirect\n'
        'from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout\n'
        'from django.contrib import messages\n'
        'from datetime import date, timedelta\n'
        'from .models import Medicine, Stock, Sale, Customer\n\n'
        'def login_view(request):\n'
        '    if request.user.is_authenticated:\n'
        '        return redirect(\'billing\')\n'
        '    if request.method == \'POST\':\n'
        '        u = request.POST.get(\'username\')\n'
        '        p = request.POST.get(\'password\')\n'
        '        user = authenticate(request, username=u, password=p)\n'
        '        if user is not None:\n'
        '            auth_login(request, user)\n'
        '            return redirect(\'billing\')\n'
        '        messages.error(request, "Invalid username or password.")\n'
        '    return render(request, \'login.html\')\n\n'
        'def logout_view(request):\n'
        '    auth_logout(request)\n'
        '    messages.success(request, "You have been logged out safely.")\n'
        '    return redirect(\'login\')\n\n'
        'def inventory_dashboard(request):\n'
        '    is_manager = request.user.is_superuser or request.user.groups.filter(name=\'Manager\').exists()\n'
        '    if not is_manager:\n'
        '        messages.error(request, "ACCESS DENIED: Cashiers cannot view the Inventory Command Center.")\n'
        '        return redirect(\'billing\')\n'
        '    # Optimized relational query ordered by earliest expiration date (FEFO)\n'
        '    stock_items = Stock.objects.select_related(\'medicine\', \'supplier\').order_by(\'expiry_date\')\n'
        '    today = date.today()\n'
        '    expired = [s for s in stock_items if s.expiry_date and s.expiry_date < today]\n'
        '    expiring = [s for s in stock_items if s.expiry_date and today <= s.expiry_date <= today + timedelta(days=30)]\n'
        '    return render(request, \'inventory.html\', {\'stock_items\': stock_items, \'expired\': expired, \'expiring\': expiring})'
    )
    story.append(make_code_card(views_snippet, "store/views.py (Backend Controller Logic)"))
    story.append(Spacer(1, 10))
    
    # 4. Database Models: store/models.py
    models_snippet = (
        '# Database Entities & Object-Relational Models\n'
        '# Source File: store/models.py\n'
        'from django.db import models\n\n'
        'class Supplier(models.Model):\n'
        '    name = models.CharField(max_length=200)\n'
        '    contact_person = models.CharField(max_length=100)\n'
        '    phone = models.CharField(max_length=20)\n'
        '    email = models.EmailField(blank=True, null=True)\n'
        '    address = models.TextField()\n'
        '    def __str__(self): return self.name\n\n'
        'class Medicine(models.Model):\n'
        '    name = models.CharField(max_length=100)\n'
        '    category = models.CharField(max_length=100)\n'
        '    manufacturer = models.CharField(max_length=200, blank=True, null=True)\n'
        '    minimum_stock_level = models.IntegerField(default=10, help_text="Reorder threshold")\n'
        '    gst_percentage = models.IntegerField(default=12, help_text="Statutory GST rate %")\n'
        '    barcode = models.CharField(max_length=100, unique=True, null=True, blank=True)\n'
        '    pack_size = models.CharField(max_length=50, default="10 Tabs")\n'
        '    def __str__(self): return self.name\n'
        '    @property\n'
        '    def total_stock(self):\n'
        '        return sum(s.quantity for s in self.stock_set.all())'
    )
    story.append(make_code_card(models_snippet, "store/models.py (Relational Data Schema)"))
    story.append(PageBreak())

    # ==================================================================
    # 5.7 USER INTERFACE SNAPSHOTS (Curated UI Figures)
    # ==================================================================
    story.append(Paragraph("5.7 User Interface Snapshots", style_h1))
    story.append(Paragraph(
        "The following operational screenshots illustrate the functional user interfaces of the running Pharmacy Management ERP platform:",
        style_body
    ))
    story.append(Spacer(1, 6))
    
    # Snapshot 1: Home Page (POS Counter)
    story.append(make_snapshot_card("ui_pos_home.png", "HOME PAGE (POS BILLING TERMINAL)", "Figure- 5.7.1: Interactive Point of Sale (POS) Counter with Hardware Barcode Search", target_width=470, max_height=260))
    story.append(PageBreak())
    
    # Snapshot 2: Login Page
    story.append(make_snapshot_card("ui_login.png", "SECURE AUTHENTICATION PORTAL", "Figure- 5.7.2: Role-Based User Authentication & Session Login Screen", target_width=470, max_height=260))
    story.append(PageBreak())
    
    # Snapshot 3: Current Items Cart
    story.append(make_snapshot_card("ui_cart_items.png", "CURRENT ITEMS & LIVE CART PREVIEW", "Figure- 5.7.3: Dynamic POS Cart Table with Pack Sizes, Unit Prices, and Live Deletion", target_width=470, max_height=260))
    story.append(PageBreak())
    
    # Snapshot 4: Inventory Command Center
    story.append(make_snapshot_card("ui_inventory_dashboard.png", "INVENTORY COMMAND CENTER", "Figure- 5.7.4: Inventory Command Center with Color-Coded Expiry Badges and One-Click PO Export", target_width=470, max_height=260))
    story.append(PageBreak())
    
    # Snapshot 5: Return and Exchange Desk
    story.append(make_snapshot_card("ui_returns_desk.png", "RETURN AND EXCHANGE DESK", "Figure- 5.7.5: Reverse Logistics Desk with Instant Barcode Receipt Verification", target_width=470, max_height=260))
    story.append(PageBreak())
    
    # Snapshot 6: Patient Directory & CRM
    story.append(make_snapshot_card("ui_patient_crm.png", "PATIENT DIRECTORY & CRM", "Figure- 5.7.6: Patient CRM Directory with Asynchronous Phone Lookup and Purchase Histories", target_width=470, max_height=260))
    story.append(PageBreak())
    
    # Snapshot 7: Thermal Receipt
    story.append(make_snapshot_card("ui_thermal_receipt.png", "PHARMACY MANAGEMENT ERP — BILLING RECEIPT", "Figure- 5.7.7: Standard 58mm/80mm Thermal Receipt with Statutory Reverse GST Breakdown", target_width=270, max_height=340))
    story.append(PageBreak())

    # ==================================================================
    # CHAPTER 6: SYSTEM TESTING
    # ==================================================================
    story.extend(make_chapter_header("CHAPTER 6", "SYSTEM TESTING"))
    
    story.append(Paragraph(
        "This chapter outlines the testing procedures for the <b>Pharmacy Management System</b> to evaluate its functionality, "
        "accuracy, reliability, and overall performance. Testing is an important phase of software development that helps identify "
        "errors, verify system requirements, and ensure that different modules work correctly. The testing process focuses on "
        "important operations such as medicine management, inventory control, point-of-sale billing, customer management, "
        "supplier records, sales returns, and financial reporting.",
        style_body
    ))
    
    story.append(Paragraph("6.1 Testing Methodologies:", style_h1))
    story.append(Paragraph(
        "Various testing methodologies are considered for evaluating the Pharmacy Management System, including unit testing, "
        "module testing, integration testing, system testing, and acceptance testing. Each testing approach focuses on a different "
        "aspect of the application to identify potential issues and verify the correct functioning of individual components and the complete system.",
        style_body
    ))
    
    story.append(Paragraph("6.2 Testing under Various States:", style_h1))
    test_states = [
        "<b>a) System Testing:</b> System testing involves evaluating the overall functionality of the Pharmacy Management System under different operating scenarios. It focuses on verifying that all major modules, including billing, medicine inventory, stock management, customer records, supplier management, and sales analytics, work together according to the specified requirements.",
        "<b>b) Module Testing:</b> Module testing focuses on examining individual components of the application to verify their functionality. Important modules include user authentication, medicine management, inventory management, POS billing, customer management, supplier management, sales returns, and financial analytics. Each module is checked independently to identify errors and ensure that its operations produce the expected results.",
        "<b>c) Integration Testing:</b> Integration testing verifies the interaction between different modules of the Pharmacy Management System. It ensures proper data flow between the frontend interface, Django backend, and SQLite database. For example, when a medicine is sold through the billing module, the corresponding stock quantity should be automatically updated in the inventory. Similarly, sales returns and related stock restoration operations should maintain consistency between connected modules.",
        "<b>d) Acceptance Testing:</b> Acceptance testing evaluates whether the Pharmacy Management System meets the operational requirements of its intended users, such as pharmacy owners, managers, and cashiers. It focuses on practical workflows, including medicine search, barcode-based billing, invoice generation, stock monitoring, expiry tracking, and sales record management. This testing helps determine whether the application is suitable for its intended pharmacy management operations."
    ]
    for ts in test_states:
        story.append(Paragraph(ts, style_body))
        
    story.append(Spacer(1, 8))
    story.append(Paragraph("6.3 Comprehensive Test Execution Matrix:", style_h1))
    story.append(Paragraph(
        "To provide rigorous validation, formal test cases were executed across functional boundaries with documented inputs, expected outcomes, and observed statuses:",
        style_body
    ))
    
    qa_table_data = [
        [Paragraph("<b>Test Case ID</b>", style_table_header),
         Paragraph("<b>Module &amp; Feature</b>", style_table_header),
         Paragraph("<b>Input Data / Action</b>", style_table_header),
         Paragraph("<b>Expected Output</b>", style_table_header),
         Paragraph("<b>Status</b>", style_table_header)],
        
        [Paragraph("<b>TC-01</b>", style_table_cell_bold),
         Paragraph("User Login", style_table_cell),
         Paragraph("Valid credentials (Owner/Cashier)", style_table_cell),
         Paragraph("Auth successful, session created, redirect to POS", style_table_cell),
         Paragraph("<font color='green'><b>PASS</b></font>", style_table_cell)],
        
        [Paragraph("<b>TC-02</b>", style_table_cell_bold),
         Paragraph("RBAC Protection", style_table_cell),
         Paragraph("Cashier navigates to /inventory/", style_table_cell),
         Paragraph("Access Denied message, redirect to POS", style_table_cell),
         Paragraph("<font color='green'><b>PASS</b></font>", style_table_cell)],
        
        [Paragraph("<b>TC-03</b>", style_table_cell_bold),
         Paragraph("Barcode Scan", style_table_cell),
         Paragraph("Hardware gun scans 890123456789", style_table_cell),
         Paragraph("Medicine matched, batch fetched, added to cart", style_table_cell),
         Paragraph("<font color='green'><b>PASS</b></font>", style_table_cell)],
        
        [Paragraph("<b>TC-04</b>", style_table_cell_bold),
         Paragraph("FEFO Depletion", style_table_cell),
         Paragraph("Sell 5 units of multi-batch drug", style_table_cell),
         Paragraph("Earliest expiring batch deducted first", style_table_cell),
         Paragraph("<font color='green'><b>PASS</b></font>", style_table_cell)],
        
        [Paragraph("<b>TC-05</b>", style_table_cell_bold),
         Paragraph("Reverse GST", style_table_cell),
         Paragraph("MRP = ₹112.00, GST = 12%", style_table_cell),
         Paragraph("Base = ₹100.00, CGST = ₹6.00, SGST = ₹6.00", style_table_cell),
         Paragraph("<font color='green'><b>PASS</b></font>", style_table_cell)],
        
        [Paragraph("<b>TC-06</b>", style_table_cell_bold),
         Paragraph("Return Logistics", style_table_cell),
         Paragraph("Return 2 damaged units from Bill-104", style_table_cell),
         Paragraph("Restock flag checked, inventory restored +2", style_table_cell),
         Paragraph("<font color='green'><b>PASS</b></font>", style_table_cell)],
        
        [Paragraph("<b>TC-07</b>", style_table_cell_bold),
         Paragraph("Patient CRM", style_table_cell),
         Paragraph("Type 9876543210 in phone field", style_table_cell),
         Paragraph("AJAX autocompletes patient name &amp; past doctor", style_table_cell),
         Paragraph("<font color='green'><b>PASS</b></font>", style_table_cell)],
        
        [Paragraph("<b>TC-08</b>", style_table_cell_bold),
         Paragraph("Reorder PO Export", style_table_cell),
         Paragraph("Click 'Export Reorder List' button", style_table_cell),
         Paragraph("CSV file downloads with supplier contact &amp; units", style_table_cell),
         Paragraph("<font color='green'><b>PASS</b></font>", style_table_cell)],
        
        [Paragraph("<b>TC-09</b>", style_table_cell_bold),
         Paragraph("Session Security", style_table_cell),
         Paragraph("1800s idle time without user action", style_table_cell),
         Paragraph("Session expires, redirect to login page", style_table_cell),
         Paragraph("<font color='green'><b>PASS</b></font>", style_table_cell)],
        
        [Paragraph("<b>TC-10</b>", style_table_cell_bold),
         Paragraph("Mobile Viewport", style_table_cell),
         Paragraph("Resize screen to 375px (iPhone SE)", style_table_cell),
         Paragraph("Navbar toggles, cart stacks, horizontal scroll hidden", style_table_cell),
         Paragraph("<font color='green'><b>PASS</b></font>", style_table_cell)],
    ]
    t_qa = Table(qa_table_data, colWidths=[CONTENT_WIDTH*0.14, CONTENT_WIDTH*0.20, CONTENT_WIDTH*0.24, CONTENT_WIDTH*0.32, CONTENT_WIDTH*0.10])
    t_qa.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_BORDER),
        ('GRID', (0,0), (-1,-1), 0.5, C_LINE),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('ALIGN', (4,1), (4,-1), 'CENTER'),
    ]))
    story.append(t_qa)
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("Current Project Status:", style_h1))
    story.append(Paragraph(
        "The Pharmacy Management System has been fully implemented using Python 3.14 and Django 6.0.4, with SQLite as its "
        "operational relational database. The application includes major functional modules such as POS billing, medicine inventory, "
        "customer management, supplier management, sales returns, and business intelligence analytics. The testing methodologies "
        "described above provide a structured framework for evaluating the system's functionality, reliability, and correctness, "
        "confirming that all core operational modules perform reliably in production.",
        style_body
    ))
    story.append(PageBreak())

    # ==================================================================
    # CHAPTER 7: CONCLUSION AND FUTURE SCOPE
    # ==================================================================
    story.extend(make_chapter_header("CHAPTER 7", "CONCLUSION AND FUTURE SCOPE"))
    
    story.append(Paragraph(
        "This chapter presents the conclusion and future scope of the <b>Pharmacy Management System</b>.",
        style_body
    ))
    
    story.append(Paragraph("7.1 Conclusion", style_h1))
    story.append(Paragraph(
        "The <b>Pharmacy Management System</b> represents a modern and efficient solution for managing retail pharmacy operations "
        "through digital automation. The system is designed to simplify medicine management, inventory tracking, billing, customer records, "
        "supplier management, sales returns, and financial reporting using modern web technologies and database systems.",
        style_body
    ))
    story.append(Paragraph(
        "Throughout the development process, the primary objective was to create a user-friendly, centralized, and reliable platform "
        "that meets the operational requirements of pharmacy owners, managers, and cashiers. The system reduces manual paperwork, "
        "minimizes errors in record management, improves inventory monitoring, and saves valuable time in daily pharmacy operations.",
        style_body
    ))
    story.append(Paragraph(
        "The integration of POS billing, barcode-based medicine search, batch-wise stock management, expiry monitoring, and FEFO "
        "(First Expiry, First Out) inventory handling provides an organized workflow for managing medicines. The system also supports "
        "customer and supplier records, sales returns, revenue summaries, and analytical dashboards, helping users manage important "
        "pharmacy activities from a centralized platform.",
        style_body
    ))
    story.append(Paragraph(
        "The application is developed using Python and Django, with SQLite for database management and HTML, CSS, Bootstrap, and JavaScript "
        "for the frontend interface. Django authentication and role-based access provide a structured approach to managing user access "
        "and protecting application operations.",
        style_body
    ))
    story.append(Paragraph(
        "In conclusion, the <b>Pharmacy Management System</b> has the potential to transform traditional pharmacy operations into a more "
        "organized, efficient, and technology-driven digital management solution.",
        style_body
    ))
    
    story.append(Paragraph("7.2 Future Scope", style_h1))
    story.append(Paragraph(
        "The project has significant potential for future enhancement and scalability. Some possible future improvements include:",
        style_body
    ))
    
    future_points = [
        "<b>1. Prescription OCR Integration:</b> Implement Optical Character Recognition (OCR) to extract medicine information from uploaded prescriptions and reduce manual data entry.",
        "<b>2. AI-Based Demand Forecasting:</b> Use machine learning techniques to predict medicine demand based on historical sales data and seasonal disease patterns.",
        "<b>3. Mobile Application Development:</b> Develop dedicated Android and iOS native mobile applications to allow pharmacy owners and staff to monitor operations on handheld mobile devices.",
        "<b>4. Cloud Deployment and Scalability:</b> Improve cloud hosting, database management, and automatic backup facilities to support multi-terminal concurrent users across distributed store chains.",
        "<b>5. Advanced Analytics Dashboard:</b> Provide deeper visual business insights into product profit margins, brand demand trends, supplier lead times, and dead-stock depreciation.",
        "<b>6. WhatsApp and Digital Notifications:</b> Integrate WhatsApp Business API to deliver paperless PDF tax invoices, low-stock alerts, medicine dosage reminders, and automated purchase orders.",
        "<b>7. Bluetooth Thermal Receipt Printer Integration:</b> Support seamless pairing with portable 58mm/80mm Bluetooth ESC/POS printers for faster off-counter billing.",
        "<b>8. Django REST Framework (DRF) API Gateway:</b> Expose secure RESTful API endpoints for third-party hospital management integrations, mobile apps, and e-commerce inventory sync.",
        "<b>9. Database Migration to PostgreSQL:</b> Migrate from SQLite to an enterprise PostgreSQL relational cluster with connection pooling to handle enterprise-level concurrency.",
        "<b>10. Automated Cloud Backup and Disaster Recovery:</b> Implement automated daily encrypted database snapshots to cloud object storage (AWS S3) to guarantee zero data loss."
    ]
    for fp in future_points:
        story.append(Paragraph(fp, style_bullet))
        
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "These enhancements can make the Pharmacy Management System more intelligent, scalable, secure, and valuable for "
        "modern commercial retail pharmacy operations in the future.",
        style_body
    ))
    story.append(PageBreak())

    # ==================================================================
    # CHAPTER 8: REFERENCES & BIBLIOGRAPHY
    # ==================================================================
    story.extend(make_chapter_header("CHAPTER 8", "REFERENCES"))
    
    story.append(Paragraph("8.1 Books:", style_h1))
    books = [
        "1. Pressman, R. S., &amp; Maxim, B. R. (2019). <i>Software Engineering: A Practitioner's Approach</i> (9th ed.). McGraw-Hill Education.",
        "2. Elmasri, R., &amp; Navathe, S. B. (2016). <i>Fundamentals of Database Systems</i> (7th ed.). Pearson Education.",
        "3. Lutz, M. (2013). <i>Learning Python</i> (5th ed.). O'Reilly Media.",
        "4. Duckett, J. (2014). <i>HTML and CSS: Design and Build Websites</i>. Wiley Publishing.",
        "5. Duckett, J. (2014). <i>JavaScript and JQuery: Interactive Front-End Web Development</i>. Wiley Publishing."
    ]
    for b in books:
        story.append(Paragraph(b, style_bullet))
        
    story.append(Spacer(1, 8))
    story.append(Paragraph("8.2 Research Papers and Articles:", style_h1))
    papers = [
        "1. World Health Organization. (2019). <i>Good Storage and Distribution Practices for Medical Products</i>. WHO Technical Report Series No. 1025, Annex 7. Geneva: World Health Organization.",
        "2. World Health Organization. (2011). <i>Model Guidance for the Storage and Transport of Time- and Temperature-Sensitive Pharmaceutical Products</i>. WHO Technical Report Series No. 961, Annex 9. Geneva: World Health Organization.",
        "3. World Health Organization. (2011). <i>WHO Good Distribution Practices for Pharmaceutical Products</i>. WHO Technical Report Series No. 957, Annex 5. Geneva: World Health Organization."
    ]
    for p in papers:
        story.append(Paragraph(p, style_bullet))
        
    story.append(Spacer(1, 8))
    story.append(Paragraph("8.3 Websites:", style_h1))
    websites = [
        "1. Python Software Foundation. <i>Python Programming Resources and Documentation</i>. Available at: https://www.python.org/",
        "2. Django Software Foundation. <i>Django Web Framework Technical Documentation and Guides</i>. Available at: https://www.djangoproject.com/",
        "3. W3Schools. <i>HTML, CSS, JavaScript, and Bootstrap Tutorials</i>. Available at: https://www.w3schools.com/",
        "4. MDN Web Docs. <i>HTML, CSS, and Modern JavaScript Web Technologies Reference</i>. Available at: https://developer.mozilla.org/",
        "5. GeeksforGeeks. <i>Python, Database Management, and Web Development Concepts</i>. Available at: https://www.geeksforgeeks.org/",
        "6. Stack Overflow. <i>Developer Community Knowledge Base and Technical Solutions</i>. Available at: https://stackoverflow.com/"
    ]
    for w in websites:
        story.append(Paragraph(w, style_bullet))
        
    story.append(Spacer(1, 8))
    story.append(Paragraph("8.4 Online Documentation:", style_h1))
    onlines = [
        "1. Python Documentation. <i>Python Language Reference (v3.14)</i>. Available at: https://docs.python.org/3/",
        "2. Django Documentation. <i>Django Web Framework Documentation (v6.0)</i>. Available at: https://docs.djangoproject.com/",
        "3. SQLite Documentation. <i>SQLite Relational Database Architecture &amp; SQL Syntax</i>. Available at: https://www.sqlite.org/docs.html",
        "4. Bootstrap Documentation. <i>Bootstrap 5 Responsive Frontend Component Library</i>. Available at: https://getbootstrap.com/docs/5.3/",
        "5. Chart.js Documentation. <i>HTML5 Canvas Responsive Charting Library</i>. Available at: https://www.chartjs.org/docs/",
        "6. Select2 Documentation. <i>jQuery-Based Dynamic Searchable Select Box</i>. Available at: https://select2.org/",
        "7. JsBarcode Documentation. <i>Client-Side Barcode Generator for CODE128/EAN</i>. Available at: https://github.com/lindell/JsBarcode",
        "8. GitHub Documentation. <i>Git Version Control, Collaboration, and Repository Hosting</i>. Available at: https://docs.github.com/"
    ]
    for o in onlines:
        story.append(Paragraph(o, style_bullet))

    return story

# ----------------------------------------------------------------------
# MAIN BUILD SCRIPT
# ----------------------------------------------------------------------
def main():
    print(f"Building thesis project report: {OUTPUT_PDF}...")
    doc = SimpleDocTemplate(
        OUTPUT_PDF,
        pagesize=letter,
        leftMargin=LEFT_MARGIN,
        rightMargin=RIGHT_MARGIN,
        topMargin=TOP_MARGIN,
        bottomMargin=BOTTOM_MARGIN
    )
    story = build_story()
    doc.build(story, canvasmaker=AcademicReportCanvas)
    print("Report build completed successfully!")

if __name__ == '__main__':
    main()

