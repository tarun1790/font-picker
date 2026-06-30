from transformers import pipeline
import torch
import os

class LLMFontSelector:
    """
    Leverages a local pre-trained zero-shot classification model (Transformer LLM)
    to semantically analyze branding messages and map them to targeted typography DNA.
    """
    def __init__(self):
        # Configure GPU usage if available
        device = 0 if torch.cuda.is_available() else -1
        print(f"[LLM SELECTOR] Initializing Zero-Shot Transformer pipeline on device: {'cuda' if device == 0 else 'cpu'}")
        try:
            # We use typeform/distilbert-base-uncased-mnli, a fast and lightweight classifier (~250MB)
            # which works completely offline once cached.
            self.classifier = pipeline(
                "zero-shot-classification",
                model="typeform/distilbert-base-uncased-mnli",
                device=device
            )
        except Exception as e:
            print(f"[LLM SELECTOR] Failed to load local pipeline: {e}. Falling back to rule-based NLP classifier.")
            self.classifier = None

    def classify_subcategory(self, prompt: str, known_subcategories: list) -> str:
        """
        Uses the zero-shot LLM to semantically classify which known subcategory
        in the Design Knowledge Graph the user prompt is referring to.
        """
        if self.classifier:
            try:
                res = self.classifier(prompt, candidate_labels=known_subcategories)
                top_sub = res["labels"][0]
                confidence = float(res["scores"][0])
                print(f"[LLM SUB CLASS] Classified prompt '{prompt}' to subcategory '{top_sub}' with confidence {confidence:.2f}")
                return top_sub
            except Exception as e:
                print(f"[LLM SUB CLASS] Zero-shot subcategory classification failed: {e}")
                
        # Rule-based fallback if offline or error
        prompt_l = prompt.lower()
        if "milk" in prompt_l and ("packet" in prompt_l or "pack" in prompt_l or "carton" in prompt_l or "bag" in prompt_l or "fresh" in prompt_l or "dairy" in prompt_l):
            return "Fresh Milk Packet"
        if "chocolate" in prompt_l:
            if "dark" in prompt_l:
                return "Luxury Dark Chocolate"
            return "Kids Candy Bar"
        if "coffee" in prompt_l or "espresso" in prompt_l:
            return "Organic Espresso Blend"
        if "watch" in prompt_l or "chronograph" in prompt_l:
            return "Mechanical Chronograph"
        if "wine" in prompt_l or "cabernet" in prompt_l:
            return "Vintage Cabernet Sauvignon"
        if "energy" in prompt_l:
            return "Extreme Caffeine Energy"
        if "baby" in prompt_l or "diaper" in prompt_l:
            return "Organic Diaper Cream"
        if "supplement" in prompt_l or "brain" in prompt_l:
            return "Nootropic Brain Booster"
        if "face" in prompt_l or "cream" in prompt_l or "serum" in prompt_l:
            return "Organic Facial Serum"
            
        # Default fallback
        return "Luxury Dark Chocolate"

    def recommend_typography_style(self, prompt: str) -> dict:
        labels = ["luxury", "modern", "playful", "scientific", "natural", "vintage"]
        
        if self.classifier:
            try:
                res = self.classifier(prompt, candidate_labels=labels)
                top_label = res["labels"][0]
                confidence = float(res["scores"][0])
            except Exception as e:
                print(f"[LLM SELECTOR] Zero-shot inference failed: {e}")
                top_label = "modern"
                confidence = 0.5
        else:
            # Rule-based NLP fallback
            prompt_l = prompt.lower()
            if any(w in prompt_l for w in ["premium", "expensive", "rich", "gold", "elegance", "luxury", "dark chocolate"]):
                top_label = "luxury"
            elif any(w in prompt_l for w in ["playful", "kids", "fun", "candy", "cartoon", "milk"]):
                top_label = "playful"
            elif any(w in prompt_l for w in ["organic", "natural", "green", "bio", "skincare", "aloe"]):
                top_label = "natural"
            elif any(w in prompt_l for w in ["science", "medical", "clean", "tech", "trust", "ai", "developer"]):
                top_label = "scientific"
            elif any(w in prompt_l for w in ["retro", "classic", "vintage", "old", "heritage", "wine"]):
                top_label = "vintage"
            else:
                top_label = "modern"
            confidence = 0.85

        # Map classifications to layout DNA parameters
        style_dna = {
            "luxury": {
                "font_style": "Serif",
                "stroke_contrast": 0.85,
                "serif_angle": 0.90,
                "x_height_ratio": 0.45,
                "description": "Elegant high-contrast Serifs reflecting premium prestige & indulgence"
            },
            "modern": {
                "font_style": "Sans",
                "stroke_contrast": 0.20,
                "serif_angle": 0.00,
                "x_height_ratio": 0.65,
                "description": "Clean, spacious geometric Sans-Serif reflecting forward innovation & simplicity"
            },
            "playful": {
                "font_style": "Display",
                "stroke_contrast": 0.30,
                "serif_angle": 0.10,
                "x_height_ratio": 0.55,
                "description": "Energetic handwritten & friendly rounded fonts displaying fun & accessibility"
            },
            "scientific": {
                "font_style": "Monospace",
                "stroke_contrast": 0.10,
                "serif_angle": 0.00,
                "x_height_ratio": 0.60,
                "description": "Data-oriented monospace & structured sans reflecting technical trust & precision"
            },
            "natural": {
                "font_style": "Sans",
                "stroke_contrast": 0.40,
                "serif_angle": 0.20,
                "x_height_ratio": 0.58,
                "description": "Soft humanist Sans-Serif and clean layouts conveying organic purity & calmness"
            },
            "vintage": {
                "font_style": "Serif",
                "stroke_contrast": 0.60,
                "serif_angle": 0.70,
                "x_height_ratio": 0.48,
                "description": "Traditional book style serifs projecting retro craft heritage & depth"
            }
        }
        
        selected = style_dna[top_label].copy()
        selected["confidence"] = confidence
        selected["label"] = top_label
        return selected
