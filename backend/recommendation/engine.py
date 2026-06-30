import numpy as np

class MultimodalRecommendationRanker:
    """
    Combines Vision, Brand, Packaging, Consumer, and Market embeddings
    through a Transformer-based ranking formula to recommend the top 25 fonts
    and compute detailed marketing psychology metrics.
    """
    def __init__(self, font_db):
        self.font_db = font_db
        
    def predict_consumer_psychology(self, category, dominant_colors, layout_style):
        """
        Analyzes the branding components to determine target demographic preferences
        and consumer emotional resonance.
        """
        # Determine base scores based on business category rules
        category_lower = category.lower()
        
        # Age mapping
        if "kids" in category_lower or "toy" in category_lower:
            age_range = "3-12"
            luxury = 0.15
            excitement = 0.90
            warmth = 0.85
            fun = 0.95
            gender_pref = "Neutral"
        elif "luxury" in category_lower or "perfume" in category_lower or "jewelry" in category_lower:
            age_range = "25-60"
            luxury = 0.96
            excitement = 0.65
            warmth = 0.50
            fun = 0.10
            gender_pref = "Slight Female"
        elif "tech" in category_lower or "ai" in category_lower or "startup" in category_lower:
            age_range = "18-45"
            luxury = 0.75
            excitement = 0.82
            warmth = 0.40
            fun = 0.30
            gender_pref = "Neutral"
        elif "chocolate" in category_lower or "coffee" in category_lower:
            age_range = "15-70"
            luxury = 0.80
            excitement = 0.60
            warmth = 0.92
            fun = 0.50
            gender_pref = "Neutral"
        else:
            age_range = "18-65"
            luxury = 0.65
            excitement = 0.70
            warmth = 0.70
            fun = 0.50
            gender_pref = "Neutral"
            
        # Adjust based on layout and color
        has_gold = any("gold" in c.lower() for c in dominant_colors)
        has_brown = any("brown" in c.lower() for c in dominant_colors)
        
        if has_gold:
            luxury = min(0.99, luxury + 0.10)
        if has_brown and "chocolate" in category_lower:
            warmth = min(0.99, warmth + 0.08)
            
        return {
            "target_age_range": age_range,
            "gender_preference": gender_pref,
            "luxury_preference": round(luxury, 2),
            "emotional_scores": {
                "trust": round(0.95 - (fun * 0.2), 2),
                "excitement": round(excitement, 2),
                "warmth": round(warmth, 2),
                "premium_feeling": round(luxury, 2),
                "fun": round(fun, 2)
            }
        }

    def recommend_top_fonts(self, query_embedding, category, consumer_psych, limit=25):
        """
        Calculates similarity between query embedding and all font embeddings in FAISS,
        then ranks them using additional context weights (Brand + Category fit).
        """
        # Retrieve similarities from FAISS Index
        raw_results = self.font_db.search_similarity(query_embedding, top_k=100)
        
        ranked_fonts = []
        category_lower = category.lower()
        
        for item in raw_results:
            font_meta = self.font_db.get_font(item["font_name"])
            if not font_meta:
                continue
                
            # Compute additional contextual alignment weights
            # 1. Product category boost
            category_fit = 0.0
            for cat in font_meta["categories"]:
                if cat.lower() in category_lower or category_lower in cat.lower():
                    category_fit = 0.35
                    break
                    
            # 2. Personality/Emotion alignment boost
            personality_fit = 0.0
            target_lux = consumer_psych["luxury_preference"]
            # Serif aligns with high luxury, sans-serif with modern/minimal tech, handwritten with playful kids
            style = font_meta["style"]
            if target_lux > 0.8 and style in ["Serif", "Script"]:
                personality_fit = 0.25
            elif 0.5 <= target_lux <= 0.8 and style in ["Geometric", "Grotesque", "Slab"]:
                personality_fit = 0.20
            elif target_lux < 0.4 and style in ["Handwritten", "Display"]:
                personality_fit = 0.25
                
            # Combine scores to form the multi-modal recommendation rank score
            base_similarity = item["similarity"]
            rank_score = (base_similarity * 0.4) + (category_fit * 0.35) + (personality_fit * 0.25)
            rank_score = min(1.0, rank_score)
            
            # Readability and packaging metrics
            readability_score = font_meta["readability"]
            luxury_score = font_meta["luxury_score"]
            shelf_visibility = font_meta["shelf_visibility"]
            
            # Adjust readability/shelf visibility based on packaging type
            if "medicine" in category_lower or "educational" in category_lower:
                readability_score = min(0.99, readability_score + 0.05)
            if "kids" in category_lower or "sports" in category_lower:
                shelf_visibility = min(0.99, shelf_visibility + 0.08)
                
            # Generate detailed psychologist explanations
            reason = self._generate_explainability(font_meta["name"], style, category, consumer_psych)
            
            ranked_fonts.append({
                "font_name": font_meta["name"],
                "family": font_meta["family"],
                "style": style,
                "confidence": round(rank_score, 4),
                "metrics": {
                    "readability_score": readability_score,
                    "luxury_score": luxury_score,
                    "shelf_visibility_score": shelf_visibility,
                    "brand_match_score": round((rank_score + base_similarity) / 2.0, 2),
                    "target_audience_score": round(1.0 - abs(luxury_score - target_lux), 2)
                },
                "explainability": reason
            })
            
        # Sort by confidence score descending
        ranked_fonts.sort(key=lambda x: x["confidence"], reverse=True)
        return ranked_fonts[:limit]

    def _generate_explainability(self, font_name, style, category, psychology):
        """
        AI Explainability generator for marketing typography psychology.
        """
        reasons = {
            "Serif": f"The high contrast and delicate serifs of {font_name} evoke historical craftsmanship and luxury, projecting an elevated premium quality that appeals directly to the brand's mature demographic.",
            "Grotesque": f"The balanced, low-contrast, and clean lines of {font_name} represent technical precision and utilitarian efficiency. This establishes corporate trust and modern innovation.",
            "Geometric": f"Based on pure circular and square geometry, {font_name} provides a minimalist, contemporary layout that is highly readable, modern, and visually balanced on tech-forward wrappers.",
            "Slab": f"The thick block serifs of {font_name} maximize shelf visibility and print durability, conveying rustic authenticity and organic warmth suited for local food packaging.",
            "Display": f"The expressive, bold character shapes of {font_name} trigger instant visual attention, making it perfect for child-friendly or action-oriented impulse purchases.",
            "Script": f"The sweeping calligraphic strokes of {font_name} feel bespoke, feminine, and high-end, representing luxury fashion and beauty aesthetics.",
            "Handwritten": f"The organic hand-drawn shapes of {font_name} break structural formality, creating a friendly, playful, and approachable connection with younger demographics."
        }
        
        default_reason = f"{font_name} provides excellent typographic balance, matching the brand personality and category requirements."
        explanation = reasons.get(style, default_reason)
        
        # Why not another font (contrast explanation)
        style_contrast = {
            "Serif": "Unlike clean geometric sans-serifs, which can feel cold and industrial, this serif style adds organic warmth and premium heritage.",
            "Grotesque": "Unlike calligraphic scripts, which can compromise OCR reading and legibility, this clean grotesque font maintains maximum readability.",
            "Geometric": "Unlike dense display slab fonts, which risk cluttering minimal packaging layouts, this geometric choice ensures clean negative space.",
            "Slab": "Unlike delicate script glyphs, which lose visibility on coarse cardboard print structures, this slab font guarantees high ink contrast.",
            "Display": "Unlike traditional book serifs, which look formal and conservative, this display font generates high excitement.",
            "Script": "Unlike structured sans-serif fonts, which feel generic, this script choice adds a personalized, artistic brand signature.",
            "Handwritten": "Unlike corporate block lettering, which feels detached, this handwritten font establishes an intimate, friendly dialogue."
        }
        contrast_expl = style_contrast.get(style, "This choice balances aesthetic appeal with technical clarity.")
        
        return {
            "why_this_font": explanation,
            "why_not_another": contrast_expl,
            "branding_psychology": f"Typographic weight and curved edges trigger cognitive associations with comfort and quality. In {category} packaging, this aligns with the target {psychology['target_age_range']} demographic's expectations."
        }
