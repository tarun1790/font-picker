import io
import requests
import base64
from PIL import Image, ImageDraw, ImageFont

def test_upload(title, img, crop=None, preset=None):
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    b64 = f"data:image/png;base64,{base64.b64encode(buf.getvalue()).decode('utf-8')}"
    
    data = {}
    if crop:
        data.update(crop)
    if preset:
        data['preset_name'] = preset
    data['image_base64'] = b64
    
    try:
        res = requests.post("http://127.0.0.1:8000/api/v1/font/identify", data=data)
        if res.status_code == 200:
            j = res.json()
            top = j['matched_fonts'][0]
            print(f"[SUCCESS: {title}]")
            print(f"   Top Match: {top['name']} ({top['category']}) - {top['match_score']}%")
            print(f"   Style:     {j['dna']['primary_style']}")
            print(f"   Foundry:   {top['foundry']}")
            print(f"   Google Alt:{top['google_font']}")
            print("-" * 60)
        else:
            print(f"[FAIL: {title}] Status {res.status_code}: {res.text}")
    except Exception as e:
        print(f"[ERROR: {title}] {e}")

if __name__ == "__main__":
    # Test 1: Full image without crop
    im1 = Image.new('RGB', (800, 300), (20, 15, 30))
    d1 = ImageDraw.Draw(im1)
    d1.text((50, 80), "TRAFFIC MOVIE POSTER", fill=(255, 255, 255))
    test_upload("Traffic Full Image Base64", im1)
    
    # Test 2: With crop box normalized
    im2 = Image.new('RGB', (1000, 500), (240, 240, 245))
    d2 = ImageDraw.Draw(im2)
    d2.text((100, 150), "SWISS HELVETICA 1957", fill=(10, 10, 20))
    crop_data = {'crop_x': 0.05, 'crop_y': 0.10, 'crop_width': 0.90, 'crop_height': 0.70}
    test_upload("Swiss with Normalized Crop", im2, crop=crop_data)
    
    # Test 3: Raw Byte Upload via MultiPart Form
    im3 = Image.new('RGB', (600, 200), (10, 10, 10))
    ImageDraw.Draw(im3).text((30, 30), "VOGUE HAUTE COUTURE", fill=(255, 255, 255))
    b3 = io.BytesIO()
    im3.save(b3, format="PNG")
    b3.seek(0)
    res3 = requests.post("http://127.0.0.1:8000/api/v1/font/identify", files={'file': ('vogue.png', b3.getvalue(), 'image/png')})
    print("[SUCCESS: Raw Multipart File Upload]", res3.status_code, res3.json()['matched_fonts'][0]['name'])
