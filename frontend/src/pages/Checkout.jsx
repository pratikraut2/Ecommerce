// src/pages/Checkout.jsx
import React, { useState, useEffect } from "react";
import axiosInstance from "../api/axios"; // your axios setup
import { useNavigate } from "react-router-dom";

export default function Checkout() {
  const [cart, setCart] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [shippingAddress, setShippingAddress] = useState("");
  const [paymentMethod, setPaymentMethod] = useState("COD");

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

  const handleCheckout = async (e) => {
    e.preventDefault();
    try {
      await axiosInstance.post("/orders/create/", {
        shipping_address: shippingAddress,
        payment_method: paymentMethod,
      });
      alert("Order placed successfully!");
      navigate("/"); // redirect to home after order
    } catch (err) {
        setError("Checkout failed. Please try again.");
        console.error("Checkout error:", err);
    }
  };

  if (loading) {
    return (
      <div className="text-center p-10 text-gray-500 text-lg">
        Loading checkout...
      </div>
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
        Your cart is empty.
      </div>
    );
  }

  return (
    <div className="p-6 max-w-lg mx-auto bg-white shadow rounded">
      <h1 className="text-3xl font-bold text-blue-600 mb-6 text-center">
        Checkout
      </h1>

      <div className="mb-4">
        <h2 className="font-semibold mb-2">Your Items:</h2>
        <ul className="space-y-2">
          {cart.items.map((item) => (
            <li
              key={item.id}
              className="flex justify-between bg-gray-100 p-2 rounded"
            >
              <span>{item.product.name} x {item.quantity}</span>
              <span>${item.unit_price * item.quantity}</span>
            </li>
          ))}
        </ul>
        <p className="text-right font-bold mt-2">
          Total: ${cart.total_amount || 0}
        </p>
      </div>

      <form onSubmit={handleCheckout} className="space-y-4">
        <div>
          <label className="block mb-1 font-medium">Shipping Address</label>
          <textarea
            className="w-full border rounded p-2"
            value={shippingAddress}
            onChange={(e) => setShippingAddress(e.target.value)}
            required
          />
        </div>

        <div>
          <label className="block mb-1 font-medium">Payment Method</label>
          <select
            className="w-full border rounded p-2"
            value={paymentMethod}
            onChange={(e) => setPaymentMethod(e.target.value)}
          >
            <option value="COD">Cash on Delivery</option>
            <option value="Card">Card Payment</option>
          </select>
        </div>

        <button
          type="submit"
          className="w-full bg-blue-600 hover:bg-blue-700 text-white py-2 rounded"
        >
          Place Order
        </button>
      </form>
    </div>
  );
}
