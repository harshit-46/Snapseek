// src/components/ResultCard.jsx
import React from 'react';

const Results = ({ product }) => {
    const imagePath = product.image.replace(/^\/?static\/?/, '');
    return (
        <div className="bg-white shadow-md rounded-lg p-4 text-center">
            <img
                src={`http://localhost:5001/static/${imagePath}`}
                alt={product.name}
                className="w-full h-40 object-contain mb-4"
            />
            <iframe
                src="https://huggingface.co/datasets/rajuptvs/ecommerce_products_clip/embed/viewer/default/train"
                frameborder="0"
                width="100%"
                height="560px"
            ></iframe>
            <h3 className="text-lg font-semibold">{product.name}</h3>
            <p className="text-green-600 font-bold">{product.price}</p>
            <a
                href={product.url}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-block mt-2 px-4 py-1 bg-blue-600 text-white rounded hover:bg-blue-700"
            >
                View Product
            </a>
        </div>
    );
};

export default Results;
