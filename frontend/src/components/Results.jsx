// src/components/ResultCard.jsx
import React from 'react';

const Results = ({ product }) => {
    return (
        <div className="bg-white shadow-md rounded-lg p-4 text-center">
            <img
                src={`http://localhost:5001/static/${product.image}`}
                alt={product.name}
                className="w-full h-40 object-contain mb-4"
            />
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
