import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Sidebar from '../components/Sidebar';
import Header from '../components/Header';
import { useCart } from '../CartContext';
import api from '../api';
import { Sparkles, TrendingUp, Package } from 'lucide-react';
import { toast } from 'sonner';

const RecommendationsPage = () => {
  const { cart, addToCart } = useCart();
  const [recommendations, setRecommendations] = useState(null);
  const [loading, setLoading] = useState(false);
  const [products, setProducts] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    fetchProducts();
    if (cart && cart.items && cart.items.length > 0) {
      generateRecommendations();
    }
  }, [cart]);

  const fetchProducts = async () => {
    try {
      const response = await api.get('/products');
      setProducts(response.data);
    } catch (error) {
      console.error('Failed to fetch products:', error);
    }
  };

  const generateRecommendations = async () => {
    if (!cart || !cart.items || cart.items.length === 0) {
      return;
    }

    try {
      setLoading(true);
      const cartItems = cart.items.map((item) => {
        const product = products.find((p) => p.id === item.product_id);
        return {
          product_id: item.product_id,
          name: product?.name || 'Unknown',
          category: product?.category || 'Unknown',
          brand: product?.brand || 'Unknown',
          price: item.price,
          quantity: item.quantity,
        };
      });

      const response = await api.post('/recommendations/analyze', {
        cart_items: cartItems,
        user_id: cart.user_id,
      });

      setRecommendations(response.data);
    } catch (error) {
      toast.error('Failed to generate recommendations');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleAddRecommended = async (productId) => {
    const result = await addToCart(productId, 1);
    if (result.success) {
      toast.success('Added to cart!');
      setTimeout(() => {
        generateRecommendations();
      }, 1000);
    } else {
      toast.error(result.error);
    }
  };

  const getProductDetails = (productId) => {
    return products.find((p) => p.id === productId);
  };

  if (!cart || !cart.items || cart.items.length === 0) {
    return (
      <div className="dashboard-layout">
        <Sidebar />
        <div className="main-content">
          <Header title="AI Recommendations" subtitle="Smart product suggestions for maximum savings" />
          <div className="page-content">
            <div className="text-center py-12">
              <Sparkles size={64} style={{ color: '#E4E4E7', margin: '0 auto 1rem' }} />
              <h3 className="text-xl font-medium mb-2" style={{ fontFamily: 'Outfit, sans-serif' }}>
                Add items to your cart first
              </h3>
              <p className="mb-6" style={{ color: '#52525B' }}>
                AI recommendations work best with at least one item in your cart
              </p>
              <button
                onClick={() => navigate('/products')}
                className="btn-primary"
                data-testid="goto-products-from-recommendations"
              >
                Browse Products
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard-layout">
      <Sidebar />
      <div className="main-content">
        <Header title="AI Recommendations" subtitle="Powered by Gemini 3 Flash" />
        <div className="page-content">
          {loading ? (
            <div className="text-center py-12">
              <div className="animate-pulse mb-4">
                <Sparkles size={64} style={{ color: '#002FA7', margin: '0 auto' }} />
              </div>
              <p style={{ color: '#52525B' }}>Analyzing your cart and generating recommendations...</p>
            </div>
          ) : recommendations ? (
            <div>
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 mb-6">
                <div className="card" data-testid="recommendation-stats">
                  <div className="flex items-center gap-3">
                    <div className="p-3 rounded-lg" style={{ background: '#002FA715' }}>
                      <TrendingUp size={24} style={{ color: '#002FA7' }} />
                    </div>
                    <div>
                      <p className="text-xs uppercase tracking-widest font-bold" style={{ color: '#52525B' }}>
                        Additional Spend
                      </p>
                      <p className="text-2xl font-medium" style={{ fontFamily: 'Outfit, sans-serif', color: '#002FA7' }}>
                        ₹{recommendations.additional_spend?.toFixed(2) || 0}
                      </p>
                    </div>
                  </div>
                </div>

                <div className="card">
                  <div className="flex items-center gap-3">
                    <div className="p-3 rounded-lg" style={{ background: '#16A34A15' }}>
                      <Package size={24} style={{ color: '#16A34A' }} />
                    </div>
                    <div>
                      <p className="text-xs uppercase tracking-widest font-bold" style={{ color: '#52525B' }}>
                        Discount Earned
                      </p>
                      <p className="text-2xl font-medium" style={{ fontFamily: 'Outfit, sans-serif', color: '#16A34A' }}>
                        ₹{recommendations.discount_earned?.toFixed(2) || 0}
                      </p>
                    </div>
                  </div>
                </div>

                <div className="card">
                  <div className="flex items-center gap-3">
                    <div className="p-3 rounded-lg" style={{ background: '#EAB30815' }}>
                      <Sparkles size={24} style={{ color: '#EAB308' }} />
                    </div>
                    <div>
                      <p className="text-xs uppercase tracking-widest font-bold" style={{ color: '#52525B' }}>
                        Savings %
                      </p>
                      <p className="text-2xl font-medium" style={{ fontFamily: 'Outfit, sans-serif', color: '#EAB308' }}>
                        {recommendations.savings_percentage?.toFixed(1) || 0}%
                      </p>
                    </div>
                  </div>
                </div>
              </div>

              <div className="recommendation-card" data-testid="ai-explanation">
                <h2 className="text-xl font-medium mb-3" style={{ fontFamily: 'Outfit, sans-serif', color: '#002FA7' }}>
                  AI Analysis & Explanation
                </h2>
                <p style={{ color: '#0A0A0A', lineHeight: '1.6' }}>
                  {recommendations.explanation}
                </p>
              </div>

              {recommendations.promotions_activated && recommendations.promotions_activated.length > 0 && (
                <div className="card mt-6" data-testid="activated-promotions">
                  <h3 className="text-lg font-medium mb-3" style={{ fontFamily: 'Outfit, sans-serif' }}>
                    Promotions Activated
                  </h3>
                  <div className="space-y-2">
                    {recommendations.promotions_activated.map((promo, idx) => (
                      <div key={idx} className="flex items-center gap-2">
                        <div className="w-2 h-2 rounded-full" style={{ background: '#16A34A' }}></div>
                        <p style={{ color: '#0A0A0A' }}>{promo}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {recommendations.recommended_products && recommendations.recommended_products.length > 0 && (
                <div className="mt-6">
                  <h2 className="text-2xl font-medium mb-4" style={{ fontFamily: 'Outfit, sans-serif' }}>
                    Recommended Products
                  </h2>
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6" data-testid="recommended-products">
                    {recommendations.recommended_products.map((recProduct) => {
                      const productDetails = getProductDetails(recProduct.product_id);
                      if (!productDetails) return null;

                      return (
                        <div
                          key={recProduct.product_id}
                          className="card"
                          style={{ border: '2px solid #002FA7' }}
                          data-testid={`recommended-product-${recProduct.product_id}`}
                        >
                          <img
                            src={productDetails.image_url}
                            alt={recProduct.name}
                            className="product-image mb-4"
                          />
                          <h3 className="text-lg font-medium mb-2" style={{ fontFamily: 'Outfit, sans-serif' }}>
                            {recProduct.name}
                          </h3>
                          <p className="text-2xl font-medium mb-3" style={{ color: '#002FA7', fontFamily: 'Outfit, sans-serif' }}>
                            ₹{recProduct.price}
                          </p>
                          <div className="explanation-box mb-3">
                            <p className="text-sm" style={{ color: '#52525B' }}>
                              {recProduct.reason}
                            </p>
                          </div>
                          <button
                            onClick={() => handleAddRecommended(recProduct.product_id)}
                            className="btn-primary w-full"
                            data-testid={`add-recommended-${recProduct.product_id}`}
                          >
                            Add to Cart
                          </button>
                        </div>
                      );
                    })}
                  </div>
                </div>
              )}

              <div className="mt-6 flex gap-4">
                <button
                  onClick={() => navigate('/cart')}
                  className="btn-secondary"
                  data-testid="back-to-cart-button"
                >
                  Back to Cart
                </button>
                <button
                  onClick={generateRecommendations}
                  className="btn-primary"
                  data-testid="refresh-recommendations-button"
                >
                  Refresh Recommendations
                </button>
              </div>
            </div>
          ) : (
            <div className="text-center py-12">
              <p style={{ color: '#52525B' }}>Click to generate recommendations</p>
              <button
                onClick={generateRecommendations}
                className="btn-primary mt-4"
                data-testid="generate-recommendations-button"
              >
                Generate Recommendations
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default RecommendationsPage;
