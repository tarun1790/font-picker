import sys
import os
import torch
import numpy as np

# Adjust path to import backend modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from backend.models.foundation_model import TypographyViTEncoder, FontDNAVectorizer
from backend.models.saliency_model import VisualSaliencyViT
from backend.vectordb.faiss_index import FontFAISSRegistry
from backend.services.fonts_db import FontMetadataDatabase
from backend.services.knowledge_graph import DesignKnowledgeGraph
from backend.font_generator.evolution import FontEvolutionEngine

def run_system_verification_tests():
    print("==================================================")
    print("   AI TYPOGRAPHY SYSTEM INTEGRATION VERIFICATION  ")
    print("==================================================")
    
    # 1. Check GPU / CUDA Enforcement
    cuda_available = torch.cuda.is_available()
    device = torch.device("cuda" if cuda_available else "cpu")
    print(f"[TEST 1] CUDA Enforcement: {'PASSED (CUDA Active)' if cuda_available else 'WARNING (CPU Fallback)'}")
    print(f"         Device Name: {torch.cuda.get_device_name(0) if cuda_available else 'CPU'}")
    
    # 2. Test Foundation Typography Encoder
    print("\n[TEST 2] Loading Typography Foundation Model...")
    encoder = TypographyViTEncoder().to(device)
    encoder.eval()
    
    # Input batch size 2, grayscale, 128x128 image
    dummy_input = torch.randn(2, 1, 128, 128).to(device)
    with torch.no_grad():
        embeddings = encoder(dummy_input)
        
    print(f"         Dummy Input shape: {dummy_input.shape}")
    print(f"         Output Embedding shape: {embeddings.shape}")
    assert embeddings.shape == (2, 1024), "Typography embedding dimension must be 1024-D"
    print("         Typography Foundation Model Output: PASSED")
    
    # 3. Test Saliency Attention Map
    print("\n[TEST 3] Loading Eye-Tracking Saliency Model...")
    saliency_model = VisualSaliencyViT().to(device)
    saliency_model.eval()
    
    dummy_img = torch.randn(2, 3, 224, 224).to(device)
    with torch.no_grad():
        heatmaps = saliency_model(dummy_img)
        
    print(f"         Dummy Image shape: {dummy_img.shape}")
    print(f"         Output Heatmap shape: {heatmaps.shape}")
    assert heatmaps.shape == (2, 1, 224, 224), "Saliency map must match input spatial dimensions"
    print("         Saliency Model Attention Resolution: PASSED")
    
    # 4. Test FAISS Vector Search & Database Ingestion
    print("\n[TEST 4] Loading FAISS registry & Ingestion pipeline...")
    font_db = FontMetadataDatabase()
    all_fonts = font_db.list_all_fonts()
    print(f"         Total fonts indexed in memory: {len(all_fonts)}")
    assert len(all_fonts) == 100000, "Font metadata builder must index 100,000 fonts"
    
    # Run mock search query
    query_emb = np.random.normal(0.0, 0.1, 1024)
    query_emb = query_emb / np.linalg.norm(query_emb)
    similar_fonts = font_db.search_similarity(query_emb.tolist(), top_k=10)
    print(f"         FAISS Search Query returns: {len(similar_fonts)} matches")
    print(f"         Top Match: {similar_fonts[0]['font_name']} (Similarity: {similar_fonts[0]['similarity']*100:.2f}%)")
    assert len(similar_fonts) == 10, "FAISS vector search failed"
    print("         FAISS Registry Search: PASSED")
    
    # 5. Test Knowledge Graph Routing
    print("\n[TEST 5] Testing Multi-level Knowledge Graph lookup...")
    kg = DesignKnowledgeGraph()
    path = kg.cypher_query("Subcategory", "Luxury Dark Chocolate")
    print(f"         Graph Path Traverse for 'Luxury Dark Chocolate':")
    for k, v in path.items():
        print(f"            - {k}: {v}")
    assert "typography" in path, "Knowledge Graph traversing failed"
    print("         Knowledge Graph Relationship Routing: PASSED")
    
    # 6. Test Font DNA Evolution Engine
    print("\n[TEST 6] Testing Font DNA Evolution Engine parameters...")
    base_dna = {
        "stroke_width": 0.4,
        "contrast": 0.8,
        "serif_angle": 0.9,
        "terminal_shape": 0.7,
        "x_height": 0.4,
        "cap_height": 0.6,
        "curvature": 0.6,
        "spacing_ratio": 0.4,
        "geometric_index": 0.2
    }
    evolved = FontEvolutionEngine.evolve_font_dna(base_dna, {"luxury": 0.5, "modern": -0.2, "readability": 0.0})
    print(f"         Base Contrast: {base_dna['contrast']} -> Evolved Contrast: {evolved['contrast']}")
    print(f"         Base Serif Angle: {base_dna['serif_angle']} -> Evolved Serif Angle: {evolved['serif_angle']}")
    assert evolved["contrast"] > base_dna["contrast"], "Font DNA evolution parameter calculations failed"
    print("         DNA Parameter Evolution Calculations: PASSED")
    
    print("\n==================================================")
    print("        ALL SYSTEM INTEGRATION TESTS PASSED       ")
    print("==================================================")

if __name__ == "__main__":
    run_system_verification_tests()
