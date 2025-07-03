# ai_engine/ai_server.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import torch, clip, faiss, json
import numpy as np
from PIL import Image
from io import BytesIO

app = Flask(__name__)
CORS(app)

# Load CLIP model
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

# Load product metadata
with open("products.json", "r", encoding='utf-8') as f:
    products = json.load(f)

# Load image embeddings and FAISS index
try:
    embeddings = np.load("embeddings.npy")
    index = faiss.read_index("index.faiss")
except Exception as e:
    print(f"Failed to load index or embeddings: {e}")
    exit()

@app.route("/match", methods=["POST"])
def match_image():
    if "image" not in request.files:
        return jsonify({"error": "No image file found in request"}), 400

    file = request.files["image"]
    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    try:
        img = preprocess(Image.open(BytesIO(file.read())).convert("RGB")).unsqueeze(0).to(device)

        with torch.no_grad():
            query_vec = model.encode_image(img).cpu().numpy().astype("float32")

        _, indices = index.search(query_vec, k=5)
        matched_indices = indices[0]

        matches = [products[i] for i in matched_indices]

        return jsonify({"matches": matches})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5001, debug=True)
