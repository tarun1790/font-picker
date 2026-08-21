import requests
import io
from PIL import Image, ImageDraw

BASE = "http://127.0.0.1:8000"

def test_endpoint(name, method, path, **kwargs):
    url = f"{BASE}{path}"
    try:
        if method == "GET":
            res = requests.get(url, **kwargs)
        else:
            res = requests.post(url, **kwargs)
            
        status = "PASSED" if res.status_code in [200, 202] else "FAILED"
        print(f"[{status}] ({res.status_code}) {name} -> {path}")
        if status == "FAILED":
            print(f"   Error: {res.text[:250]}")
        return res.status_code in [200, 202]
    except Exception as e:
        print(f"[ERROR] {name} -> {path} : {e}")
        return False

def run_full_prod_audit():
    print("================================================================")
    print("       STARTING END-TO-END PRODUCTION SYSTEM AUDIT")
    print("================================================================")
    
    passed = 0
    total = 0
    
    # 1. Health & Server Metadata
    total += 1
    if test_endpoint("Health Check", "GET", "/api/v1/health"): passed += 1
    
    total += 1
    if test_endpoint("Settings Endpoint", "GET", "/api/settings"): passed += 1
    
    total += 1
    if test_endpoint("List Fonts Catalog", "GET", "/api/v1/fonts"): passed += 1
    
    total += 1
    if test_endpoint("Knowledge Graph", "GET", "/api/v1/knowledge-graph"): passed += 1
    
    total += 1
    if test_endpoint("Font DNA Query", "GET", "/api/v1/font-dna/Helvetica"): passed += 1
    
    # 2. Brand Analysis & LLM Selector
    total += 1
    payload = {
        "brand_name": "Aura Luxury",
        "category": "Luxury Dark Chocolate",
        "colors": "Brown, Gold",
        "selected_font": "Playfair Display",
        "package_shape": "box",
        "personality": "Minimal, Modern, Premium",
        "target_age": "25-50",
        "market": "Global",
        "price_tier": "Luxury",
        "brand_values": "Craftsmanship, Elegance"
    }
    if test_endpoint("Brand Analysis Engine", "POST", "/api/v1/analyze-brand", data=payload): passed += 1
    
    # 3. Vector Similarity
    total += 1
    sim_payload = {
        "source_font": "Helvetica",
        "target_fonts": ["Arial", "Univers", "Bodoni", "Roboto"],
        "top_k": 3
    }
    if test_endpoint("Vector Font Similarity", "POST", "/api/v1/font-similarity", data={"font_name": "Helvetica", "top_k": 5}): passed += 1
    
    # 4. Font Identification & 250,000+ Registry Verification
    total += 1
    img = Image.new('RGB', (600, 200), color=(15, 23, 42))
    d = ImageDraw.Draw(img)
    d.text((50, 70), "HELVETICA NOW", fill=(255, 255, 255))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    img_bytes = buf.getvalue()
    
    files = {'file': ('poster.png', img_bytes, 'image/png')}
    form = {'crop_x': 0.0, 'crop_y': 0.0, 'crop_width': 1.0, 'crop_height': 1.0}
    if test_endpoint("Font Identification Engine (250k)", "POST", "/api/v1/font/identify", files=files, data=form): passed += 1
    
    # 5. Glyph Vectorization
    total += 1
    buf.seek(0)
    files_glyph = {'file': ('char.png', img_bytes, 'image/png')}
    if test_endpoint("Neural Glyph Vectorization", "POST", "/api/v1/font/vectorize-glyph", files=files_glyph): passed += 1
    
    # 6. Multi-Modal Typography AI Chat
    total += 1
    chat_payload = {
        "message": "Suggest a luxury serif pairing for Helvetica Now display headlines.",
        "history": []
    }
    if test_endpoint("AI Typography Chat Assistant", "POST", "/api/v1/chat", json=chat_payload): passed += 1
    
    print("================================================================")
    print(f" AUDIT COMPLETE: {passed}/{total} ENDPOINTS PASSED ({round((passed/total)*100, 1)}%)")
    print("================================================================")

if __name__ == "__main__":
    run_full_prod_audit()
