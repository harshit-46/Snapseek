import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
from flask import Flask, request, jsonify
from flask_cors import CORS
import faiss, json, numpy as np
from PIL import Image, UnidentifiedImageError
import torch
from io import BytesIO
from model_utils import load_clip_model

app = Flask(__name__)
CORS(app)

# Load CLIP model
model, preprocess, device = load_clip_model()

# Load product metadata and vector index
try:
    with open("products.json", "r", encoding="utf-8") as f:
        products = json.load(f)
    embeddings = np.load("embeddings.npy")
    index = faiss.read_index("index.faiss")

    if len(products) != embeddings.shape[0]:
        print("⚠️ Warning: products and embeddings count mismatch.")
except Exception as e:
    print(f"❌ Failed to load data: {e}")
    exit()

@app.route("/match", methods=["POST"])
def match_image():
    if "image" not in request.files:
        return jsonify({"error": "No image file"}), 400

    file = request.files["image"]
    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    try:
        # Read and preprocess image
        img = Image.open(BytesIO(file.read())).convert("RGB")
        img_tensor = preprocess(img).unsqueeze(0).to(device)

        # Encode image using CLIP
        with torch.no_grad():
            query_vec = model.encode_image(img_tensor).cpu().numpy().astype("float32")

        # Search for top 5 similar vectors
        distances, indices = index.search(query_vec, k=5)

        # Get matched products
        matches = [products[i] for i in indices[0]]

        # Remove duplicates based on image name
        seen = set()
        unique_matches = []
        for product in matches:
            if product["image"] not in seen:
                unique_matches.append(product)
                seen.add(product["image"])

        print("Matched:", [p["name"] for p in unique_matches])  # Optional logging
        return jsonify({"matches": unique_matches})

    except UnidentifiedImageError:
        return jsonify({"error": "Unsupported or corrupted image"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print(f"✅ Loaded {len(products)} products using CLIP on {device}")
    app.run(port=5001, debug=True)
