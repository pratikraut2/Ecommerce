import { useState, useEffect } from 'react';
import { useQuery } from '@tanstack/react-query';
import ProductCard from '../components/ProductCard';
import Navbar from '../components/Navbar';





export default function Home() {
  const [cartItems, setCartItems] = useState([]);

  // todo: replace with real API call
  const { data: products = [], isLoading } = useQuery({
    queryKey: ['/api/products'],
    queryFn: () => fetch('/api/products').then(res => res.json())
  });

  const handleAddToCart = (product) => {
    setCartItems(prev => [...prev, product]);
    console.log('Added to cart:', product);
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-background">
        <Navbar cartItemCount={cartItems.length} />
        <main className="pt-20 px-4">
          <div className="max-w-7xl mx-auto">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
              {[...Array(8)].map((_, i) => (
                <div key={i} className="bg-card rounded-lg h-96 animate-pulse" />
              ))}
            </div>
          </div>
        </main>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      <Navbar cartItemCount={cartItems.length} />
      <main className="pt-20 px-4">
        <div className="max-w-7xl mx-auto">
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-foreground mb-2" data-testid="text-page-title">
              Featured Products
            </h1>
            <p className="text-muted-foreground">
              Discover our latest collection of premium electronics and tech products
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {products.map((product) => (
              <ProductCard
                key={product.id}
                product={product}
                onAddToCart={handleAddToCart}
              />
            ))}
          </div>
        </div>
      </main>
    </div>
  );
}