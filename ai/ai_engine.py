from flask import Flask, request, jsonify
from flask_cors import CORS
import torch
import clip
from PIL import Image
import os
import numpy as np
import faiss
import io

app = Flask(__name__)
CORS(app)

# Load CLIP model
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

# Load product image embeddings
product_dir = "product_images"
product_files = [f for f in os.listdir(product_dir) if f.endswith(('.png', '.jpg'))]
embeddings = []

for img_path in product_files:
    image = preprocess(Image.open(os.path.join(product_dir, img_path))).unsqueeze(0).to(device)
    with torch.no_grad():
        embedding = model.encode_image(image)
        embedding /= embedding.norm(dim=-1, keepdim=True)
        embeddings.append(embedding.cpu().numpy())

embeddings = np.vstack(embeddings).astype("float32")
index = faiss.IndexFlatIP(embeddings.shape[1])
index.add(embeddings)

# Match endpoint
@app.route('/match', methods=['POST'])
def match_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    file = request.files['image']
    image = Image.open(io.BytesIO(file.read()))
    image_tensor = preprocess(image).unsqueeze(0).to(device)

    with torch.no_grad():
        query = model.encode_image(image_tensor)
        query /= query.norm(dim=-1, keepdim=True)

    query_np = query.cpu().numpy().astype("float32")
    distances, indices = index.search(query_np, 5)

    matches = [product_files[i] for i in indices[0]]
    return jsonify({'matches': matches})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
