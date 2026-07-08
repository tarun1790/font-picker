import os
import uuid
import hashlib
import time
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing, Rect, String, Line

# Enriched mock company registry matching Engine 2 specifications
COMPANY_KNOWLEDGE = {
    "cadbury.com": {
        "company_name": "Cadbury",
        "domain": "cadbury.com",
        "industry": "Food & Beverage",
        "sub_industry": "Confectionery",
        "headquarters": "Uxbridge, London, UK",
        "country": "United Kingdom",
        "parent_entity": "Mondelez International Inc.",
        "corporate_subsidiaries": ["Fry's Chocolate", "Green & Black's", "Toblerone"],
        "brands": ["Dairy Milk", "Creme Egg", "Bournville", "Roses"],
        "products": ["Chocolate Bars", "Baking Ingredients", "Beverages"],
        "services": ["Direct-to-consumer gifting portal"],
        "revenue_tier": "$36.2 Billion (Mondelez total)",
        "employees": "Approx. 80,000 global",
        "company_description": "Cadbury is a British multinational confectionery company fully owned by Mondelez International. It is the second largest confectionery brand in the world.",
        "technology_stack": "Shopify Plus, Cloudflare CDN, Google Analytics, React.js",
        "contact_info": {
            "linkedin": "linkedin.com/company/cadbury-uk",
            "website": "www.cadbury.co.uk",
            "mobile_apps": ["Cadbury Joy Deliverer (iOS)", "Chocolate Builder AR (Android)"]
        },
        # Font Detection Metrics
        "detected_font": "Playfair Display",
        "font_style": "Serif",
        "similarity_score": 0.965,
        "confidence": 0.98,
        "css_rule": "font-family: 'Playfair Display', Georgia, serif; font-weight: 700;",
        "font_url": "https://www.cadbury.com/assets/fonts/playfair-display-bold.woff2",
        "dom_elements": ["h1.brand-headline", "h2.hero-title", "button.btn-premium"],
        "license_status": "Potential Match – Human Review Required"
    },
    "starbucks.com": {
        "company_name": "Starbucks",
        "domain": "starbucks.com",
        "industry": "Food & Beverage",
        "sub_industry": "Coffeehouse Chain",
        "headquarters": "Seattle, Washington, USA",
        "country": "United States",
        "parent_entity": "Starbucks Corporation",
        "corporate_subsidiaries": ["Seattle's Best Coffee", "Teavana", "Evolution Fresh", "Ethos Water"],
        "brands": ["Starbucks Coffee", "Teavana Tea", "La Boulange Bakery"],
        "products": ["Fresh Coffee", "Beverages", "Espresso Machines", "Merchandise"],
        "services": ["Starbucks Rewards Mobile Payment Portal", "In-store Wi-Fi network"],
        "revenue_tier": "$35.9 Billion (FY2023)",
        "employees": "Approx. 381,000 global",
        "company_description": "Starbucks Corporation is an American multinational chain of coffeehouses and roastery reserves headquartered in Seattle, Washington.",
        "technology_stack": "Next.js, Microsoft Azure Cloud, Akamai Edge, Optimizely",
        "contact_info": {
            "linkedin": "linkedin.com/company/starbucks",
            "website": "www.starbucks.com",
            "mobile_apps": ["Starbucks Card & Payment App (iOS/Android)"]
        },
        # Font Detection Metrics
        "detected_font": "Montserrat",
        "font_style": "Geometric Sans-Serif",
        "similarity_score": 0.948,
        "confidence": 0.95,
        "css_rule": "font-family: 'Montserrat', sans-serif; font-weight: 500; letter-spacing: 0.5px;",
        "font_url": "https://www.starbucks.com/static/fonts/montserrat-regular.woff2",
        "dom_elements": ["nav.nav-menu-item", "span.rewards-score", "button.btn-order"],
        "license_status": "Potential Match – Human Review Required"
    }
}

AUDIT_TASKS = {} # task_id -> {status, progress_logs, result}

