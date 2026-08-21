import io
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps

def extract_tight_foreground_mask(image):
    np_img = np.array(image.convert('RGB'))
    gray = cv2.cvtColor(np_img, cv2.COLOR_RGB2GRAY)
    
    # Dual-pass adaptive thresholding for light and dark backgrounds
    if np.mean(gray) < 127:
        _, th = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    else:
        _, th = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        
    # Find bounding box of all foreground pixels
    coords = cv2.findNonZero(th)
    if coords is not None:
        x, y, w, h = cv2.boundingRect(coords)
        th_cropped = th[y:y+h, x:x+w]
        return th_cropped, w, h
    return th, th.shape[1], th.shape[0]

def compute_structural_cross_correlation(query_mask, candidate_font_file, sample_text="QUICK"):
    """
    Renders the candidate font at normalized height (120px) and computes normalized 2D correlation.
    """
    qh, qw = query_mask.shape
    if qh < 5 or qw < 5:
        return 0.0
        
    # Normalize query mask to standard height 100px
    target_h = 100
    scale = target_h / float(qh)
    target_w = max(10, int(qw * scale))
    norm_query = cv2.resize(query_mask, (target_w, target_h), interpolation=cv2.INTER_AREA)
    
    # Render candidate font
    im_cand = Image.new('L', (target_w * 2 + 100, target_h * 2), 0)
    try:
        f = ImageFont.truetype(candidate_font_file, 80)
    except:
        return 0.0
        
    ImageDraw.Draw(im_cand).text((20, 20), sample_text, fill=255, font=f)
    cand_np = np.array(im_cand)
    coords = cv2.findNonZero(cand_np)
    if coords is None:
        return 0.0
    cx, cy, cw, ch = cv2.boundingRect(coords)
    cand_cropped = cand_np[cy:cy+ch, cx:cx+cw]
    
    # Scale candidate to standard height 100px
    cand_scale = target_h / float(ch)
    cand_w = max(10, int(cw * cand_scale))
    norm_cand = cv2.resize(cand_cropped, (cand_w, target_h), interpolation=cv2.INTER_AREA)
    
    # Compare aspect ratios and cross-correlation
    aspect_diff = abs((target_w / float(target_h)) - (cand_w / float(target_h)))
    aspect_penalty = min(40.0, aspect_diff * 15.0)
    
    # Resize candidate to match query width for pixel overlap test
    aligned_cand = cv2.resize(norm_cand, (target_w, target_h), interpolation=cv2.INTER_AREA)
    
    # Intersection over Union (IoU) on binary shapes
    intersection = np.sum((norm_query > 127) & (aligned_cand > 127))
    union = np.sum((norm_query > 127) | (aligned_cand > 127)) + 1e-5
    iou = intersection / union
    
    # Template correlation
    res = cv2.matchTemplate(norm_query, aligned_cand, cv2.TM_CCOEFF_NORMED)
    corr = float(res[0][0]) if res is not None and not np.isnan(res[0][0]) else 0.0
    corr = max(0.0, corr)
    
    final_score = (iou * 60.0) + (corr * 40.0) - aspect_penalty
    return round(float(final_score), 2)

if __name__ == '__main__':
    # Test queries with real typography
    queries = [
        ('TRAFFIC', 'impact.ttf', 'Traffic Movie Logo in Impact'),
        ('HELVETICA SWISS', 'arial.ttf', 'Helvetica Swiss Poster in Arial'),
        ('THE GREAT GATSBY', 'georgia.ttf', 'The Great Gatsby in Georgia'),
        ('ACADEMIC REVIEW', 'times.ttf', 'Academic Review in Times')
    ]
    
    candidates = {
        'Impact / Compacta': 'impact.ttf',
        'Helvetica / Arial': 'arial.ttf',
        'Georgia': 'georgia.ttf',
        'Times New Roman': 'times.ttf',
        'Courier New': 'cour.ttf'
    }
    
    print('=== MULTI-FONT CROSS-CORRELATION ACCURACY TEST ===')
    for q_text, q_font, q_label in queries:
        im_q = Image.new('RGB', (800, 200), (20, 20, 30))
        try:
            f = ImageFont.truetype(q_font, 70)
        except:
            continue
        ImageDraw.Draw(im_q).text((30, 40), q_text, fill=(255, 255, 255), font=f)
        q_mask, qw, qh = extract_tight_foreground_mask(im_q)
        
        scores = []
        for c_name, c_file in candidates.items():
            sc = compute_structural_cross_correlation(q_mask, c_file, sample_text=q_text)
            scores.append((c_name, sc))
            
        scores.sort(key=lambda s: s[1], reverse=True)
        print(f'Query: {q_label}')
        for r, (name, sc) in enumerate(scores[:3]):
            print(f'   #{r+1}: {name:20s} (Structural Correlation: {sc:.1f}%)')
        print('-'*50)
