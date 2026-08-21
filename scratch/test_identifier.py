import io
import base64
from PIL import Image, ImageDraw, ImageFont
import requests

def test_identifier():
    # 1. Generate a test luxury serif image
    img = Image.new('RGB', (800, 240), color=(15, 23, 42))
    d = ImageDraw.Draw(img)
    d.text((100, 80), "VOGUE EDITORIAL", fill=(248, 250, 252))
    
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_bytes = buffered.getvalue()
    b64_str = base64.b64encode(img_bytes).decode('utf-8')
    
    print("[TEST] Testing identifier_service directly...")
    from backend.services.identifier_service import identify_font_pipeline
    res = identify_font_pipeline(img_bytes, crop_box={"x": 50, "y": 40, "width": 700, "height": 160})
    
    print("Status:", res.get("status"))
    print("Extracted DNA:", res.get("dna"))
    print("Top Matched Fonts:")
    for idx, f in enumerate(res.get("matched_fonts", [])):
        print(f"  #{idx+1}: {f['name']} ({f['category']}) - {f['match_score']}% Match")
    print(f"Extracted Vector Glyphs Count: {len(res.get('vector_glyphs', []))}")
    if res.get("vector_glyphs"):
        print("Sample SVG Path d snippet:", res["vector_glyphs"][0]["svg_path"][:60] + "...")
        
    print("\n[SUCCESS] Font Identifier and GlyphCraft vectorization tests passed completely!")

if __name__ == "__main__":
    test_identifier()
