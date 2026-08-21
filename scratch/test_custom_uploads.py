import io
import requests
from PIL import Image, ImageDraw

def test_custom_upload(text, font_label):
    img = Image.new('RGB', (800, 240), color=(15, 23, 42))
    d = ImageDraw.Draw(img)
    d.text((100, 80), text, fill=(255, 255, 255))
    
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    
    files = {'file': ('custom_upload.png', buf.getvalue(), 'image/png')}
    data = {'crop_x': 0.0, 'crop_y': 0.0, 'crop_width': 1.0, 'crop_height': 1.0}
    # No preset provided!
    
    res = requests.post('http://127.0.0.1:8000/api/v1/font/identify', files=files, data=data)
    if res.status_code == 200:
        j = res.json()
        print(f"=== Custom Upload: {font_label} ===")
        print(f"   [1] Transcribed Text (OCR): \"{j.get('extracted_sample_text')}\"")
        top = j['matched_fonts'][0]
        print(f"   [2] Matched Typeface:       {top['name']} ({top['category']}) - {top['match_score']}%")
        second = j['matched_fonts'][1]
        print(f"   [3] #2 Candidate:           {second['name']} ({second['category']}) - {second['match_score']}%")
        print("-" * 65)
    else:
        print(f"[FAIL: {font_label}] {res.status_code} - {res.text}")

if __name__ == "__main__":
    test_custom_upload("NIKE JUST DO IT", "Nike Poster")
    test_custom_upload("STARBUCKS RESERVE", "Starbucks Poster")
    test_custom_upload("HARVARD LAW REVIEW", "Harvard Serif Poster")
