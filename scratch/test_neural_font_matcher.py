import io
import torch
import torchvision.models as models
import torchvision.transforms as transforms
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import cv2

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 1. Initialize Deep Neural Vision Feature Extractor
class DeepFontVisualEmbedder:
    def __init__(self):
        self.backbone = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
        # Remove final classification layer to get 512-dim visual embeddings
        self.backbone.fc = torch.nn.Identity()
        self.backbone = self.backbone.to(device).eval()
        
        self.preprocess = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        
    def embed_image(self, pil_image):
        # Convert to RGB and preprocess
        img_t = self.preprocess(pil_image.convert("RGB")).unsqueeze(0).to(device)
        with torch.no_grad():
            feat = self.backbone(img_t)
            # L2 normalize
            feat = torch.nn.functional.normalize(feat, p=2, dim=1)
        return feat.squeeze(0).cpu().numpy()

embedder = DeepFontVisualEmbedder()
print("DeepFontVisualEmbedder initialized successfully on GPU:", device)
