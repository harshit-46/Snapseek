const express = require("express");
const multer = require("multer");
const cors = require("cors");
const fs = require("fs");
const axios = require("axios");
const FormData = require("form-data");

const app = express();
app.use(cors());

const upload = multer({ dest: "uploads/" });

app.post("/upload", upload.single("image"), async (req, res) => {
    const imagePath = req.file.path;

    try {
        const form = new FormData();
        form.append("image", fs.createReadStream(imagePath));

        const response = await axios.post("http://localhost:5001/match", form, {
            headers: form.getHeaders(),
        });

        res.json(response.data);
    } catch (err) {
        console.error("Error forwarding to Flask:", err.message);
        res.status(500).json({ error: "Failed to connect to AI engine" });
    } finally {
        fs.unlinkSync(imagePath); // Clean up
    }
});

app.listen(5000, () => console.log("🚀 Backend running on port 5000"));
