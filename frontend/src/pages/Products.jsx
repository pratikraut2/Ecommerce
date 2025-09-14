// src/pages/Products.jsx
import React, { useEffect, useState } from "react";
import { getProducts } from "../api/products"; // your axios API call
import ProductCard from "../components/ProductCard";

function Products() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);

  // Fetch products on mount
  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const data = await getProducts(); // fetch from backend
        setProducts(data);
      } catch (error) {
        console.error("Error fetching products:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchProducts();
  }, []);

  if (loading) {
    return (
      <div className="text-center p-10 text-gray-500 text-lg">
        Loading products...
      </div>
    );
  }

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold text-blue-600 mb-6 text-center">
        All Products
      </h1>

      {products.length === 0 ? (
        <p className="text-center text-gray-500">No products found.</p>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
          {products.map((product) => (
            <ProductCard key={product.id} product={product} />
          ))}
        </div>
      )}
    </div>
  );
}

export default Products;
