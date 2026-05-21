import { useEffect, useState } from 'react';
import Sidebar from '../components/Sidebar';
import Header from '../components/Header';
import api from '../api';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

const AnalyticsPage = () => {
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);

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

  const COLORS = ['#002FA7', '#16A34A', '#EAB308', '#8B5CF6', '#F97316'];

  if (loading) {
    return (
      <div className="dashboard-layout">
        <Sidebar />
        <div className="main-content">
          <Header title="Analytics" subtitle="Insights and performance metrics" />
          <div className="page-content">
            <p>Loading analytics...</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard-layout">
      <Sidebar />
      <div className="main-content">
        <Header title="Analytics" subtitle="Data-driven insights for your retail business" />
        <div className="page-content">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
            <div className="card" data-testid="category-chart">
              <h3 className="text-xl font-medium mb-4" style={{ fontFamily: 'Outfit, sans-serif' }}>
                Products by Category
              </h3>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={analytics?.categories || []}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#E4E4E7" />
                  <XAxis dataKey="name" style={{ fontSize: '12px' }} />
                  <YAxis style={{ fontSize: '12px' }} />
                  <Tooltip />
                  <Bar dataKey="count" fill="#002FA7" />
                </BarChart>
              </ResponsiveContainer>
            </div>

            <div className="card" data-testid="brand-chart">
              <h3 className="text-xl font-medium mb-4" style={{ fontFamily: 'Outfit, sans-serif' }}>
                Products by Brand
              </h3>
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={analytics?.brands || []}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={(entry) => `${entry.name}: ${entry.count}`}
                    outerRadius={100}
                    fill="#8884d8"
                    dataKey="count"
                  >
                    {(analytics?.brands || []).map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="card" data-testid="promotion-stats">
              <h3 className="text-xl font-medium mb-4" style={{ fontFamily: 'Outfit, sans-serif' }}>
                Promotion Types Distribution
              </h3>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={analytics?.promotion_types || []}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#E4E4E7" />
                  <XAxis dataKey="type" style={{ fontSize: '12px', textTransform: 'capitalize' }} />
                  <YAxis style={{ fontSize: '12px' }} />
                  <Tooltip />
                  <Bar dataKey="count" fill="#16A34A" />
                </BarChart>
              </ResponsiveContainer>
            </div>

            <div className="card" data-testid="inventory-alerts">
              <h3 className="text-xl font-medium mb-4" style={{ fontFamily: 'Outfit, sans-serif' }}>
                Inventory Alerts
              </h3>
              <div className="space-y-3">
                {analytics?.low_stock_products && analytics.low_stock_products.length > 0 ? (
                  analytics.low_stock_products.map((product) => (
                    <div key={product.id} className="flex items-center justify-between p-3 rounded-lg" style={{ background: '#FEF3C7' }}>
                      <div>
                        <p style={{ color: '#0A0A0A', fontWeight: 500 }}>{product.name}</p>
                        <p className="text-xs" style={{ color: '#52525B' }}>
                          {product.category} • {product.brand}
                        </p>
                      </div>
                      <span className="badge badge-warning">{product.inventory} left</span>
                    </div>
                  ))
                ) : (
                  <p style={{ color: '#52525B' }}>All products are adequately stocked</p>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AnalyticsPage;