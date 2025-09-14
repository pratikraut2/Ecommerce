import React from "react";
import { Link } from "react-router-dom";

const Footer = () => {
  return (
    <footer className="footer">
      <div className="footer-content">

        {/* Left Section */}
        <div className="footer-left">
          <h2>MyShop</h2>
          <p>Best products at the best prices!</p>
        </div>

        {/* Center Section */}
        <div className="footer-links">
          <Link to="/">Home</Link>
          <Link to="/products">Products</Link>
          <Link to="/cart">Cart</Link>
          <Link to="/orders">Orders</Link>
          <Link to="/profile">Profile</Link>
        </div>

        {/* Right Section */}
        <div className="footer-right">
          <p>📧 support@myshop.com</p>
          <p>📞 +91 98765 43210</p>
        </div>
      </div>

      {/* Bottom Strip */}
      <div className="footer-bottom">
        <p>© {new Date().getFullYear()} MyShop. All rights reserved.</p>
      </div>
    </footer>
  );
};

export default Footer;
