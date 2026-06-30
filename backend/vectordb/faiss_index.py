import faiss
import numpy as np
import os
import json
import torch

class FontFAISSRegistry:
    """
    Registry managing FAISS indexes of 1024-Dimensional Typography Foundation Model Embeddings.
    Allows saving, loading, and searching the top 100 similar fonts.
    """
    def __init__(self, dimension=1024):
        self.dimension = dimension
        # Flat Index (L2 distance or Inner Product)
        self.index = faiss.IndexFlatL2(self.dimension)
        # In-memory mapping of FAISS index positions to font identifiers
        self.font_mapping = [] # List of dicts: {"index": int, "font_name": str, "family": str, "style": str}
        
    def add_font(self, font_name, family, style, embedding_vector):
        """
        Appends a font embedding to the FAISS index.
        """
        assert len(embedding_vector) == self.dimension, f"Embedding must be {self.dimension}-D"
        # Convert to float32 numpy array
        vec_arr = np.array(embedding_vector, dtype=np.float32).reshape(1, -1)
        self.index.add(vec_arr)
        
        pos = len(self.font_mapping)
        self.font_mapping.append({
            "index": pos,
            "font_name": font_name,
            "family": family,
            "style": style
        })
        
    def search_similar(self, query_vector, top_k=100):
        """
        Performs a vector search in FAISS and returns similarity scores and font metadata.
        """
        if self.index.ntotal == 0:
            return []
            
        vec_arr = np.array(query_vector, dtype=np.float32).reshape(1, -1)
        top_k = min(top_k, self.index.ntotal)
        
        distances, indices = self.index.search(vec_arr, top_k)
        
        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx == -1:
                continue
            meta = self.font_mapping[idx]
            # Convert L2 distance to percentage similarity
            similarity = float(1.0 / (1.0 + dist))
            results.append({
                "font_name": meta["font_name"],
                "family": meta["family"],
                "style": meta["style"],
                "distance": float(dist),
                "similarity": round(similarity, 4)
            })
            
        return results

    def save_index(self, folder_path):
        """
        Persists the index and metadata to disk.
        """
        os.makedirs(folder_path, exist_ok=True)
        faiss.write_index(self.index, os.path.join(folder_path, "fonts.faiss"))
        with open(os.path.join(folder_path, "mapping.json"), "w") as f:
            json.dump(self.font_mapping, f, indent=2)
            
    def load_index(self, folder_path):
        """
        Loads the index and metadata from disk.
        """
        index_file = os.path.join(folder_path, "fonts.faiss")
        mapping_file = os.path.join(folder_path, "mapping.json")
        
        if os.path.exists(index_file) and os.path.exists(mapping_file):
            self.index = faiss.read_index(index_file)
            with open(mapping_file, "r") as f:
                self.font_mapping = json.load(f)
            print(f"[FAISS REGISTRY] Loaded index containing {self.index.ntotal} fonts.")
            return True
        return False
