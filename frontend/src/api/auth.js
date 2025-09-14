
// src/api/auth.js
import axiosInstance from "./axios";

// ✅ POST /signup/ → create new user
export const signup = async (username, email, password) => {
  const res = await axiosInstance.post("/signup/", {
    username,
    email,
    password,
  });
  return res.data; // returns { user, access, refresh }
};

// ✅ POST /login/ → authenticate user
export const login = async (username, password) => {
  const res = await axiosInstance.post("/login/", {
    username,
    password,
  });

  if (res.data.access) {
    // Store tokens in localStorage
    localStorage.setItem("access", res.data.access);
    localStorage.setItem("refresh", res.data.refresh);
  }

  return res.data; // returns { user, access, refresh }
};

// ✅ GET /profile/ → get current logged-in user
export const getProfile = async () => {
  const res = await axiosInstance.get("/profile/");
  return res.data; // returns user details
};

// ✅ Logout → just clear tokens (no backend call needed)
export const logout = () => {
  localStorage.removeItem("access");
  localStorage.removeItem("refresh");
};
