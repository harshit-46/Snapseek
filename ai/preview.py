import os
import pandas as pd
import json
import requests
from PIL import Image
from io import BytesIO

# Constants
CSV_FILE = "amz_in_total_products_data_processed.csv"
IMAGE_DIR = "product_images"
BATCH_SIZE = 10000
PROGRESS_FILE = "progress.txt"

# Create image folder if not exists
os.makedirs(IMAGE_DIR, exist_ok=True)

# Load CSV
df = pd.read_csv(CSV_FILE)

# Initialize start index
start_index = 0
if os.path.exists(PROGRESS_FILE):
    with open(PROGRESS_FILE, "r") as f:
        start_index = int(f.read().strip())

end_index = min(start_index + BATCH_SIZE, len(df))
print(f"➡️ Starting from {start_index}, ending at {end_index}")

products = []
downloaded = 0

for idx in range(start_index, end_index):
    row = df.iloc[idx]
    asin = row["asin"]
    title = str(row["title"])
    img_url = row["imgUrl"]
    product_url = row["productURL"]
    price = row["price"]
    
    image_filename = f"{asin}.jpg"
    image_path = os.path.join(IMAGE_DIR, image_filename)

    # Skip if image already exists
    if os.path.exists(image_path):
        continue

    try:
        # Download image
        response = requests.get(img_url, timeout=10)
        img = Image.open(BytesIO(response.content)).convert("RGB")
        img.save(image_path)

        # Store metadata
        products.append({
            "image": image_filename,
            "name": title,
            "price": f"₹{price}",
            "url": product_url
        })

        downloaded += 1

        if downloaded % 500 == 0:
            print(f"✅ Downloaded {downloaded} images...")

    except Exception as e:
        print(f"❌ Failed for {asin}: {e}")
        continue

# Save this batch's metadata
json_file = f"products_part_{start_index + 1}-{end_index}.json"
with open(json_file, "w", encoding="utf-8") as f:
    json.dump(products, f, indent=4, ensure_ascii=False)

# Update progress
with open(PROGRESS_FILE, "w") as f:
    f.write(str(end_index))

print(f"\n✅ Done. Downloaded {downloaded} products from index {start_index} to {end_index - 1}")
print(f"📦 Metadata saved to {json_file}")