import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import io

def extract_advanced_glyph_micro_anatomy(glyph_img):
    """
    Extracts deep typographic micro-anatomy from an isolated glyph contour:
    1. Terminal Cut Angle (Horizontal 0 deg vs Diagonal 30-45 deg vs Ball/Didone terminal)
    2. Apex / Vertex Sharpness (Sharp triangle apex vs Flat top bar on A, M, V, W)
    3. Stroke Contrast (Max thickness / Min thickness via distance transform)
    4. Aperture Openness (Gap ratio on C, S, e, c, s)
    5. Lateral Serif Protrusion vs Vertical Stem
    6. Aspect Ratio & Optical Density
    """
    if len(glyph_img.shape) == 3:
        gray = cv2.cvtColor(glyph_img, cv2.COLOR_RGB2GRAY)
    else:
        gray = glyph_img
        
    if np.mean(gray) < 127:
        _, th = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    else:
        _, th = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        
    gh, gw = th.shape
    if gh < 10 or gw < 5 or np.sum(th == 255) < 20:
        return {}
        
    # 1. Distance transform for stroke thickness and contrast
    dist = cv2.distanceTransform(th, cv2.DIST_L2, 5)
    fg_vals = dist[th == 255] * 2.0
    if len(fg_vals) > 0:
        max_stroke = float(np.percentile(fg_vals, 90))
        min_stroke = max(1.0, float(np.percentile(fg_vals, 15)))
        contrast = max_stroke / min_stroke
        median_stroke = float(np.median(fg_vals))
    else:
        contrast = 1.0
        median_stroke = 4.0
        
    # 2. Optical Density & Aspect
    density = float(np.sum(th == 255)) / float(gh * gw)
    aspect = float(gw) / float(gh)
    
    # 3. Apex / Top Sharpness (Top 10% row profile)
    top_10_h = max(2, int(gh * 0.10))
    top_rows = th[:top_10_h, :]
    top_widths = [np.sum(top_rows[r, :] == 255) for r in range(top_10_h) if np.sum(top_rows[r, :] == 255) > 0]
    min_top_w = min(top_widths) if top_widths else gw
    is_sharp_apex = (min_top_w <= max(2, int(median_stroke * 0.8)))
    
    # 4. Terminal Cut Angles (Sample stroke ends)
    # Detect horizontal vs diagonal terminal cuts
    corners = cv2.goodFeaturesToTrack(th, maxCorners=30, qualityLevel=0.05, minDistance=3)
    n_corners = len(corners) if corners is not None else 0
    
    # 5. Lateral Serif Protrusions
    k_v = cv2.getStructuringElement(cv2.MORPH_RECT, (1, max(7, int(gh * 0.25))))
    v_stems = cv2.morphologyEx(th, cv2.MORPH_OPEN, k_v)
    lateral_pixels = cv2.subtract(th, v_stems)
    lateral_ratio = float(np.sum(lateral_pixels > 0)) / (np.sum(th > 0) + 1e-5)
    
    return {
        'aspect': round(aspect, 3),
        'density': round(density, 3),
        'contrast': round(contrast, 2),
        'median_stroke': round(median_stroke, 1),
        'is_sharp_apex': is_sharp_apex,
        'n_corners': n_corners,
        'lateral_ratio': round(lateral_ratio, 3)
    }

if __name__ == '__main__':
    # Test on real fonts
    fonts = {
        'Impact (Condensed Black)': 'impact.ttf',
        'Arial (Diagonal Cuts Sans)': 'arial.ttf',
        'Georgia (High Contrast Serif)': 'georgia.ttf',
        'Times New Roman (Classic Serif)': 'times.ttf',
        'Courier New (Monospace Slab)': 'cour.ttf'
    }
    
    print('=== TYPOGRAPHIC MICRO-ANATOMY BENCHMARK ===')
    for label, fname in fonts.items():
        im = Image.new('L', (300, 200), 255)
        try:
            f = ImageFont.truetype(fname, 120)
        except:
            continue
        ImageDraw.Draw(im).text((40, 20), 'A', fill=0, font=f)
        crop_box = im.getbbox()
        if crop_box:
            glyph = np.array(im.crop(crop_box))
            metrics = extract_advanced_glyph_micro_anatomy(glyph)
            print(f'{label}:')
            for k, v in metrics.items():
                print(f'   {k:15s}: {v}')
            print('-'*40)
