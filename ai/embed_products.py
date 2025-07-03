# ai_engine/embed_products.py
import os, json, faiss
import numpy as np
import torch
from PIL import Image
from tqdm import tqdm
from model_utils import load_clip_model

# Load model and device
model, preprocess, device = load_clip_model()

# Load product metadata
with open("products.json", "r", encoding="utf-8") as f:
    products = json.load(f)

image_dir = "product_images"
embeddings = []
image_names = []

missing = 0
for product in tqdm(products, desc="Embedding products"):
    image_path = os.path.join(image_dir, product["image"])
    if not os.path.exists(image_path):
        print(f"⚠️ Missing image: {product['image']}")
        missing += 1
        continue

    try:
        img = preprocess(Image.open(image_path).convert("RGB")).unsqueeze(0).to(device)
        with torch.no_grad():
            embed = model.encode_image(img).cpu().numpy()
            embeddings.append(embed[0])
            image_names.append(product["image"])
    except Exception as e:
        print(f"❌ Error with {product['image']}: {e}")
        continue

# Save embeddings
embeddings = np.array(embeddings).astype("float32")
np.save("embeddings.npy", embeddings)

# Save FAISS index
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)
faiss.write_index(index, "index.faiss")

# Optional: Save filenames
with open("image_names.json", "w") as f:
    json.dump(image_names, f)

print(f"✅ Indexed {len(embeddings)} images. ❌ Missing: {missing}")
