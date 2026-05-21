import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Sidebar from '../components/Sidebar';
import Header from '../components/Header';
import { useCart } from '../CartContext';
import api from '../api';
import { ShoppingCart, Trash2, Plus, Minus, Sparkles } from 'lucide-react';
import { toast } from 'sonner';

const CartPage = () => {
  const { cart, removeFromCart, addToCart, fetchCart } = useCart();
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      await fetchCart();
      const productsRes = await api.get('/products');
      setProducts(productsRes.data);
    } catch (error) {
      toast.error('Failed to fetch data');
    } finally {
      setLoading(false);
    }
  };

  const getProductDetails = (productId) => {
    return products.find((p) => p.id === productId);
  };

  const handleQuantityChange = async (productId, newQuantity) => {
    if (newQuantity < 1) return;
    const result = await addToCart(productId, newQuantity);
    if (!result.success) {
      toast.error(result.error);
    }
  };

  const handleRemove = async (productId) => {
    const result = await removeFromCart(productId);
    if (result.success) {
      toast.success('Removed from cart');
    } else {
      toast.error(result.error);
    }
  };

  const handleGetRecommendations = () => {
    navigate('/recommendations');
  };

  if (loading) {
    return (
      <div className="dashboard-layout">
        <Sidebar />
        <div className="main-content">
          <Header title="Cart Simulator" subtitle="Build and optimize your shopping cart" />
          <div className="page-content">
            <p>Loading cart...</p>
          </div>
        </div>
      </div>
    );
  }

  const cartItems = cart?.items || [];
  const isEmpty = cartItems.length === 0;

  return (
    <div className="dashboard-layout">
      <Sidebar />
      <div className="main-content">
        <Header title="Cart Simulator" subtitle="Optimize your cart for maximum savings" />
        <div className="page-content">
          {isEmpty ? (
            <div className="text-center py-12">
              <ShoppingCart size={64} style={{ color: '#E4E4E7', margin: '0 auto 1rem' }} />
              <h3 className="text-xl font-medium mb-2" style={{ fontFamily: 'Outfit, sans-serif' }}>
                Your cart is empty
              </h3>
              <p className="mb-6" style={{ color: '#52525B' }}>
                Add products to see promotions and recommendations
              </p>
              <button
                onClick={() => navigate('/products')}
                className="btn-primary"
                data-testid="goto-products-from-empty-cart"
              >
                Browse Products
              </button>
            </div>
          ) : (
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <div className="lg:col-span-2">
                <div className="card">
                  <h2 className="text-xl font-medium mb-4" style={{ fontFamily: 'Outfit, sans-serif' }}>
                    Cart Items ({cartItems.length})
                  </h2>
                  <div className="space-y-4" data-testid="cart-items-list">
                    {cartItems.map((item) => {
                      const product = getProductDetails(item.product_id);
                      if (!product) return null;

                      return (
                        <div
                          key={item.product_id}
                          className="flex items-center gap-4 p-4 border border-gray-200 rounded-lg"
                          data-testid={`cart-item-${item.product_id}`}
                        >
                          <img
                            src={product.image_url}
                            alt={product.name}
                            className="w-20 h-20 object-cover rounded-lg"
                          />
                          <div className="flex-1">
                            <h4 className="font-medium" style={{ color: '#0A0A0A' }}>
                              {product.name}
                            </h4>
                            <p className="text-sm" style={{ color: '#52525B' }}>
                              {product.brand} • {product.category}
                            </p>
                            <p className="text-lg font-medium mt-1" style={{ color: '#002FA7', fontFamily: 'Outfit, sans-serif' }}>
                              ₹{item.price}
                            </p>
                          </div>
                          <div className="flex items-center gap-2">
                            <button
                              onClick={() => handleQuantityChange(item.product_id, item.quantity - 1)}
                              className="p-2 rounded-lg border border-gray-300"
                              data-testid={`decrease-qty-${item.product_id}`}
                            >
                              <Minus size={16} />
                            </button>
                            <span className="w-12 text-center font-medium">{item.quantity}</span>
                            <button
                              onClick={() => handleQuantityChange(item.product_id, item.quantity + 1)}
                              className="p-2 rounded-lg border border-gray-300"
                              data-testid={`increase-qty-${item.product_id}`}
                            >
                              <Plus size={16} />
                            </button>
                          </div>
                          <button
                            onClick={() => handleRemove(item.product_id)}
                            className="p-2 rounded-lg"
                            style={{ color: '#FF2A00' }}
                            data-testid={`remove-item-${item.product_id}`}
                          >
                            <Trash2 size={20} />
                          </button>
                        </div>
                      );
                    })}
                  </div>
                </div>
              </div>

              <div>
                <div className="card sticky top-24" data-testid="cart-summary">
                  <h2 className="text-xl font-medium mb-4" style={{ fontFamily: 'Outfit, sans-serif' }}>
                    Cart Summary
                  </h2>

                  <div className="space-y-3 mb-4">
                    <div className="flex justify-between">
                      <span style={{ color: '#52525B' }}>Subtotal</span>
                      <span className="font-medium">₹{cart.subtotal?.toFixed(2)}</span>
                    </div>
                    
                    {cart.discount > 0 && (
                      <div className="flex justify-between" style={{ color: '#16A34A' }}>
                        <span>Discount</span>
                        <span className="font-medium">-₹{cart.discount?.toFixed(2)}</span>
                      </div>
                    )}

                    <div className="border-t border-gray-200 pt-3 flex justify-between">
                      <span className="text-lg font-medium" style={{ fontFamily: 'Outfit, sans-serif' }}>
                        Total
                      </span>
                      <span className="text-2xl font-medium" style={{ color: '#002FA7', fontFamily: 'Outfit, sans-serif' }}>
                        ₹{cart.total?.toFixed(2)}
                      </span>
                    </div>
                  </div>

                  {cart.applied_promotions && cart.applied_promotions.length > 0 && (
                    <div className="mb-4 p-3 rounded-lg" style={{ background: '#DCFCE7' }}>
                      <p className="text-xs uppercase tracking-widest font-bold mb-2" style={{ color: '#16A34A' }}>
                        Applied Promotions
                      </p>
                      {cart.applied_promotions.map((promo, idx) => (
                        <p key={idx} className="text-sm mb-1" style={{ color: '#0A0A0A' }}>
                          • {promo}
                        </p>
                      ))}
                    </div>
                  )}

                  <button
                    onClick={handleGetRecommendations}
                    className="btn-primary w-full flex items-center justify-center gap-2"
                    data-testid="get-recommendations-button"
                  >
                    <Sparkles size={20} />
                    Get AI Recommendations
                  </button>

                  {cart.discount > 0 && (
                    <div className="mt-4 p-3 rounded-lg" style={{ background: '#F9FAFB' }}>
                      <p className="text-sm text-center" style={{ color: '#16A34A', fontWeight: 500 }}>
                        You're saving ₹{cart.discount?.toFixed(2)}!
                      </p>
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default CartPage;
