// src/pages/Cart.jsx
import React, { useEffect, useState } from "react";
import axiosInstance from "../api/axios"; // your axios setup
import { useNavigate, Link } from "react-router-dom";

export default function Cart() {
  const [cart, setCart] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  // Fetch cart on mount
  useEffect(() => {
    const fetchCart = async () => {
      try {
        const res = await axiosInstance.get("/cart/");
        setCart(res.data);
      } catch (err) {
        setError("Failed to fetch cart");
        console.error("Cart fetch error:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchCart();
  }, []);

  const handleRemove = async (itemId) => {
    try {
      await axiosInstance.delete(`/cart/items/${itemId}/`);
      // Update cart locally
      setCart((prev) => ({
        ...prev,
        items: prev.items.filter((item) => item.id !== itemId),
      }));
    } catch (err) {
      alert("Failed to remove item");
        console.error("Remove item error:", err);
    }
  };

  const handleCheckout = () => {
    navigate("/checkout");
  };

  if (loading) {
    return (
      <div className="text-center p-10 text-gray-500 text-lg">Loading cart...</div>
    );
  }

  if (error) {
    return (
      <div className="text-center p-10 text-red-500 text-lg">{error}</div>
    );
  }

  if (!cart || cart.items.length === 0) {
    return (
      <div className="text-center p-10 text-gray-500 text-lg">
        Your cart is empty. <Link to="/products" className="text-blue-500 underline">Shop now</Link>
      </div>
    );
  }

  return (
    <div className="p-6 max-w-3xl mx-auto bg-white shadow rounded">
      <h1 className="text-3xl font-bold text-blue-600 mb-6 text-center">Your Cart</h1>

      <ul className="space-y-4">
        {cart.items.map((item) => (
          <li
            key={item.id}
            className="flex justify-between items-center bg-gray-100 p-4 rounded"
          >
            <div>
              <h2 className="font-semibold">{item.product.name}</h2>
              <p className="text-gray-500">Qty: {item.quantity}</p>
            </div>
            <div className="flex items-center gap-4">
              <span className="font-bold">${item.unit_price * item.quantity}</span>
              <button
                onClick={() => handleRemove(item.id)}
                className="text-red-600 hover:underline"
              >
                Remove
              </button>
            </div>
          </li>
        ))}
      </ul>

      <div className="mt-6 text-right">
        <p className="text-xl font-bold">Total: ${cart.total_amount || 0}</p>
        <button
          onClick={handleCheckout}
          className="mt-4 w-full md:w-auto bg-blue-600 hover:bg-blue-700 text-white py-2 px-6 rounded"
        >
          Proceed to Checkout
        </button>
      </div>
    </div>
  );
}
