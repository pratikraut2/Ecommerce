// src/api/products.js
import axiosInstance from "./axios";

// ✅ GET /products/ → list all active products
export const getProducts = async () => {
  const res = await axiosInstance.get("/products/");
  return res.data;
};

// ✅ GET /products/:id/ → get single product details
export const getProductDetail = async (id) => {
  const res = await axiosInstance.get(`/products/${id}/`);
  return res.data;
};

// ✅ GET /categories/ → list all categories
export const getCategories = async () => {
  const res = await axiosInstance.get("/categories/");
  return res.data;
};
