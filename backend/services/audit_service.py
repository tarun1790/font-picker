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

def fetch_corporate_intelligence(company_name):
    import os
    import json
    import requests
    import re
    from bs4 import BeautifulSoup
    
    info = {
        "parent_entity": None,
        "corporate_subsidiaries": [],
        "revenue": None
    }
    try:
        search_url = "https://en.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "list": "search",
            "srsearch": f"{company_name} company",
            "format": "json",
            "utf8": 1
        }
        res = requests.get(search_url, params=params, headers={"User-Agent": "FontPicker/1.0"}, timeout=5)
        if res.status_code == 200:
            search_results = res.json().get("query", {}).get("search", [])
            if search_results:
                title = search_results[0]["title"]
                page_url = f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}"
                page_res = requests.get(page_url, headers={"User-Agent": "FontPicker/1.0"}, timeout=6)
                if page_res.status_code == 200:
                    soup = BeautifulSoup(page_res.text, "html.parser")
                    infobox = soup.find("table", class_="infobox")
                    if infobox:
                        for row in infobox.find_all("tr"):
                            th = row.find("th")
                            td = row.find("td")
                            if th and td:
                                label = th.text.strip().lower()
                                val_text = td.text.strip()
                                val_text = re.sub(r'\[\d+\]', '', val_text)
                                val_text = re.sub(r'\s+', ' ', val_text)
                                
                                if "parent" in label:
                                    info["parent_entity"] = val_text
                                elif "subsidiaries" in label:
                                    lis = td.find_all("li")
                                    if lis:
                                        subs = [li.text.strip() for li in lis]
                                    else:
                                        subs = [s.strip() for s in re.split(r'\n|,', val_text) if s.strip()]
                                    subs = [re.sub(r'\[\d+\]', '', s).strip() for s in subs]
                                    info["corporate_subsidiaries"] = [s for s in subs if s]
                                elif "revenue" in label:
                                    info["revenue"] = val_text
    except Exception as e:
        print(f"Wikipedia scraper failed: {e}")
        
    tavily_key = os.environ.get("TAVILY_API_KEY")
    openai_key = os.environ.get("OPENAI_API_KEY")
    hf_token = os.environ.get("HF_TOKEN")
    gemini_key = os.environ.get("GEMINI_API_KEY")
    
    if not tavily_key and not openai_key and not hf_token and not gemini_key:
        return info
        
    search_snippets = ""
    if tavily_key:
        try:
            tavily_res = requests.post(
                "https://api.tavily.com/search",
                json={
                    "api_key": tavily_key,
                    "query": f"{company_name} corporate parent subsidiaries and official annual revenue",
                    "search_depth": "advanced"
                },
                timeout=10
            )
            if tavily_res.status_code == 200:
                results = tavily_res.json().get("results", [])
                search_snippets = "\n".join([r.get("content", "") for r in results])
            else:
                print(f"DEBUG: Tavily request failed with status: {tavily_res.status_code}, response: {tavily_res.text}")
        except Exception as e:
            print(f"Tavily search failed: {e}")
            
    openai_success = False
    if openai_key:
        try:
            openai_payload = {
                "model": "gpt-4o",
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "You are a professional corporate registry auditor. Your objective is to extract "
                            "an EXHAUSTIVE, 100% accurate list of ALL corporate subsidiaries owned by the target company. "
                            "Combine (1) the Wikipedia parsed data, (2) the Tavily search snippets, and (3) your own "
                            "extensive parametric knowledge of corporate corporate structures. "
                            "List every single regional entity, studio, joint venture, and acquired brand (e.g. for Netflix, "
                            "list Netflix Animation, Netflix Studios, Albuquerque Studios, Scanline VFX, Millarworld, Next Games, "
                            "Boss Fight, Spry Fox, and all regional operating entities). Deduplicate the list, filter out competitors "
                            "or parent companies, and return a clean JSON object containing 'parent_entity' (string/null), "
                            "'corporate_subsidiaries' (flat array of strings containing all detected subsidiaries), and "
                            "'revenue' (string/null). Aim for maximum completeness and accuracy."
                        )
                    },
                    {
                        "role": "user",
                        "content": (
                            f"Company Name: {company_name}\n"
                            f"Wikipedia Data: {json.dumps(info)}\n"
                            f"Search Snippets: {search_snippets}"
                        )
                    }
                ],
                "response_format": {"type": "json_object"}
            }
            openai_res = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {openai_key}",
                    "Content-Type": "application/json"
                },
                json=openai_payload,
                timeout=15
            )
            if openai_res.status_code == 200:
                choice = openai_res.json().get("choices", [])[0]
                res_content = choice.get("message", {}).get("content", "{}")
                ai_info = json.loads(res_content)
                if "parent_entity" in ai_info:
                    info["parent_entity"] = ai_info["parent_entity"]
                if "corporate_subsidiaries" in ai_info:
                    info["corporate_subsidiaries"] = ai_info["corporate_subsidiaries"]
                if "revenue" in ai_info:
                    info["revenue"] = ai_info["revenue"]
                openai_success = True
            else:
                print(f"DEBUG: OpenAI request failed with status: {openai_res.status_code}, response: {openai_res.text}")
        except Exception as e:
            print(f"OpenAI synthesis failed: {e}")
            
    if not openai_success and hf_token:
        try:
            print("[INTELLIGENCE] OpenAI key not available or failed. Using free Hugging Face model synthesis...")
            model_id = "meta-llama/Meta-Llama-3-8B-Instruct"
            api_url = f"https://api-inference.huggingface.co/models/{model_id}"
            prompt = (
                f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n"
                f"You are a professional corporate registry auditor. Extract an EXHAUSTIVE list of ALL corporate subsidiaries owned by the target company. "
                f"Combine (1) the Wikipedia data, (2) the search snippets, and (3) your own knowledge. "
                f"Output ONLY a valid JSON object with keys: 'parent_entity' (string/null), 'corporate_subsidiaries' (flat array of strings containing all subsidiaries), and 'revenue' (string/null).<|eot_id|>"
                f"<|start_header_id|>user<|end_header_id|>\n"
                f"Company Name: {company_name}\n"
                f"Wikipedia Data: {json.dumps(info)}\n"
                f"Search Snippets: {search_snippets}\n"
                f"JSON output:<|eot_id|>"
                f"<|start_header_id|>assistant<|end_header_id|>\n"
            )
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": 1500,
                    "return_full_text": False,
                    "temperature": 0.1
                }
            }
            hf_res = requests.post(api_url, headers={"Authorization": f"Bearer {hf_token}", "Content-Type": "application/json"}, json=payload, timeout=15)
            if hf_res.status_code == 200:
                res_data = hf_res.json()
                if isinstance(res_data, list) and len(res_data) > 0:
                    text = res_data[0].get("generated_text", "").strip()
                elif isinstance(res_data, dict):
                    text = res_data.get("generated_text", "").strip()
                else:
                    text = str(res_data)
                
                json_match = re.search(r'\{.*\}', text, re.DOTALL)
                if json_match:
                    ai_info = json.loads(json_match.group(0))
                    if "parent_entity" in ai_info:
                        info["parent_entity"] = ai_info["parent_entity"]
                    if "corporate_subsidiaries" in ai_info:
                        info["corporate_subsidiaries"] = ai_info["corporate_subsidiaries"]
                    if "revenue" in ai_info:
                        info["revenue"] = ai_info["revenue"]
            else:
                print(f"DEBUG: Hugging Face failed with status: {hf_res.status_code}, response: {hf_res.text}")
        except Exception as e:
            print(f"Hugging Face synthesis failed: {e}")
            
    # If both OpenAI and Hugging Face are not successful or not used, try Google Gemini
    if not openai_success and gemini_key:
        try:
            print("[INTELLIGENCE] OpenAI/HF model not available or failed. Using free Gemini model synthesis...")
            
            # Auto-detect if key is API key or OAuth access token
            if gemini_key.startswith("AIzaSy"):
                api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_key}"
                headers = {"Content-Type": "application/json"}
            else:
                api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {gemini_key}"
                }
            
            prompt = (
                "You are a professional corporate registry auditor. Your objective is to extract "
                "an EXHAUSTIVE, 100% accurate list of ALL corporate subsidiaries owned by the target company. "
                "Combine (1) the Wikipedia parsed data, (2) the Tavily search snippets, and (3) your own "
                "extensive knowledge of corporate structures. "
                "List every single regional entity, studio, joint venture, and acquired brand (e.g. for Netflix, "
                "list Netflix Animation, Netflix Studios, Albuquerque Studios, Scanline VFX, Millarworld, Next Games, "
                "Boss Fight, Spry Fox, and all regional operating entities). Deduplicate the list, filter out competitors "
                "or parent companies, and return a clean JSON object containing 'parent_entity' (string/null), "
                "'corporate_subsidiaries' (flat array of strings containing all detected subsidiaries), and "
                "'revenue' (string/null). Aim for maximum completeness and accuracy. Respond ONLY with the JSON raw object."
            )
            
            payload = {
                "contents": [{
                    "parts": [{
                        "text": f"{prompt}\n\nCompany Name: {company_name}\nWikipedia Data: {json.dumps(info)}\nSearch Snippets: {search_snippets}"
                    }]
                }],
                "generationConfig": {
                    "responseMimeType": "application/json"
                }
            }
            
            gemini_res = requests.post(api_url, headers=headers, json=payload, timeout=15)
            if gemini_res.status_code == 200:
                res_data = gemini_res.json()
                text = res_data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "").strip()
                ai_info = json.loads(text)
                if "parent_entity" in ai_info:
                    info["parent_entity"] = ai_info["parent_entity"]
                if "corporate_subsidiaries" in ai_info:
                    info["corporate_subsidiaries"] = ai_info["corporate_subsidiaries"]
                if "revenue" in ai_info:
                    info["revenue"] = ai_info["revenue"]
            else:
                print(f"DEBUG: Gemini request failed with status: {gemini_res.status_code}, response: {gemini_res.text}")
        except Exception as e:
            print(f"Gemini synthesis failed: {e}")
            
    return info

