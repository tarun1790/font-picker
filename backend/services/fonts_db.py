import numpy as np
import random
from backend.vectordb.faiss_index import FontFAISSRegistry

# Seed random generation for reproducible mock embeddings
random.seed(42)
np.random.seed(42)

# Standard template of premium and popular fonts
FONT_TEMPLATES = [
    # Serif Fonts
    {"name": "Playfair Display", "family": "Playfair Display", "style": "Serif", "categories": ["Chocolate", "Perfume", "Jewelry", "Luxury Watch", "Fashion"], "personality": ["Luxury", "Premium", "Elegant", "Vintage"], "target_age": "25-60", "luxury_score": 0.95, "readability": 0.82, "shelf_visibility": 0.88, "multilingual": ["English", "Hindi"]},
    {"name": "Cinzel Decorative", "family": "Cinzel", "style": "Serif", "categories": ["Perfume", "Jewelry", "Luxury Watch", "Wine"], "personality": ["Luxury", "Traditional", "Elegant"], "target_age": "30-65", "luxury_score": 0.98, "readability": 0.65, "shelf_visibility": 0.92, "multilingual": ["English"]},
    {"name": "Merriweather", "family": "Merriweather", "style": "Serif", "categories": ["Medicine", "Educational", "Government", "Financial"], "personality": ["Traditional", "Corporate", "Scientific", "Premium"], "target_age": "20-70", "luxury_score": 0.75, "readability": 0.95, "shelf_visibility": 0.70, "multilingual": ["English", "Hindi", "Korean"]},
    {"name": "Lora", "family": "Lora", "style": "Serif", "categories": ["Beauty", "Cosmetics", "Cafe", "Restaurant"], "personality": ["Elegant", "Modern", "Organic", "Friendly"], "target_age": "18-50", "luxury_score": 0.82, "readability": 0.90, "shelf_visibility": 0.75, "multilingual": ["English", "Japanese"]},
    {"name": "Times New Roman", "family": "Times New Roman", "style": "Serif", "categories": ["Government", "Financial", "Educational", "Legal"], "personality": ["Traditional", "Corporate", "Academic"], "target_age": "15-90", "luxury_score": 0.70, "readability": 0.94, "shelf_visibility": 0.75, "multilingual": ["English", "Arabic"]},
    {"name": "Georgia", "family": "Georgia", "style": "Serif", "categories": ["News", "Publishing", "Financial", "Luxury Watch"], "personality": ["Traditional", "Elegant", "Premium"], "target_age": "20-80", "luxury_score": 0.80, "readability": 0.96, "shelf_visibility": 0.78, "multilingual": ["English"]},
    {"name": "Garamond", "family": "Garamond", "style": "Serif", "categories": ["Books", "Wine", "Publishing"], "personality": ["Traditional", "Elegant", "Vintage"], "target_age": "25-80", "luxury_score": 0.90, "readability": 0.93, "shelf_visibility": 0.70, "multilingual": ["English"]},
    {"name": "Didot", "family": "Didot", "style": "Serif", "categories": ["Luxury Fashion", "Perfume", "Jewelry"], "personality": ["Luxury", "Premium", "Elegant"], "target_age": "25-65", "luxury_score": 0.98, "readability": 0.72, "shelf_visibility": 0.94, "multilingual": ["English"]},
    
    # Sans-Serif / Grotesque
    {"name": "Inter", "family": "Inter", "style": "Grotesque", "categories": ["Technology", "AI Startup", "Electronics", "Financial", "Healthcare"], "personality": ["Minimal", "Modern", "Corporate", "Scientific"], "target_age": "15-50", "luxury_score": 0.78, "readability": 0.98, "shelf_visibility": 0.85, "multilingual": ["English", "Hindi", "Japanese", "Chinese", "Arabic", "Korean", "Tamil", "Telugu", "Kannada", "Malayalam"]},
    {"name": "Roboto", "family": "Roboto", "style": "Grotesque", "categories": ["Technology", "Medical", "Government", "Educational"], "personality": ["Modern", "Minimal", "Corporate"], "target_age": "10-75", "luxury_score": 0.60, "readability": 0.97, "shelf_visibility": 0.80, "multilingual": ["English", "Hindi", "Japanese", "Chinese", "Korean"]},
    {"name": "Montserrat", "family": "Montserrat", "style": "Geometric", "categories": ["Sports", "Automotive", "Gaming", "Streetwear", "Beverage"], "personality": ["Modern", "Playful", "Premium", "Friendly"], "target_age": "12-40", "luxury_score": 0.84, "readability": 0.92, "shelf_visibility": 0.89, "multilingual": ["English", "Hindi", "Arabic"]},
    {"name": "Space Grotesk", "family": "Space Grotesk", "style": "Grotesque", "categories": ["AI Startup", "Gaming", "Technology", "Streetwear"], "personality": ["Modern", "Minimal", "Playful", "Scientific"], "target_age": "15-35", "luxury_score": 0.70, "readability": 0.90, "shelf_visibility": 0.88, "multilingual": ["English"]},
    {"name": "Arial", "family": "Arial", "style": "Grotesque", "categories": ["Corporate", "Government", "Financial", "Educational"], "personality": ["Neutral", "Modern", "Corporate"], "target_age": "5-80", "luxury_score": 0.50, "readability": 0.95, "shelf_visibility": 0.80, "multilingual": ["English", "Hindi", "Japanese"]},
    {"name": "Helvetica", "family": "Helvetica", "style": "Grotesque", "categories": ["Automotive", "Technology", "Electronics", "Streetwear"], "personality": ["Minimal", "Modern", "Corporate"], "target_age": "10-75", "luxury_score": 0.85, "readability": 0.98, "shelf_visibility": 0.90, "multilingual": ["English", "Japanese"]},
    {"name": "Verdana", "family": "Verdana", "style": "Grotesque", "categories": ["Electronics", "E-commerce", "Technology"], "personality": ["Modern", "Minimal", "Legible"], "target_age": "5-80", "luxury_score": 0.45, "readability": 0.98, "shelf_visibility": 0.85, "multilingual": ["English"]},
    {"name": "Calibri", "family": "Calibri", "style": "Grotesque", "categories": ["Office", "Corporate", "Financial"], "personality": ["Modern", "Friendly", "Neutral"], "target_age": "8-80", "luxury_score": 0.40, "readability": 0.96, "shelf_visibility": 0.75, "multilingual": ["English"]},
    
    # Geometric / Slab
    {"name": "Futura", "family": "Futura", "style": "Geometric", "categories": ["Automotive", "Fashion", "Sports", "Electronics", "AI Startup"], "personality": ["Minimal", "Modern", "Premium"], "target_age": "18-55", "luxury_score": 0.90, "readability": 0.93, "shelf_visibility": 0.90, "multilingual": ["English", "Chinese"]},
    {"name": "Century Gothic", "family": "Century Gothic", "style": "Geometric", "categories": ["Cosmetics", "Beauty", "Advertising"], "personality": ["Modern", "Minimal", "Premium"], "target_age": "12-50", "luxury_score": 0.82, "readability": 0.91, "shelf_visibility": 0.88, "multilingual": ["English"]},
    {"name": "Arvo", "family": "Arvo", "style": "Slab", "categories": ["Chocolate", "Coffee", "Restaurant", "Cafe"], "personality": ["Traditional", "Organic", "Friendly", "Vintage"], "target_age": "20-60", "luxury_score": 0.68, "readability": 0.88, "shelf_visibility": 0.82, "multilingual": ["English"]},
    {"name": "Rockwell", "family": "Rockwell", "style": "Slab", "categories": ["Sports", "Automotive", "Government"], "personality": ["Traditional", "Corporate", "Premium"], "target_age": "25-65", "luxury_score": 0.75, "readability": 0.86, "shelf_visibility": 0.85, "multilingual": ["English"]},
    {"name": "Courier New", "family": "Courier New", "style": "Slab", "categories": ["Coding", "Scriptwriting", "Government"], "personality": ["Brutalist", "Traditional", "Technical"], "target_age": "15-70", "luxury_score": 0.30, "readability": 0.90, "shelf_visibility": 0.70, "multilingual": ["English"]},
    
    # Display / Script / Handmade
    {"name": "Lobster", "family": "Lobster", "style": "Display", "categories": ["Ice Cream", "Cafe", "Toy", "Beverage"], "personality": ["Playful", "Friendly", "Kids", "Vintage"], "target_age": "5-45", "luxury_score": 0.40, "readability": 0.70, "shelf_visibility": 0.95, "multilingual": ["English", "Arabic"]},
    {"name": "Impact", "family": "Impact", "style": "Display", "categories": ["Meme", "Sports", "Advertisements"], "personality": ["Playful", "Energy", "Bold"], "target_age": "10-45", "luxury_score": 0.20, "readability": 0.65, "shelf_visibility": 0.99, "multilingual": ["English"]},
    {"name": "Great Vibes", "family": "Great Vibes", "style": "Script", "categories": ["Perfume", "Beauty", "Jewelry", "Cosmetics"], "personality": ["Elegant", "Luxury", "Vintage"], "target_age": "25-60", "luxury_score": 0.95, "readability": 0.50, "shelf_visibility": 0.78, "multilingual": ["English"]},
    {"name": "Pacifico", "family": "Pacifico", "style": "Handwritten", "categories": ["Chocolate", "Ice Cream", "Cafe", "Restaurant"], "personality": ["Playful", "Friendly", "Organic"], "target_age": "5-35", "luxury_score": 0.35, "readability": 0.72, "shelf_visibility": 0.90, "multilingual": ["English"]},
    {"name": "Comic Sans", "family": "Comic Neue", "style": "Handwritten", "categories": ["Toy", "Kids", "Educational"], "personality": ["Kids", "Playful", "Friendly"], "target_age": "3-15", "luxury_score": 0.10, "readability": 0.85, "shelf_visibility": 0.80, "multilingual": ["English"]}
]

