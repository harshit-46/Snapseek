const Results = ({ results }) => {
    return (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6 mt-8">
            {results.map((item, idx) => (
                <div key={idx} className="border p-4 rounded-lg shadow-md bg-white">
                    <img src={`/product_images/${item.image}`} alt={item.name} className="w-full h-48 object-cover rounded-md" />
                    <h3 className="text-xl font-semibold mt-2">{item.name}</h3>
                    <p className="text-gray-600">{item.price}</p>
                    <a href={item.url} target="_blank" className="text-blue-500 hover:underline mt-2 block">View Product</a>
                </div>
            ))}
        </div>
    );
};