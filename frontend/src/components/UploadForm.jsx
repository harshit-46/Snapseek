// src/components/UploadForm.jsx
import React, { useState } from 'react';
import axios from 'axios';
import Results from './Results';

const UploadForm = () => {
    const [image, setImage] = useState(null);
    const [results, setResults] = useState([]);

    const handleUpload = async () => {
        const formData = new FormData();
        formData.append('image', image);

        try {
            const res = await axios.post('http://localhost:5000/upload', formData);
            setResults(res.data.matches);
        } catch (err) {
            alert("Error: " + err.message);
        }
    };

    return (
        <div className="flex flex-col items-center gap-6">
            <input type="file" onChange={e => setImage(e.target.files[0])} />
            <button
                onClick={handleUpload}
                className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
            >
                Search Similar Products
            </button>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
                {results.map((item, idx) => (
                    <Results key={idx} product={item} />
                ))}
            </div>
        </div>
    );
};

export default UploadForm;
