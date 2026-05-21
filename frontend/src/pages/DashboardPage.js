import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Sidebar from '../components/Sidebar';
import Header from '../components/Header';
import api from '../api';
import { Package, Tag, Users, AlertTriangle } from 'lucide-react';

const DashboardPage = () => {
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    fetchAnalytics();
  }, []);

  const fetchAnalytics = async () => {
    try {
      const response = await api.get('/analytics');
      setAnalytics(response.data);
    } catch (error) {
      console.error('Failed to fetch analytics:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="dashboard-layout">
        <Sidebar />
        <div className="main-content">
          <Header title="Dashboard" subtitle="Welcome to PromoSmart AI" />
          <div className="page-content">
            <p>Loading...</p>
          </div>
        </div>
      </div>
    );
  }

  const stats = [
    {
      label: 'Total Products',
      value: analytics?.overview?.total_products || 0,
      icon: Package,
      color: '#002FA7',
      testId: 'stat-total-products',
    },
    {
      label: 'Active Promotions',
      value: analytics?.overview?.total_active_promotions || 0,
      icon: Tag,
      color: '#16A34A',
      testId: 'stat-active-promotions',
    },
    {
      label: 'Total Users',
      value: analytics?.overview?.total_users || 0,
      icon: Users,
      color: '#EAB308',
      testId: 'stat-total-users',
    },
    {
      label: 'Low Stock Items',
      value: analytics?.overview?.low_stock_items || 0,
      icon: AlertTriangle,
      color: '#FF2A00',
      testId: 'stat-low-stock',
    },
  ];

  return (
    <div className="dashboard-layout">
      <Sidebar />
      <div className="main-content">
        <Header title="Dashboard" subtitle="AI-Powered Retail Promotion Optimizer" />
        <div className="page-content">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            {stats.map((stat) => {
              const Icon = stat.icon;
              return (
                <div key={stat.label} className="stat-card" data-testid={stat.testId}>
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-xs uppercase tracking-widest font-bold mb-2" style={{ color: '#52525B' }}>
                        {stat.label}
                      </p>
                      <p className="text-4xl font-medium" style={{ fontFamily: 'Outfit, sans-serif', color: stat.color }}>
                        {stat.value}
                      </p>
                    </div>
                    <div
                      className="p-3 rounded-lg"
                      style={{ background: `${stat.color}15` }}
                    >
                      <Icon size={32} style={{ color: stat.color }} />
                    </div>
                  </div>
                </div>
              );
            })}
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
            <div className="card" data-testid="category-distribution">
              <h3 className="text-xl font-medium mb-4" style={{ fontFamily: 'Outfit, sans-serif' }}>
                Category Distribution
              </h3>
              <div className="space-y-3">
                {analytics?.categories?.slice(0, 5).map((cat) => (
                  <div key={cat.name} className="flex items-center justify-between">
                    <span style={{ color: '#52525B' }}>{cat.name}</span>
                    <span className="font-medium" style={{ color: '#002FA7' }}>
                      {cat.count} products
                    </span>
                  </div>
                ))}
              </div>
            </div>

            <div className="card" data-testid="brand-distribution">
              <h3 className="text-xl font-medium mb-4" style={{ fontFamily: 'Outfit, sans-serif' }}>
                Top Brands
              </h3>
              <div className="space-y-3">
                {analytics?.brands?.slice(0, 5).map((brand) => (
                  <div key={brand.name} className="flex items-center justify-between">
                    <span style={{ color: '#52525B' }}>{brand.name}</span>
                    <span className="font-medium" style={{ color: '#002FA7' }}>
                      {brand.count} products
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="card" data-testid="promotion-types">
              <h3 className="text-xl font-medium mb-4" style={{ fontFamily: 'Outfit, sans-serif' }}>
                Promotion Types
              </h3>
              <div className="space-y-3">
                {analytics?.promotion_types?.map((promo) => (
                  <div key={promo.type} className="flex items-center justify-between">
                    <span style={{ color: '#52525B', textTransform: 'capitalize' }}>{promo.type}</span>
                    <span className="badge badge-success">{promo.count} active</span>
                  </div>
                ))}
              </div>
            </div>

            <div className="card" data-testid="low-stock-alert">
              <h3 className="text-xl font-medium mb-4" style={{ fontFamily: 'Outfit, sans-serif' }}>
                Low Stock Alert
              </h3>
              <div className="space-y-3">
                {analytics?.low_stock_products?.length > 0 ? (
                  analytics.low_stock_products.map((product) => (
                    <div key={product.id} className="flex items-center justify-between">
                      <div>
                        <p style={{ color: '#0A0A0A', fontWeight: 500 }}>{product.name}</p>
                        <p className="text-xs" style={{ color: '#52525B' }}>
                          {product.category}
                        </p>
                      </div>
                      <span className="badge badge-warning">{product.inventory} left</span>
                    </div>
                  ))
                ) : (
                  <p style={{ color: '#52525B' }}>All products are well stocked</p>
                )}
              </div>
            </div>
          </div>

          <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-4">
            <button
              onClick={() => navigate('/products')}
              className="btn-primary"
              data-testid="goto-products-button"
            >
              Manage Products
            </button>
            <button
              onClick={() => navigate('/promotions')}
              className="btn-primary"
              data-testid="goto-promotions-button"
            >
              Manage Promotions
            </button>
            <button
              onClick={() => navigate('/cart')}
              className="btn-primary"
              data-testid="goto-cart-button"
            >
              Start Cart Simulation
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;