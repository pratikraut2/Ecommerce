// src/api/auth.js
import axiosInstance from "./axios";

// ✅ Signup
export const signup = async (username, email, password) => {
  const res = await axiosInstance.post("/auth/signup/", {
    username,
    email,
    password,
  });
  return res.data; // { user, access, refresh }
};

// ✅ Login
export const login = async (username, password) => {
  const res = await axiosInstance.post("/auth/login/", { username, password });

  if (res.data.access) {
    localStorage.setItem("access", res.data.access);
    localStorage.setItem("refresh", res.data.refresh);
  }

  return res.data;
};

// ✅ Get profile
export const getProfile = async () => {
  const res = await axiosInstance.get("/auth/profile/");
  return res.data;
};

// ✅ Logout
export const logout = () => {
  localStorage.removeItem("access");
  localStorage.removeItem("refresh");
};