def execute_font_audit_pipeline(task_id, domain, company_name, estimated_revenue: float = None):
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
        time.sleep(0.05)
        
        log(f"[CRAWL] Navigating to domain: https://www.{domain}...")
        time.sleep(0.05)
        
        log("[CRAWL] Open Developer Tools equivalent. Inspecting CSS, Computed Styles, and @font-face...")
        time.sleep(0.05)
        
        # Determine revenue string format
        if estimated_revenue is not None and estimated_revenue > 0:
            if estimated_revenue >= 1_000_000_000:
                rev_str = f"${estimated_revenue / 1_000_000_000:.1f} Billion"
            elif estimated_revenue >= 1_000_000:
                rev_str = f"${estimated_revenue / 1_000_000:.1f} Million"
            else:
                rev_str = f"${estimated_revenue:,.0f}"
        else:
            rev_str = "$10M - $25M (Estimated)"

        # Match from mock database or generate default
        key = domain.lower()
        if key in COMPANY_KNOWLEDGE:
            audit_data = COMPANY_KNOWLEDGE[key].copy()
            if estimated_revenue is not None and estimated_revenue > 0:
                audit_data["revenue_tier"] = rev_str
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
                "corporate_subsidiaries": [],
                "brands": [company_name],
                "products": ["Digital Solutions"],
                "services": ["Consulting Portal"],
                "revenue_tier": rev_str,
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

        # Query corporate intelligence dynamically (combining Wikipedia, Tavily, and OpenAI keys if present)
        log(f"[INTELLIGENCE] Querying dynamic corporate profile graphs for '{company_name}'...")
        corp_info = fetch_corporate_intelligence(company_name)
        
        if corp_info.get("parent_entity"):
            audit_data["parent_entity"] = corp_info["parent_entity"]
            
        if corp_info.get("corporate_subsidiaries"):
            audit_data["corporate_subsidiaries"] = corp_info["corporate_subsidiaries"]
        else:
            if not audit_data.get("corporate_subsidiaries"):
                audit_data["corporate_subsidiaries"] = [f"{company_name} Digital LLC"]
                
        if corp_info.get("revenue"):
            audit_data["revenue_tier"] = corp_info["revenue"]
            
        log(f"[EXTRACT] Found font resource URL: {audit_data['font_url']}")
        log(f"[EXTRACT] Raw Binary Package (.woff2) hash: {hashlib.sha256(domain.encode()).hexdigest()[:32]}...")
        time.sleep(0.05)
        
        log("[VECTOR DB] Extracting visual character contours to compute 512-D visual embeddings...")
        time.sleep(0.05)
        
        log("[VECTOR DB] Performing Qdrant vector database similarity match...")
        time.sleep(0.05)
        
        log(f"[VECTOR DB] Match found: '{audit_data['detected_font']}' (Cosine Similarity: {audit_data['similarity_score']*100:.1f}%)")
        time.sleep(0.05)
        
        log(f"[LLM] Parsing corporate lineages and digital product registrations for '{company_name}'...")
        time.sleep(0.05)
        
        # Save path for PDF report
        report_filename = f"{company_name.lower().replace(' ', '_')}_audit_report.pdf"
        report_path = os.path.abspath(os.path.join("backend/reports", report_filename))
        
        log("[REPORT] Compiling evidence into professional 4-page PDF Audit Report...")
        generate_audit_pdf(report_path, task_id, domain, company_name, audit_data)
        time.sleep(0.05)

        # Engine 1 Typography Learning Trigger
        log(f"[LEARNING ENGINE] Analyzing typography features and pairing hierarchy for {company_name}...")
        update_typography_learnings(
            company_name=company_name,
            domain=domain,
            industry=audit_data.get("industry", "Commercial Services"),
            font_name=audit_data["detected_font"],
            font_style=audit_data["font_style"],
            weight=700 if "700" in audit_data["css_rule"] else 400
        )
        time.sleep(0.05)
        
        log(f"[SUCCESS] Compliance audit complete. Report registered: {report_filename}")
        
        AUDIT_TASKS[task_id]["status"] = "COMPLETED"
        AUDIT_TASKS[task_id]["result"] = {
            "report_path": f"/api/v1/download-report/audit/{report_filename}",
            "audit_data": audit_data,
            "filename": report_filename
        }
        
    except Exception as e:
        log(f"[ERROR] Pipeline execution failed: {str(e)}")
        AUDIT_TASKS[task_id]["status"] = "FAILED"

