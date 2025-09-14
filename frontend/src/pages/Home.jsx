import React, { useEffect, useState } from "react";
import { getProducts } from "../api/products";
import ProductCard from "../components/ProductCard";
import SearchBar from "../components/SearchBar";

const Home = () => {
  const [products, setProducts] = useState([]);
  const [filtered, setFiltered] = useState([]);

  // Load products on mount
  useEffect(() => {
    const fetchData = async () => {
      try {
        const data = await getProducts();
        setProducts(data);
        setFiltered(data);
      } catch (error) {
        console.error("Error fetching products:", error);
      }
    };
    fetchData();
  }, []);

  // Search filter
  const handleSearch = (query) => {
    if (!query) {
      setFiltered(products);
    } else {
      setFiltered(
        products.filter((p) =>
          p.name.toLowerCase().includes(query.toLowerCase())
        )
      );
    }
  };

  return (
    <div className="p-6">
      {/* Hero Section */}
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-blue-600">Welcome to MyShop</h1>
        <p className="text-gray-600">Find the best products at the best prices!</p>
      </div>

      {/* Search */}
      <SearchBar onSearch={handleSearch} />

      {/* Product Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        {filtered.length > 0 ? (
          filtered.map((product) => (
            <ProductCard key={product.id} product={product} />
          ))
        ) : (
          <p className="col-span-full text-center text-gray-500">
            No products found.
          </p>
        )}
      </div>
    </div>
  );
};

export default Home;
