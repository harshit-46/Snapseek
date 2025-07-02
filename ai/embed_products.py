# ai_engine/embed_products.py
import os, json, clip, torch
import numpy as np
import faiss
from PIL import Image
from tqdm import tqdm

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

with open("products.json", "r") as f:
    products = json.load(f)

image_dir = "product_images"
embeddings = []
image_names = []

for product in tqdm(products):
    image_path = os.path.join(image_dir, product["image"])
    if not os.path.exists(image_path): continue

    img = preprocess(Image.open(image_path)).unsqueeze(0).to(device)
    with torch.no_grad():
        embed = model.encode_image(img).cpu().numpy()
        embeddings.append(embed[0])
        image_names.append(product["image"])

embeddings = np.array(embeddings).astype("float32")

# Save embeddings
np.save("embeddings.npy", embeddings)

# Save FAISS index
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)
faiss.write_index(index, "index.faiss")

print(f"✅ Indexed {len(embeddings)} product images.")
