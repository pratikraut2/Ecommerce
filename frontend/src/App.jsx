
import { Switch, Route } from "wouter";
import { queryClient } from "./lib/queryClient";
import { QueryClientProvider } from "@tanstack/react-query";
import { AuthProvider } from "./context/AuthContext";
import { CartProvider } from "./context/CartContext";

// Pages
import Home from "./pages/Home";
import Products from "./pages/Products";
import ProductDetail from "./pages/ProductDetail";
import Cart from "./pages/Cart";
import Checkout from "./pages/Checkout";
import Orders from "./pages/Orders";
import Signup from "./pages/Signup";
import Signin from "./pages/Signin";
import Login from "./pages/Login";
import Profile from "./pages/Profile";
import NotFound from "./pages/not-found";

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <CartProvider>
          <div className="min-h-screen bg-gray-50">
            <Switch>
              <Route path="/" component={Home} />
              <Route path="/products" component={Products} />
              <Route path="/product/:id" component={ProductDetail} />
              <Route path="/cart" component={Cart} />
              <Route path="/checkout" component={Checkout} />
              <Route path="/orders" component={Orders} />
              <Route path="/signup" component={Signup} />
              <Route path="/signin" component={Signin} />
              <Route path="/login" component={Login} />
              <Route path="/profile" component={Profile} />
              <Route component={NotFound} />
            </Switch>
          </div>
        </CartProvider>
      </AuthProvider>
    </QueryClientProvider>
  );
}

export default App;
