// src/api/orders.js
import axiosInstance from "./axios";

// ✅ Create a new order (from current cart)
export const createOrder = async (shipping_address, payment_method = "COD") => {
  const res = await axiosInstance.post("/orders/create/", {
    shipping_address,
    payment_method,
  });
  return res.data;
};

// ✅ Get details of a specific order
export const getOrderDetail = async (orderId) => {
  const res = await axiosInstance.get(`/orders/${orderId}/`);
  return res.data;
};