class FontMetadataDatabase:
    """
    Simulates a rich database of 50,000+ fonts (scaled here with 1,024 fully attribute-tagged open source fonts).
    Maintains a FAISS registry and calculates DNA mappings.
    """
    def __init__(self):
        self.fonts = {} # Font Name -> Meta Dict
        self.registry = FontFAISSRegistry(dimension=1024)
        self._initialize_database()
        
    def _initialize_database(self):
        styles = ["Serif", "Grotesque", "Geometric", "Slab", "Display", "Script", "Handwritten"]
        prefixes = ["Aileron", "Alegreya", "Almarai", "Amiri", "Arimo", "Assistant", "Barlow", "Cabin", "Cairo", "Chivo", 
                    "Cormorant", "Crimson", "DM Sans", "Didot", "Exo", "Fira", "Heebo", "Jost", "Kanit", "Lato", 
                    "Manrope", "Maven", "Merriweather", "Mukta", "Nanum", "Nunito", "Overpass", "PT Sans", "Playfair", 
                    "Prata", "Quicksand", "Rubik", "Sarabun", "Sen", "Teko", "Ubuntu", "Varela", "Work Sans", "Yantramanav", "Zilla"]
        variations = ["Pro", "Elite", "Standard", "Neue", "Sans", "Serif", "Slab", "Display", "Grotesk", "Geometric", 
                      "Humanist", "Variable", "Color", "SVG", "OpenType", "COLRv1"]
                      
        total_fonts = 100000
        print(f"[FONTS DATABASE] Ingesting {total_fonts} fonts into FAISS index...")
        
        # Bulk generate embeddings matrix for extreme speed
        embeddings_matrix = np.random.normal(0.0, 0.1, (total_fonts, 1024)).astype(np.float32)
        
        for i in range(total_fonts):
            if i < len(FONT_TEMPLATES):
                base = FONT_TEMPLATES[i]
                name = base["name"]
                style = base["style"]
                categories = base["categories"]
                personality = base["personality"]
                target_age = base["target_age"]
                lux_val = base["luxury_score"]
                read_val = base["readability"]
                vis_val = base["shelf_visibility"]
                multilingual = base["multilingual"]
            else:
                base = random.choice(FONT_TEMPLATES)
                name = f"{random.choice(prefixes)} {random.choice(variations)} {i}"
                style = base['style']
                categories = base["categories"]
                personality = base["personality"]
                target_age = base["target_age"]
                lux_val = base["luxury_score"] + random.uniform(-0.1, 0.1)
                read_val = base["readability"] + random.uniform(-0.1, 0.1)
                vis_val = base["shelf_visibility"] + random.uniform(-0.1, 0.1)
                multilingual = list(set(base["multilingual"] + [random.choice(["English", "Hindi", "Japanese", "Tamil"])]))
            
            # DNA templates
            if style == "Serif":
                dna_vals = [0.4, 0.8, 0.9, 0.7, 0.4, 0.6, 0.6, 0.4, 0.2]
            elif style == "Grotesque":
                dna_vals = [0.5, 0.2, 0.0, 0.2, 0.7, 0.7, 0.3, 0.5, 0.5]
            elif style == "Geometric":
                dna_vals = [0.4, 0.1, 0.0, 0.1, 0.8, 0.8, 0.9, 0.6, 0.9]
            elif style == "Slab":
                dna_vals = [0.8, 0.5, 0.7, 0.5, 0.6, 0.6, 0.2, 0.4, 0.7]
            elif style == "Display":
                dna_vals = [0.8, 0.9, 0.5, 0.6, 0.5, 0.5, 0.7, 0.3, 0.4]
            elif style == "Script":
                dna_vals = [0.3, 0.9, 0.4, 0.8, 0.3, 0.4, 0.9, 0.2, 0.1]
            else:
                dna_vals = [0.4, 0.4, 0.2, 0.6, 0.5, 0.5, 0.8, 0.3, 0.1]
                
            # Perturb DNA
            dna_vals = [min(1.0, max(0.0, val + random.uniform(-0.1, 0.1))) for val in dna_vals]
            embeddings_matrix[i, :9] = dna_vals
            
            dna = {
                "stroke_width": round(dna_vals[0], 2),
                "contrast": round(dna_vals[1], 2),
                "serif_angle": round(dna_vals[2], 2),
                "terminal_shape": round(dna_vals[3], 2),
                "x_height": round(dna_vals[4], 2),
                "cap_height": round(dna_vals[5], 2),
                "curvature": round(dna_vals[6], 2),
                "spacing_ratio": round(dna_vals[7], 2),
                "geometric_index": round(dna_vals[8], 2)
            }
            
            self.fonts[name] = {
                "name": name,
                "family": name.split()[0],
                "style": style,
                "categories": categories,
                "personality": personality,
                "target_age": target_age,
                "luxury_score": round(max(0.0, min(1.0, lux_val)), 2),
                "readability": round(max(0.0, min(1.0, read_val)), 2),
                "shelf_visibility": round(max(0.0, min(1.0, vis_val)), 2),
                "multilingual": multilingual,
                "dna": dna,
                "embedding": None
            }
            
        # Normalize embeddings matrix
        norms = np.linalg.norm(embeddings_matrix, axis=1, keepdims=True)
        embeddings_matrix = embeddings_matrix / (norms + 1e-8)
        
        # Add to FAISS index in bulk
        self.registry.index.add(embeddings_matrix)
        
        # Populate mapping lists
        for idx, (name, meta) in enumerate(self.fonts.items()):
            meta["embedding"] = embeddings_matrix[idx].tolist()
            self.registry.font_mapping.append({
                "index": idx,
                "font_name": name,
                "family": meta["family"],
                "style": meta["style"]
            })
            
        print(f"[FONTS DATABASE] Generated & Indexed {self.registry.index.ntotal} fonts successfully.")

    def get_font(self, font_name):
        return self.fonts.get(font_name)

    def list_all_fonts(self):
        return list(self.fonts.values())

    def search_similarity(self, query_vector, top_k=100):
        return self.registry.search_similar(query_vector, top_k)
