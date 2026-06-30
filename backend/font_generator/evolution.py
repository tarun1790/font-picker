import xml.etree.ElementTree as ET
import os

class FontEvolutionEngine:
    """
    Simulates generative glyph mutation and SVG font creation.
    Takes a base Font DNA dictionary, applies delta modifications (Luxury, Modern, Readability),
    calculates new glyph paths, and outputs vector representations.
    """
    @staticmethod
    def evolve_font_dna(base_dna, adjustment_params):
        """
        Applies modifiers to DNA parameters:
        adjustment_params: {"luxury": float, "modern": float, "readability": float}
        E.g., +0.20 Luxury, -0.10 Curviness.
        """
        evolved = base_dna.copy()
        
        lux = adjustment_params.get("luxury", 0.0)
        mod = adjustment_params.get("modern", 0.0)
        read = adjustment_params.get("readability", 0.0)
        
        # 1. Luxury increases contrast and increases serif angle, decreases width
        evolved["contrast"] = min(1.0, max(0.0, evolved["contrast"] + (lux * 0.3)))
        evolved["serif_angle"] = min(1.0, max(0.0, evolved["serif_angle"] + (lux * 0.4)))
        evolved["stroke_width"] = min(1.0, max(0.0, evolved["stroke_width"] - (lux * 0.15)))
        
        # 2. Modern increases geometric index, decreases serif angle, increases x-height
        evolved["geometric_index"] = min(1.0, max(0.0, evolved["geometric_index"] + (mod * 0.4)))
        evolved["serif_angle"] = min(1.0, max(0.0, evolved["serif_angle"] - (mod * 0.5)))
        evolved["x_height"] = min(1.0, max(0.0, evolved["x_height"] + (mod * 0.2)))
        
        # 3. Readability balances contrast (moves toward 0.5), sets spacing ratio to medium-high
        target_contrast = 0.4
        evolved["contrast"] = evolved["contrast"] + (target_contrast - evolved["contrast"]) * read
        evolved["spacing_ratio"] = min(1.0, max(0.0, evolved["spacing_ratio"] + (read * 0.3)))
        
        # Round evolved values
        for key in evolved:
            evolved[key] = round(evolved[key], 4)
            
        return evolved

    @staticmethod
    def generate_svg_glyph(char, dna):
        """
        Generates vector SVG paths for characters (A-Z, numbers) dynamically
        styled using Font DNA variables (e.g. stroke-width, curvature, contrast).
        """
        # Base dimensions
        width = 100
        height = 100
        stroke_w = 4 + (dna["stroke_width"] * 16)
        contrast_ratio = 1.0 - (dna["contrast"] * 0.7) # ratio of thin lines
        stroke_thin = stroke_w * contrast_ratio
        
        is_serif = dna["serif_angle"] > 0.4
        curve_factor = dna["curvature"]
        
        paths = []
        
        # Vector coordinates mapping based on character geometry
        if char == 'A':
            # Slanted legs
            paths.append(f"M 15,90 L 45,15 L 55,15 L 85,90")
            # Crossbar (thin line)
            paths.append(f"M 28,65 L 72,65")
            if is_serif:
                # Add horizontal serif lines at the feet
                paths.append(f"M 5,90 L 25,90 M 75,90 L 95,90")
        elif char == 'B':
            # Vertical stem
            paths.append(f"M 25,10 L 25,90")
            # Double loop
            r1 = 20 * (1.0 + curve_factor * 0.2)
            r2 = 22 * (1.0 + curve_factor * 0.2)
            paths.append(f"M 25,10 H 50 C 65,10 70,30 50,45 H 25")
            paths.append(f"M 25,45 H 52 C 68,45 75,90 50,90 H 25")
            if is_serif:
                paths.append(f"M 15,10 L 35,10 M 15,90 L 35,90")
        elif char == 'C':
            # Curve
            rx = 30 * (1.0 + curve_factor * 0.1)
            ry = 40 * (1.0 + curve_factor * 0.1)
            paths.append(f"M 75,25 C 60,10 30,10 30,50 C 30,90 60,90 75,75")
        elif char == 'O':
            # Oval / Circle
            if curve_factor > 0.7:
                # Perfect circle
                paths.append(f"M 50,10 A 40,40 0 1,1 50,90 A 40,40 0 1,1 50,10 Z")
            else:
                # Ellipse
                paths.append(f"M 50,10 C 25,10 25,90 50,90 C 75,90 75,10 50,10 Z")
        elif char == 'T':
            # Top bar and stem
            paths.append(f"M 15,15 H 85 M 50,15 V 90")
            if is_serif:
                paths.append(f"M 15,10 V 20 M 85,10 V 20 M 40,90 H 60,90")
        else:
            # Fallback simple letter skeleton
            paths.append(f"M 20,20 L 80,20 L 80,80 L 20,80 Z")
            
        # Compile paths to SVG markup
        svg_parts = []
        for idx, p in enumerate(paths):
            s_val = stroke_w if idx == 0 else stroke_thin
            # Return SVG path object
            svg_parts.append(f'<path d="{p}" stroke="currentColor" fill="none" stroke-width="{s_val:.1f}" stroke-linecap="round" stroke-linejoin="round" />')
            
        return "\n  ".join(svg_parts)

    @classmethod
    def compile_svg_font_face(cls, font_name, dna):
        """
        Creates an inline SVG Font container preview
        containing vector definitions of glyphs for the evolved font.
        """
        characters = ['A', 'B', 'C', 'O', 'T']
        glyph_defs = {}
        for char in characters:
            glyph_defs[char] = cls.generate_svg_glyph(char, dna)
            
        return {
            "font_name": font_name,
            "dna": dna,
            "glyphs": glyph_defs
        }
