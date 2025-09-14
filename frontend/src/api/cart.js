// src/api/cart.js
import axiosInstance from "./axios";

// ✅ Get current user's cart
export const getCart = async () => {
  const res = await axiosInstance.get("/cart/");
  return res.data;
};

// ✅ Add product to cart
export const addToCart = async (productId, quantity = 1) => {
  const res = await axiosInstance.post(`/cart/add/${productId}/`, {
    quantity,
  });
  return res.data;
};

// ✅ Remove item from cart
export const removeFromCart = async (itemId) => {
  const res = await axiosInstance.delete(`/cart/remove/${itemId}/`);
  return res.data;
};
