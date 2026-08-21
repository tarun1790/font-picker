import io
import requests
from PIL import Image, ImageDraw

def test_poster(text, font_label):
    img = Image.new('RGB', (800, 240), color=(15, 23, 42))
    d = ImageDraw.Draw(img)
    d.text((100, 80), text, fill=(255, 255, 255))
    
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    
    files = {'file': ('poster.png', buf.getvalue(), 'image/png')}
    data = {'crop_x': 0.0, 'crop_y': 0.0, 'crop_width': 1.0, 'crop_height': 1.0}
    res = requests.post('http://127.0.0.1:8000/api/v1/font/identify', files=files, data=data)
    if res.status_code == 200:
        json_data = res.json()
        print(f"[TEST: {font_label}]")
        print(f"   Extracted Text: \"{json_data.get('extracted_sample_text')}\"")
        top = json_data['matched_fonts'][0]
        print(f"   Top Matched Font: {top['name']} ({top['category']}) - {top['match_score']}%")
        second = json_data['matched_fonts'][1]
        print(f"   #2 Matched Font: {second['name']} ({second['match_score']}%)")
        print("-" * 50)
    else:
        print(f"[FAIL: {font_label}] {res.status_code} - {res.text}")

if __name__ == "__main__":
    test_poster("HELVETICA SWISS 1957", "Helvetica Swiss Poster")
    test_poster("BAUHAUS DESSAU", "Bauhaus / Futura Poster")
    test_poster("HAUTE COUTURE VOGUE", "Bodoni / Vogue Poster")
    test_poster("WANTED DEAD OR ALIVE", "Clarendon Slab Poster")
    test_poster("GILL SANS LONDON", "Gill Sans Poster")