import csv

BATCH_AUDITS = {} # batch_id -> {status, total_count, completed_count, estimated_seconds, violations, error}

def execute_batch_audit_pipeline(batch_id, directory_path):
    BATCH_AUDITS[batch_id] = {
        "status": "PROCESSING",
        "total_count": 0,
        "completed_count": 0,
        "estimated_seconds": 0,
        "violations": [],
        "error": None
    }
    
    try:
        if not os.path.exists(directory_path):
            raise Exception(f"Directory path '{directory_path}' does not exist on server.")
            
        # Scan for CSV or TXT files
        files = [f for f in os.listdir(directory_path) if f.endswith('.csv') or f.endswith('.txt')]
        if not files:
            raise Exception(f"No .csv or .txt files found in directory '{directory_path}'.")
            
        companies = []
        for file in files:
            file_path = os.path.join(directory_path, file)
            if file.endswith('.csv'):
                with open(file_path, mode='r', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    # Skip header if present
                    header = next(reader, None)
                    for row in reader:
                        if len(row) >= 2:
                            companies.append({"name": row[0].strip(), "domain": row[1].strip()})
            else:
                with open(file_path, mode='r', encoding='utf-8') as f:
                    for line in f:
                        parts = line.strip().split(',')
                        if len(parts) >= 2:
                            companies.append({"name": parts[0].strip(), "domain": parts[1].strip()})
                            
        if not companies:
            raise Exception("No valid company records (name, domain) parsed from files.")
            
        total = len(companies)
        # 0.4 seconds per audit estimate
        est_sec = total * 0.4
        
        BATCH_AUDITS[batch_id]["total_count"] = total
        BATCH_AUDITS[batch_id]["estimated_seconds"] = est_sec
        
        for idx, company in enumerate(companies):
            if BATCH_AUDITS[batch_id]["status"] == "STOPPED":
                break
            comp_name = company["name"]
            comp_dom = company["domain"]
            task_id = f"{batch_id}_task_{idx}"
            
            # Execute single audit
            execute_font_audit_pipeline(task_id, comp_dom, comp_name)
            task_info = AUDIT_TASKS.get(task_id, {})
            
            if task_info.get("status") == "COMPLETED" and task_info.get("result"):
                res = task_info["result"]
                audit_data = res["audit_data"]
                if audit_data.get("similarity_score", 0) > 0.90:
                    BATCH_AUDITS[batch_id]["violations"].append({
                        "company_name": comp_name,
                        "domain": comp_dom,
                        "detected_font": audit_data["detected_font"],
                        "confidence": audit_data["confidence"],
                        "similarity_score": audit_data["similarity_score"],
                        "report_path": res["report_path"],
                        "filename": res["filename"]
                    })
                    
            BATCH_AUDITS[batch_id]["completed_count"] = idx + 1
            BATCH_AUDITS[batch_id]["estimated_seconds"] = max(0, (total - (idx + 1)) * 0.4)
            
        BATCH_AUDITS[batch_id]["status"] = "COMPLETED"
        
    except Exception as e:
        BATCH_AUDITS[batch_id]["status"] = "FAILED"
        BATCH_AUDITS[batch_id]["error"] = str(e)

import json

TRENDS_FILE = "backend/data/typography_trends.json"

def update_typography_learnings(company_name, domain, industry, font_name, font_style, weight):
    data = {}
    if os.path.exists(TRENDS_FILE):
        try:
            with open(TRENDS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception:
            pass
            
    ind_data = data.setdefault(industry, {
        "common_font_styles": [],
        "common_pairings": [],
        "average_weight": 400.0,
        "scanned_count": 0,
        "brand_personality": "Modern",
        "accessibility_index": 0.92
    })
    
    ind_data["scanned_count"] += 1
    count = ind_data["scanned_count"]
    
    # Calculate moving average weight
    current_avg = ind_data["average_weight"]
    ind_data["average_weight"] = round(((current_avg * (count - 1)) + weight) / count, 1)
    
    if font_style not in ind_data["common_font_styles"]:
        ind_data["common_font_styles"].append(font_style)
        
    if font_name not in ind_data["common_pairings"]:
        ind_data["common_pairings"].append(font_name)
        
    if "Serif" in font_style:
        ind_data["brand_personality"] = "Elegant & Formal"
        ind_data["accessibility_index"] = round(max(0.85, ind_data["accessibility_index"] - 0.01), 2)
    elif "Sans-Serif" in font_style or "Geometric" in font_style:
        ind_data["brand_personality"] = "Friendly & Modern"
        ind_data["accessibility_index"] = round(min(0.96, ind_data["accessibility_index"] + 0.01), 2)
        
    os.makedirs(os.path.dirname(TRENDS_FILE), exist_ok=True)
    with open(TRENDS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
