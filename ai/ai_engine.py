from flask import Flask, request, jsonify
from flask_cors import CORS
import faiss, json, numpy as np
from PIL import Image
import torch
from io import BytesIO
from model_utils import load_clip_model

app = Flask(__name__)
CORS(app)

model, preprocess, device = load_clip_model()

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
        img = preprocess(Image.open(BytesIO(file.read())).convert("RGB")).unsqueeze(0).to(device)
        with torch.no_grad():
            query_vec = model.encode_image(img).cpu().numpy().astype("float32")

        _, indices = index.search(query_vec, k=5)
        matches = [products[i] for i in indices[0]]

        return jsonify({"matches": matches})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print(f"✅ Loaded {len(products)} products using CLIP on {device}")
    app.run(port=5001, debug=True)
