import io
import sys
sys.path.insert(0, ".")
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def test_traffic_poster():
    img = Image.new('RGB', (800, 1100), color=(20, 15, 10))
    d = ImageDraw.Draw(img)
    
    # Draw large letters for TRAFFIC (e.g., using font if available or high-res layout)
    # Let's draw TRAFFIC
    try:
        font_large = ImageFont.truetype("arial.ttf", 90)
        font_med = ImageFont.truetype("arial.ttf", 28)
        font_small = ImageFont.truetype("arial.ttf", 16)
    except:
        font_large = font_med = font_small = None
        
    d.text((180, 350), "TRAFFIC", fill=(255, 255, 255), font=font_large)
    d.text((200, 480), "NO ONE GETS AWAY CLEAN", fill=(230, 200, 150), font=font_med)
    d.text((140, 950), "DIRECTED BY STEVEN SODERBERGH", fill=(180, 180, 180), font=font_small)
    
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    
    from backend.services.identifier_service import identify_font_pipeline
    
    res = identify_font_pipeline(buf.getvalue())
    print("=== MULTI-LAYER IDENTIFICATION RESULT ===")
    print("Primary Extracted Text:", res.get("extracted_sample_text"))
    print("Top Matched Font:", res["matched_fonts"][0]["name"], f"({res['matched_fonts'][0]['category']})")
    
    layers = res.get("detected_layers", [])
    print(f"Total Detected Layers: {len(layers)}")
    for idx, l in enumerate(layers):
        safe_role = l.get('role', '').encode('ascii', 'ignore').decode('ascii')
        print(f"  [Layer #{idx+1} - {safe_role}]: \"{l.get('extracted_text')}\" -> {l.get('matched_font', {}).get('name')}")

if __name__ == "__main__":
    test_traffic_poster()
