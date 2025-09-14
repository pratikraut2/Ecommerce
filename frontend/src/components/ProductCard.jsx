export default function ProductCard({ product, onAddToCart }) {
  const handleAddToCart = () => {
    if (onAddToCart) onAddToCart(product);
    console.log('Added to cart:', product);
  };

  return (
    <div className="bg-white rounded-lg shadow-md border border-gray-200 overflow-hidden hover:shadow-lg hover:scale-105 transition-all duration-200 group">
      <div className="relative aspect-square overflow-hidden">
        <img
          src={product.image}
          alt={product.name}
          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-200"
        />
        {!product.inStock && (
          <span className="absolute top-2 right-2 bg-gray-200 text-gray-700 px-2 py-1 text-xs rounded-md">
            Out of Stock
          </span>
        )}
      </div>
      <div className="p-4">
        <h3 className="font-medium text-gray-900 mb-2 line-clamp-2">
          {product.name}
        </h3>
        <p className="text-gray-600 text-sm mb-2 line-clamp-2">
          {product.description}
        </p>
        <div className="flex items-center justify-between mb-4">
          <span className="text-lg font-bold text-blue-600">
            ${product.price}
          </span>
          <span className="border border-gray-300 text-gray-600 px-2 py-1 text-xs rounded-md">
            {product.category}
          </span>
        </div>
        <button
          onClick={handleAddToCart}
          className={`w-full py-2 px-4 rounded-md font-medium transition-colors duration-200 ${
            product.inStock
              ? 'bg-blue-600 text-white hover:bg-blue-700'
              : 'bg-gray-300 text-gray-500 cursor-not-allowed'
          }`}
          disabled={!product.inStock}
        >
          {product.inStock ? 'Add to Cart' : 'Out of Stock'}
        </button>
      </div>
    </div>
  );
}
