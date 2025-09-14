// App.jsx
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import Home from "./pages/Home";
import Products from "./pages/Products";
import ProductDetail from "./pages/ProductDetail";
// ... other pages
import Cart from "./pages/Cart";             // <-- add this
import Checkout from "./pages/Checkout";     // <-- add this
import Login from "./pages/Login";           // <-- add this
import Signup from "./pages/Signup";       // <-- add this
import Profile from "./pages/Profile";       // <-- add this


function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/products" element={<Products />} />
        <Route path="/product/:id" element={<ProductDetail />} />
        <Route path="/cart" element={<Cart />} />
        <Route path="/checkout" element={<Checkout />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/profile" element={<Profile />} />
        
      </Routes>
      <Footer />
    </Router>
  );
}

export default App;
