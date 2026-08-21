import requests
import io
from PIL import Image, ImageDraw

def test_live_api():
    img = Image.new('RGB', (800, 240), color=(15, 23, 42))
    d = ImageDraw.Draw(img)
    d.text((100, 80), "HELVETICA SWISS", fill=(248, 250, 252))
    
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_bytes = buffered.getvalue()
    
    files = {
        'file': ('poster.png', img_bytes, 'image/png')
    }
    data = {
        'crop_x': 0.05,
        'crop_y': 0.15,
        'crop_width': 0.9,
        'crop_height': 0.7
    }
    
    print("[TEST] Sending POST to http://127.0.0.1:8000/api/v1/font/identify...")
    res = requests.post("http://127.0.0.1:8000/api/v1/font/identify", files=files, data=data)
    print("HTTP Status Code:", res.status_code)
    json_data = res.json()
    print("Response JSON Status:", json_data.get("status"))
    print("Verified Presence:", json_data.get("database_presence"))
    print("Matched Font #1:", json_data.get("matched_fonts", [{}])[0].get("name"))

if __name__ == "__main__":
    test_live_api()
