import asyncio
import winocr
import cv2
import numpy as np
from PIL import Image, ImageDraw

async def test_image(text, style_name):
    img = Image.new('RGB', (800, 240), color=(15, 23, 42))
    d = ImageDraw.Draw(img)
    d.text((80, 80), text, fill=(255, 255, 255))
    
    # 1. OCR text via native Windows OCR
    res = await winocr.recognize_pil(img, 'en')
    ocr_text = res.text.strip()
    
    # 2. Geometric analysis
    gray = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    dist = cv2.distanceTransform(thresh, cv2.DIST_L2, 5)
    fg_dist = dist[thresh == 255]
    contrast = float(np.percentile(fg_dist, 90) / max(1.0, np.percentile(fg_dist, 15))) if len(fg_dist) > 0 else 1.0
    
    h_lines = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT, (7, 1)))
    v_lines = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT, (1, 7)))
    serif_ratio = np.sum(h_lines > 0) / (np.sum(v_lines > 0) + 1e-5)
    
    print(f"[{style_name}]")
    print(f"   OCR Extracted: \"{ocr_text}\"")
    print(f"   Stroke Contrast: {contrast:.2f} | Serif Ratio: {serif_ratio:.2f}")
    print("-" * 50)

async def main():
    await test_image("HELVETICA SWISS 1957", "Swiss Poster")
    await test_image("BAUHAUS DESSAU 1926", "Bauhaus Poster")
    await test_image("VOGUE HAUTE COUTURE", "Vogue Poster")
    await test_image("TIMES NEW ROMAN LONDON", "Times Poster")
    await test_image("ROCKWELL ARCHITECTURE", "Rockwell Poster")

if __name__ == "__main__":
    asyncio.run(main())
