# ai_engine/ai_server.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import torch, clip, faiss, json
import numpy as np
from PIL import Image
from io import BytesIO

app = Flask(__name__)
CORS(app)

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

with open("products.json", "r") as f:
    products = json.load(f)

embeddings = np.load("embeddings.npy")
index = faiss.read_index("index.faiss")

@app.route("/match", methods=["POST"])
def match_image():
    file = request.files["image"]
    img = preprocess(Image.open(BytesIO(file.read()))).unsqueeze(0).to(device)

    with torch.no_grad():
        query_vec = model.encode_image(img).cpu().numpy().astype("float32")

    _, indices = index.search(query_vec, k=5)
    matches = [p for i in indices[0] for p in products if p["image"] == p["image"]]

    return jsonify({"matches": matches})

if __name__ == "__main__":
    app.run(port=5001)
