class DesignKnowledgeGraph:
    """
    Simulates a multi-level graph mapping:
    Industry -> Category -> Subcategory -> Target Audience -> Emotion -> Typography -> Color -> Layout -> Material -> Print Constraints
    Provides Cypher-like lookup interfaces for brand psychology routing.
    """
    def __init__(self):
        self.nodes = {}
        self.edges = []
        self._build_graph()
        
    def _build_graph(self):
        # We define a rich knowledge graph for diverse industries
        # 1. Chocolate Industry path
        self._add_path(
            industry="Food & Beverage",
            category="Chocolate",
            subcategory="Luxury Dark Chocolate",
            audience="Adults 25-55 (Premium lifestyle)",
            emotion="Premium Sophistication & Indulgence",
            typography="High-Contrast Serif",
            color="Warm Brown & Foil Gold",
            layout="Classical Centered Minimalist",
            material="Recycled Kraft Cardboard",
            print_constraints="Foil Stamping & Matte Varnish"
        )
        
        self._add_path(
            industry="Food & Beverage",
            category="Chocolate",
            subcategory="Kids Candy Bar",
            audience="Children & Parents (3-12 years)",
            emotion="Fun, High Energy & Playfulness",
            typography="Rounded Handwritten / Display",
            color="Vibrant Red & Neon Yellow",
            layout="Dynamic Asymmetric Overlay",
            material="Glossy Plastic Wrap",
            print_constraints="Flexographic high-speed printing"
        )
        
        # 2. Cosmetics Industry path
        self._add_path(
            industry="Cosmetics & Beauty",
            category="Skincare",
            subcategory="Organic Facial Serum",
            audience="Eco-conscious Adults 18-45",
            emotion="Purity, Natural Wellness & Calmness",
            typography="Geometric Sans-Serif",
            color="Sage Green, Soft Sand & White",
            layout="Spacious Clean Grid",
            material="Frosted Amber Glass",
            print_constraints="Screen printing & Direct UV coating"
        )
        
        self._add_path(
            industry="Cosmetics & Beauty",
            category="Perfume",
            subcategory="Luxury Eau de Parfum",
            audience="High-end Consumer 20-60",
            emotion="Sensuality, Mystique & Prestige",
            typography="Elegant High-Contrast Serif / Script",
            color="Deep Obsidian & Rose Gold",
            layout="Ultra-Minimal Off-Center",
            material="Heavy Crystal Flacon",
            print_constraints="Acid etching & Hot-foil stamping"
        )

        # 3. Technology / AI
        self._add_path(
            industry="Technology",
            category="Artificial Intelligence",
            subcategory="AI Developer Tooling",
            audience="Software Engineers & CTOs 20-45",
            emotion="High Trust, Precision & Innovation",
            typography="Grotesque Variable Sans (Inter/Space Grotesk)",
            color="Midnight Blue & Cyber Lime",
            layout="Information-Dense Structured Grid",
            material="Aluminum casing / Digital screen",
            print_constraints="RGB Digital & Matte anodized engraving"
        )
        
        # 4. Medicine / Healthcare
        self._add_path(
            industry="Healthcare",
            category="Pharmaceuticals",
            subcategory="Pediatric Vitamin Gummy",
            audience="Parents & Kids (2-10 years)",
            emotion="Fun Safety, Friendliness & Health",
            typography="Bold Friendly Sans-Serif (Montserrat)",
            color="Soft Teal & Sweet Orange",
            layout="Clean Layout with Playful Icons",
            material="PET Recyclable Bottle",
            print_constraints="Glossy paper wrap label"
        )

        # 5. Premium Coffee Niche
        self._add_path(
            industry="Food & Beverage",
            category="Coffee",
            subcategory="Organic Espresso Blend",
            audience="Coffee Enthusiasts & Professionals",
            emotion="Rich Aroma, Authenticity & Focus",
            typography="Slab-Serif / Industrial Display",
            color="Dark Roast Brown & Warm Bronze",
            layout="Retro Bold Stamp",
            material="Matte Kraft Paper Bag",
            print_constraints="Screen print white ink & Matte finish"
        )

        # 6. Luxury Watch Niche
        self._add_path(
            industry="Luxury Goods",
            category="Watches",
            subcategory="Mechanical Chronograph",
            audience="Watch Collectors 30-70",
            emotion="Timeless Craftsmanship & Precision Heritage",
            typography="Elegant Geometric Sans-Serif",
            color="Metallic Silver, Slate Grey & White",
            layout="Balanced Centered Classic",
            material="Premium Textured Cardboard Box",
            print_constraints="Silver foil stamping & Blind deboss"
        )

        # 7. Wine & Spirits Niche
        self._add_path(
            industry="Food & Beverage",
            category="Alcohol",
            subcategory="Vintage Cabernet Sauvignon",
            audience="Wine Enthusiasts & Collectors 30-65",
            emotion="Prestige, Organic Soil Heritage & Depth",
            typography="Traditional High-Contrast Serif (Garamond)",
            color="Deep Bordeaux Red & Antique Gold",
            layout="Centered Classic Label",
            material="Uncoated Linen Paper Label",
            print_constraints="Embossed gold foil & Deckled edge"
        )

        # 8. Energy Drink Niche
        self._add_path(
            industry="Food & Beverage",
            category="Energy Drinks",
            subcategory="Extreme Caffeine Energy",
            audience="Gen Z Athletes & Gamers 16-30",
            emotion="High Voltage, Adrenaline & Intense Focus",
            typography="Aggressive Slanted Sans / Sci-Fi Display",
            color="Matte Black & Fluorescent Green",
            layout="Vertical Dynamic Text Block",
            material="Brushed Aluminum Can",
            print_constraints="Offset thermal transfer & Gloss varnish"
        )

        # 9. Baby Care Niche
        self._add_path(
            industry="Consumer Goods",
            category="Baby Care",
            subcategory="Organic Diaper Cream",
            audience="New Parents 22-40",
            emotion="Pure Gentleness, Safety & Calming Care",
            typography="Soft Rounded Friendly Sans (Quicksand)",
            color="Pastel Blue, Soft Cream & Lavender",
            layout="Symmetric Soft Margins",
            material="Bio-plastic Squeeze Tube",
            print_constraints="Water-based screen print & Satin finish"
        )

        # 10. Health Supplement Niche
        self._add_path(
            industry="Healthcare",
            category="Supplements",
            subcategory="Nootropic Brain Booster",
            audience="Biohackers & Professionals 20-50",
            emotion="Peak Cognitive Performance & Scientific Trust",
            typography="Tech Mono-spaced / Futuristic Sans",
            color="Cobalt Blue, Clean White & Silver",
            layout="Structured Grid with Data Table",
            material="Matte Finish HDPE Bottle",
            print_constraints="Thermal transfer UV labels"
        )

        # 11. Dairy / Milk Packaging Niche
        self._add_path(
            industry="Food & Beverage",
            category="Dairy",
            subcategory="Fresh Milk Packet",
            audience="General Families & Household Consumers",
            emotion="Purity, Freshness, Health & Wholesomeness",
            typography="Friendly Rounded Sans-Serif",
            color="Sky Blue, Clean White & Cream",
            layout="Clean Spacious Balanced Layout",
            material="Recyclable HDPE Plastic Bag / Tetra Pak",
            print_constraints="Flexographic low-odor inks & Satin finish"
        )

    def _add_path(self, **kwargs):
        # Dynamically create nodes and add directed relationships
        keys = list(kwargs.keys())
        for i in range(len(keys) - 1):
            source_type = keys[i]
            target_type = keys[i+1]
            source_name = kwargs[source_type]
            target_name = kwargs[target_type]
            
            # Register nodes
            self.nodes[source_name] = {"label": source_name, "type": source_type}
            self.nodes[target_name] = {"label": target_name, "type": target_type}
            
            # Register edges
            edge = {
                "source": source_name,
                "target": target_name,
                "relationship": f"determines_{target_type}"
            }
            if edge not in self.edges:
                self.edges.append(edge)

    def cypher_query(self, match_type, match_value):
        """
        Simulates Cypher: MATCH (n {type: match_type, value: match_value})-[r*]->(m) RETURN m
        Traces the downstream nodes in the design path.
        """
        results = {}
        # Find starting node
        start_node_name = None
        for name, meta in self.nodes.items():
            if meta["type"] == match_type and match_value.lower() in name.lower():
                start_node_name = name
                break
                
        if not start_node_name:
            # Try to match subcategory or category generally
            for name, meta in self.nodes.items():
                if match_value.lower() in name.lower():
                    start_node_name = name
                    break
                    
        if not start_node_name:
            return {}
            
        # Traverse downstream
        current = start_node_name
        results[self.nodes[current]["type"]] = current
        
        visited = set()
        while current and current not in visited:
            visited.add(current)
            next_node = None
            for edge in self.edges:
                if edge["source"] == current:
                    next_node = edge["target"]
                    results[self.nodes[next_node]["type"]] = next_node
                    break
            current = next_node
            
        return results

    def get_full_graph(self):
        """
        Returns full nodes and edges list for drawing in frontend D3/cytoscape plots.
        """
        return {
            "nodes": [{"id": name, "label": meta["label"], "type": meta["type"]} for name, meta in self.nodes.items()],
            "edges": self.edges
        }
