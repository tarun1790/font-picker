import io
import sys
sys.path.insert(0, ".")
from PIL import Image, ImageDraw
from backend.services.identifier_service import identify_font_pipeline

def test_pipeline(text, label, preset=None):
    img = Image.new('RGB', (800, 240), color=(15, 23, 42))
    d = ImageDraw.Draw(img)
    d.text((100, 80), text, fill=(255, 255, 255))
    
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    
    res = identify_font_pipeline(buf.getvalue(), {'x': 0.0, 'y': 0.0, 'width': 1.0, 'height': 1.0}, preset_name=preset)
    print(f"=== {label} ===")
    print(f"   Extracted Poster Text: \"{res['extracted_sample_text']}\"")
    top = res['matched_fonts'][0]
    print(f"   Top Matched Font: {top['name']} ({top['category']}) - {top['match_score']}%")
    second = res['matched_fonts'][1]
    print(f"   #2 Matched Font:  {second['name']} ({second['category']}) - {second['match_score']}%")
    print("-" * 60)

if __name__ == "__main__":
    test_pipeline("HELVETICA SWISS 1957", "Helvetica Swiss Poster", preset="helvetica")
    test_pipeline("BAUHAUS DESSAU", "Bauhaus / Futura Poster", preset="futura")
    test_pipeline("HAUTE COUTURE", "Bodoni / Vogue Didone Poster", preset="bodoni")
    test_pipeline("WILD WEST BREWERY", "Clarendon Slab Poster", preset="clarendon")
    test_pipeline("BRITISH RAILWAYS", "Gill Sans Poster", preset="gill")
    test_pipeline("VOGUE EDITORIAL", "Vogue Magazine Poster", preset="vogue")
