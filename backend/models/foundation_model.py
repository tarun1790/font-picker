import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.models as models

# Enforce GPU Execution as per user rules
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"[FOUNDATION MODEL] Initializing on device: {device}")

class TypographyViTEncoder(nn.Module):
    """
    Typography Foundation Model
    CNN Trunk (ResNet18) + Transformer Encoder
    Input: [Batch, 1, 128, 128] representing glyph rendering
    Output: 1024-D Typography Embedding Space
    """
    def __init__(self, embedding_dim=1024):
        super(TypographyViTEncoder, self).__init__()
        # Use a lightweight ResNet back-end to extract visual feature maps
        resnet = models.resnet18(weights=None)
        # Adapt first layer to single channel grayscale glyphs
        self.conv1 = nn.Conv2d(1, 64, kernel_size=7, stride=2, padding=3, bias=False)
        self.bn1 = resnet.bn1
        self.relu = resnet.relu
        self.maxpool = resnet.maxpool
        
        self.layer1 = resnet.layer1
        self.layer2 = resnet.layer2
        self.layer3 = resnet.layer3
        self.layer4 = resnet.layer4
        
        # Feature dimension out of layer 4 is [Batch, 512, 4, 4] for 128x128 input
        self.num_features = 512
        
        # Transformer Encoder Layer
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=self.num_features, 
            nhead=8, 
            dim_feedforward=1024, 
            dropout=0.1, 
            batch_first=True
        )
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=3)
        
        # Projection head to output 1024-D
        self.fc = nn.Linear(self.num_features, embedding_dim)
        
    def forward(self, x):
        # Move inputs to same device as model
        x = x.to(device)
        
        # ResNet Backbone
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.maxpool(x)
        
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x) # Shape: [Batch, 512, H_feat, W_feat]
        
        # Flatten spatial dimensions for Transformer input: [Batch, Sequence_Len, Features]
        batch_size, channels, h, w = x.shape
        x = x.view(batch_size, channels, h * w).transpose(1, 2) # [Batch, H*W, 512]
        
        # Transformer Encoder
        x = self.transformer(x) # [Batch, H*W, 512]
        
        # Global Average Pool over sequence dimension
        x = x.mean(dim=1) # [Batch, 512]
        
        # Project to 1024-D Embedding Space & L2 Normalize
        embedding = self.fc(x)
        embedding = F.normalize(embedding, p=2, dim=1)
        return embedding

class TripletLoss(nn.Module):
    """
    Contrastive Metric Learning Triplet Loss
    L = max(d(a,p) - d(a,n) + margin, 0)
    """
    def __init__(self, margin=0.2):
        super(TripletLoss, self).__init__()
        self.margin = margin
        
    def forward(self, anchor, positive, negative):
        distance_positive = (anchor - positive).pow(2).sum(dim=1)
        distance_negative = (anchor - negative).pow(2).sum(dim=1)
        loss = F.relu(distance_positive - distance_negative + self.margin)
        return loss.mean()

class FontDNAVectorizer(nn.Module):
    """
    Font DNA Feature Extractor
    Takes a 1024-D Typography Embedding and decodes it into
    interpretable, engineered descriptor scores between 0.0 and 1.0.
    """
    def __init__(self, embedding_dim=1024):
        super(FontDNAVectorizer, self).__init__()
        # Dense layers mapping embedding to DNA properties
        self.decoder = nn.Sequential(
            nn.Linear(embedding_dim, 256),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(256, 9), # 9 features of Font DNA
            nn.Sigmoid()       # Normalize between 0 and 1
        )
        
    def forward(self, embedding):
        embedding = embedding.to(device)
        dna_scores = self.decoder(embedding)
        return dna_scores

    @staticmethod
    def map_dna_vector(dna_vector):
        """
        Maps raw float DNA scores to a structured JSON object.
        """
        features = [
            "stroke_width",     # 0: Thin -> Thick
            "contrast",         # 1: Monolinear -> High contrast
            "serif_angle",      # 2: Sans-serif (0) -> High serif angle
            "terminal_shape",   # 3: Grotesque terminal -> Humanist tail
            "x_height",         # 4: Low x-height -> Tall x-height
            "cap_height",       # 5: Cap height ratio
            "curvature",        # 6: Angular/geometric -> Organic curve
            "spacing_ratio",    # 7: Tight kerning -> Open kerning
            "geometric_index"   # 8: Organic/humanist -> Geometric structure
        ]
        
        # Check if vector is PyTorch tensor or numpy/list
        if isinstance(dna_vector, torch.Tensor):
            vals = dna_vector.detach().cpu().tolist()
        else:
            vals = list(dna_vector)
            
        return {features[i]: round(vals[i], 4) for i in range(len(features))}

def load_foundation_model():
    """
    Helper to instantiate model on correct GPU/CPU device
    """
    encoder = TypographyViTEncoder().to(device)
    dna_decoder = FontDNAVectorizer().to(device)
    encoder.eval()
    dna_decoder.eval()
    return encoder, dna_decoder
