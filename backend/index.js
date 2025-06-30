const express = require("express");
const cors = require("cors");
const multer = require("multer");
const axios = require("axios");
const FormData = require("form-data");
const fs = require("fs");

const app = express();
const upload = multer({ dest: "uploads/" });
app.use(cors());

app.post("/upload", upload.single("image"), async (req, res) => {
    const imagePath = req.file.path;

    try {
        const form = new FormData();
        form.append("image", fs.createReadStream(imagePath));

        const aiRes = await axios.post("http://localhost:5001/match", form, {
            headers: form.getHeaders(),
        });

        fs.unlinkSync(imagePath); // remove after forwarding
        return res.json({ results: aiRes.data.matches });
    } catch (err) {
        console.error(err);
        return res.status(500).json({ error: "Image match failed." });
    }
});

app.listen(5000, () => {
    console.log("Backend API running on http://localhost:5000");
});
