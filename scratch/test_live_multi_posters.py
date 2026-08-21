import io
import requests
from PIL import Image, ImageDraw

def test_poster_live(text, font_label, preset=None):
    img = Image.new('RGB', (800, 240), color=(15, 23, 42))
    d = ImageDraw.Draw(img)
    d.text((100, 80), text, fill=(255, 255, 255))
    
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    
    files = {'file': ('poster.png', buf.getvalue(), 'image/png')}
    data = {'crop_x': 0.0, 'crop_y': 0.0, 'crop_width': 1.0, 'crop_height': 1.0}
    if preset:
        data['preset_name'] = preset
        
    res = requests.post('http://127.0.0.1:8000/api/v1/font/identify', files=files, data=data)
    if res.status_code == 200:
        j = res.json()
        print(f"=== {font_label} ===")
        print(f"   [1] Extracted Poster Text: \"{j.get('extracted_sample_text')}\"")
        top = j['matched_fonts'][0]
        print(f"   [2] Top Matched Font:      {top['name']} ({top['category']}) - {top['match_score']}%")
        second = j['matched_fonts'][1]
        print(f"   [3] #2 Matched Font:       {second['name']} ({second['category']}) - {second['match_score']}%")
        print("-" * 65)
    else:
        print(f"[FAIL: {font_label}] {res.status_code} - {res.text}")

if __name__ == "__main__":
    test_poster_live("HELVETICA SWISS 1957", "Helvetica Swiss Poster", preset="helvetica")
    test_poster_live("BAUHAUS DESSAU", "Bauhaus / Futura Poster", preset="futura")
    test_poster_live("HAUTE COUTURE", "Bodoni Didone Poster", preset="bodoni")
    test_poster_live("WILD WEST BREWERY", "Clarendon Slab Poster", preset="clarendon")
    test_poster_live("BRITISH RAILWAYS", "Gill Sans Poster", preset="gill")
    test_poster_live("VOGUE EDITORIAL", "Vogue Magazine Poster", preset="vogue")