def generate_audit_pdf(report_path, task_id, domain, company_name, audit_data):
    """
    Generates a professional 4-page Font Compliance & Company Intelligence Report.
    """
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    doc = SimpleDocTemplate(report_path, pagesize=letter,
                            rightMargin=54, leftMargin=54, topMargin=54, bottomMargin=54)
    
    styles = getSampleStyleSheet()
    
    # Visual Design Theme
    c_primary = colors.HexColor("#4F46E5")   # Indigo
    c_secondary = colors.HexColor("#10B981") # Emerald
    c_dark = colors.HexColor("#1F2937")      # Slate 800
    c_light = colors.HexColor("#F3F4F6")     # Gray 100
    c_warn = colors.HexColor("#F59E0B")      # Amber / Orange warning
    
    style_cover_title = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=30,
        textColor=c_primary,
        spaceAfter=15
    )
    
    style_cover_subtitle = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=18,
        textColor=c_dark,
        spaceAfter=25
    )
    
    style_heading = ParagraphStyle(
        'Header1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=c_primary,
        spaceBefore=15,
        spaceAfter=8,
        keepWithNext=True
    )
    
    style_subheading = ParagraphStyle(
        'Header2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=c_secondary,
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    )
    
    style_body = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=c_dark,
        spaceAfter=8
    )
    
    story = []
    
    # ================= PAGE 1: TITLE & EXECUTIVE SUMMARY =================
    story.append(Spacer(1, 20))
    story.append(Paragraph("FONT COMPLIANCE & COMPANY INTELLIGENCE REPORT", style_cover_title))
    story.append(Paragraph(f"Audited Target Domain: {domain} ({company_name})", style_cover_subtitle))
    
    # Status Banner
    draw_banner = Drawing(500, 130)
    draw_banner.add(Rect(0, 0, 500, 110, fillColor=colors.HexColor("#FEF3C7"), strokeColor=c_warn, strokeWidth=1.5, rx=8, ry=8))
    draw_banner.add(String(20, 75, "STATUS: POTENTIAL MATCH - HUMAN REVIEW REQUIRED", fontName="Helvetica-Bold", fontSize=12, fillColor=c_warn))
    draw_banner.add(String(20, 50, f"Detected Font: {audit_data['detected_font']} ({audit_data['font_style']})", fontName="Helvetica", fontSize=9, fillColor=c_dark))
    draw_banner.add(String(20, 30, "Disclaimer: Visual similarity does not determine licensing status. Requires manual legal review.", fontName="Helvetica-Oblique", fontSize=8, fillColor=colors.HexColor("#78350F")))
    story.append(draw_banner)
    
    story.append(Spacer(1, 20))
    story.append(Paragraph("1. Executive Summary", style_heading))
    story.append(Paragraph(
        "This report was compiled by Engine 2 (Font Detection & Company Intelligence Engine) "
        "following a visual matching and corporate profiling sequence. The extraction pipeline "
        "downloaded active font headers from the target domain and cross-referenced them "
        "against the corporate database using visual embeddings and vector search. "
        "A high similarity index was recorded, triggering this manual review package.",
        style_body
    ))
    
    story.append(Spacer(1, 30))
    story.append(Paragraph(f"<b>Report Compiled:</b> {time.strftime('%Y-%m-%d %H:%M:%S GMT')}<br/><b>Task ID:</b> {task_id}<br/><b>Classifier Model:</b> ResNet-50-v4", style_body))
    story.append(PageBreak())
    
    # ================= PAGE 2: COMPANY OVERVIEW & CORPORATE STRUCTURE =================
    story.append(Paragraph("2. Corporate Intelligence & Overview", style_heading))
    story.append(Paragraph(
        "To evaluate potential billing nodes and verify corporate hierarchy, our background registry "
        "crawlers parsed parent companies, subsidiaries, active brands, and tech stacks.",
        style_body
    ))
    
    profile_table = [
        ["Attribute", "Company Profile Details"],
        ["Legal Entity Name", audit_data["company_name"]],
        ["Industry Sector", f"{audit_data['industry']} ({audit_data['sub_industry']})"],
        ["Headquarters", audit_data["headquarters"]],
        ["Parent Corporation", audit_data["parent_entity"]],
        ["Revenue Tier", audit_data["revenue_tier"]],
        ["Employees", audit_data["employees"]],
        ["Technology Stack", audit_data["technology_stack"]]
    ]
    t_profile = Table(profile_table, colWidths=[140, 360])
    t_profile.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), c_light),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('FONTSIZE', (0,0), (-1,-1), 8.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_profile)
    
    story.append(Paragraph("Subsidiary & Product Registry", style_subheading))
    story.append(Paragraph(f"<b>Subsidiaries:</b> {', '.join(audit_data['corporate_subsidiaries'])}", style_body))
    story.append(Paragraph(f"<b>Brands Coverage:</b> {', '.join(audit_data['brands'])}", style_body))
    story.append(Paragraph(f"<b>Active Digital Products:</b> {', '.join(audit_data['contact_info']['mobile_apps'])}", style_body))
    story.append(Paragraph(f"<b>Corporate LinkedIn Node:</b> {audit_data['contact_info']['linkedin']}", style_body))
    story.append(PageBreak())
    
    # ================= PAGE 3: TYPOGRAPHY ANALYSIS & EVIDENCE =================
    story.append(Paragraph("3. Technical Typography Evidence", style_heading))
    story.append(Paragraph(
        "Visual signatures matching target font-faces were extracted using WebGL framebuffers and vector databases.",
        style_body
    ))
    
    evidence_table = [
        ["Parameter", "Extracted Value / Match Coordinates"],
        ["Reference Font Match", audit_data["detected_font"]],
        ["Visual Style Profile", audit_data["font_style"]],
        ["Qdrant Similarity Score", f"{(audit_data['similarity_score'] * 100):.1f}%"],
        ["Confidence Index", f"{(audit_data['confidence'] * 100):.1f}%"],
        ["CSS Font Rule", audit_data["css_rule"]],
        ["Header Binary URL", audit_data["font_url"]],
        ["Binary Hash (SHA256)", hashlib.sha256(domain.encode()).hexdigest()[:32]],
        ["Target DOM Elements", ", ".join(audit_data["dom_elements"])],
        ["Detection Context", f"Chromium Headless / Browser Ver 124.0 / Engine Ver 2.0.4"]
    ]
    t_evidence = Table(evidence_table, colWidths=[155, 345])
    t_evidence.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_light),
        ('TEXTCOLOR', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('FONTSIZE', (0,0), (-1,-1), 8.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_evidence)
    story.append(PageBreak())
    
    # ================= PAGE 4: REVIEW NOTES & RECOMMENDATIONS =================
    story.append(Paragraph("4. Review Notes & Recommendations", style_heading))
    story.append(Paragraph(
        "<b>Legal & Compliance Review Guidance:</b><br/>"
        "Visual similarities in letter structures, letter-spacing, and line-heights are "
        "extremely high, indicating the target domain has rendered custom glyphs. However, "
        "because fonts can be embedded via legal corporate styling licenses, visual matching "
        "does not immediately constitute infringement.",
        style_body
    ))
    
    story.append(Paragraph("Audit Notes", style_subheading))
    story.append(Paragraph(
        "1. Check if the parent company <b>" + audit_data["parent_entity"] + "</b> holds a global desktop or web license covering this web property.<br/>"
        "2. Review corporate billing records to verify if any subsidiary (e.g. " + ", ".join(audit_data["corporate_subsidiaries"][:2]) + ") purchased web-font usage metrics.<br/>"
        "3. Cross-reference the identified digital products (" + audit_data["contact_info"]["mobile_apps"][0] + ") to inspect if the font binaries are packaged internally.",
        style_body
    ))
    
    story.append(Spacer(1, 15))
    story.append(Paragraph("Actionable Recommendations", style_subheading))
    story.append(Paragraph(
        "<b>Step A:</b> Connect with the corporate communications or brand management teams via " + audit_data["contact_info"]["linkedin"] + ".<br/>"
        "<b>Step B:</b> Request verification of the licensing status for font resource: " + audit_data["font_url"] + ".<br/>"
        "<b>Step C:</b> Flag status in internal registry database for follow-up audit in 90 days.",
        style_body
    ))
    
    doc.build(story)

def execute_font_audit_pipeline(task_id, domain, company_name):
    """
    Simulates the background crawl, vector DB matching, and PDF generation.
    """
    AUDIT_TASKS[task_id] = {
        "status": "PROCESSING",
        "progress_logs": [],
        "result": None
    }
    
    def log(msg):
        t_str = time.strftime("%H:%M:%S")
        AUDIT_TASKS[task_id]["progress_logs"].append(f"[{t_str}] {msg}")
        
    try:
        log("[INIT] Launching Playwright Chromium headless cluster...")
        time.sleep(1.2)
        
        log(f"[CRAWL] Navigating to domain: https://www.{domain}...")
        time.sleep(1.2)
        
        log("[CRAWL] Open Developer Tools equivalent. Inspecting CSS, Computed Styles, and @font-face...")
        time.sleep(1.2)
        
        # Match from mock database or generate default
        key = domain.lower()
        if key in COMPANY_KNOWLEDGE:
            audit_data = COMPANY_KNOWLEDGE[key]
        else:
            # Generate dynamically
            audit_data = {
                "company_name": company_name,
                "domain": domain,
                "industry": "Commercial Services",
                "sub_industry": "Professional Services",
                "headquarters": "New York, NY, USA",
                "country": "United States",
                "parent_entity": f"{company_name} Holdings Inc.",
                "corporate_subsidiaries": [f"{company_name} Digital LLC"],
                "brands": [company_name],
                "products": ["Digital Solutions"],
                "services": ["Consulting Portal"],
                "revenue_tier": "$10M - $25M (Estimated)",
                "employees": "Approx. 150",
                "company_description": f"{company_name} is a professional services organization catering to digital operations and system optimizations.",
                "technology_stack": "WordPress, Cloudflare, Google Tag Manager",
                "contact_info": {
                    "linkedin": f"linkedin.com/company/{company_name.lower().replace(' ', '')}",
                    "website": f"www.{domain}",
                    "mobile_apps": ["Customer Support Hub App"]
                },
                "detected_font": "Roboto",
                "font_style": "Sans-Serif",
                "similarity_score": 0.925,
                "confidence": 0.94,
                "css_rule": "font-family: 'Roboto', sans-serif; font-weight: 400;",
                "font_url": f"https://www.{domain}/fonts/roboto.woff2",
                "dom_elements": ["body", "p", "a.nav-link"],
                "license_status": "Potential Match – Human Review Required"
            }
            
        log(f"[EXTRACT] Found font resource URL: {audit_data['font_url']}")
        log(f"[EXTRACT] Raw Binary Package (.woff2) hash: {hashlib.sha256(domain.encode()).hexdigest()[:32]}...")
        time.sleep(1.2)
        
        log("[VECTOR DB] Extracting visual character contours to compute 512-D visual embeddings...")
        time.sleep(1.2)
        
        log("[VECTOR DB] Performing Qdrant vector database similarity match...")
        time.sleep(1.0)
        
        log(f"[VECTOR DB] Match found: '{audit_data['detected_font']}' (Cosine Similarity: {audit_data['similarity_score']*100:.1f}%)")
        time.sleep(1.0)
        
        log(f"[LLM] Parsing corporate lineages and digital product registrations for '{company_name}'...")
        time.sleep(1.2)
        
        # Save path for PDF report
        report_filename = f"{company_name.lower().replace(' ', '_')}_audit_report.pdf"
        report_path = os.path.abspath(os.path.join("backend/reports", report_filename))
        
        log("[REPORT] Compiling evidence into professional 4-page PDF Audit Report...")
        generate_audit_pdf(report_path, task_id, domain, company_name, audit_data)
        time.sleep(1.0)
        
        log(f"[SUCCESS] Compliance audit complete. Report registered: {report_filename}")
        
        AUDIT_TASKS[task_id]["status"] = "COMPLETED"
        AUDIT_TASKS[task_id]["result"] = {
            "report_path": f"/api/v1/download-report/{report_filename}",
            "audit_data": audit_data,
            "filename": report_filename
        }
        
    except Exception as e:
        log(f"[ERROR] Pipeline execution failed: {str(e)}")
        AUDIT_TASKS[task_id]["status"] = "FAILED"
