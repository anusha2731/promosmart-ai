import { useEffect, useState } from 'react';
import Sidebar from '../components/Sidebar';
import Header from '../components/Header';
import api from '../api';
import { Tag, ToggleLeft, ToggleRight } from 'lucide-react';
import { toast } from 'sonner';

const PromotionsPage = () => {
  const [promotions, setPromotions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showActiveOnly, setShowActiveOnly] = useState(false);

  useEffect(() => {
    fetchPromotions();
  }, [showActiveOnly]);

  const fetchPromotions = async () => {
    try {
      setLoading(true);
      const response = await api.get('/promotions', {
        params: { active_only: showActiveOnly }
      });
      setPromotions(response.data);
    } catch (error) {
      toast.error('Failed to fetch promotions');
    } finally {
      setLoading(false);
    }
  };

  const getPromoTypeColor = (type) => {
    const colors = {
      bundle: '#002FA7',
      threshold: '#16A34A',
      category: '#EAB308',
      brand: '#8B5CF6',
    };
    return colors[type] || '#52525B';
  };

  const getPromoTypeLabel = (type) => {
    return type.charAt(0).toUpperCase() + type.slice(1);
  };

  const formatDiscount = (promo) => {
    if (promo.discount_type === 'percentage') {
      return `${promo.discount_value}% OFF`;
    } else {
      return `₹${promo.discount_value} OFF`;
    }
  };

  const formatRules = (rules) => {
    const conditions = rules.conditions || {};
    if (rules.type === 'threshold') {
      return `Spend ₹${conditions.min_spend} or more`;
    } else if (rules.type === 'category') {
      return `Buy ${conditions.min_quantity} ${conditions.category} items`;
    } else if (rules.type === 'brand') {
      return `Buy ${conditions.min_quantity} ${conditions.brand} products`;
    } else if (rules.type === 'bundle') {
      return `Buy specific product combination`;
    }
    return 'Special offer';
  };

  return (
    <div className="dashboard-layout">
      <Sidebar />
      <div className="main-content">
        <Header title="Promotions" subtitle="Manage your promotional offers" />
        <div className="page-content">
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center gap-3">
              <button
                onClick={() => setShowActiveOnly(!showActiveOnly)}
                className="flex items-center gap-2 px-4 py-2 rounded-lg border border-gray-300"
                data-testid="toggle-active-promotions"
              >
                {showActiveOnly ? (
                  <ToggleRight size={20} style={{ color: '#002FA7' }} />
                ) : (
                  <ToggleLeft size={20} style={{ color: '#52525B' }} />
                )}
                <span>{showActiveOnly ? 'Showing Active Only' : 'Show All'}</span>
              </button>
            </div>
          </div>

          {loading ? (
            <p>Loading promotions...</p>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6" data-testid="promotions-grid">
              {promotions.map((promo) => (
                <div
                  key={promo.id}
                  className="card"
                  data-testid={`promo-card-${promo.id}`}
                  style={{
                    borderLeft: `4px solid ${getPromoTypeColor(promo.type)}`,
                  }}
                >
                  <div className="flex items-start justify-between mb-3">
                    <div className="flex items-center gap-2">
                      <Tag size={20} style={{ color: getPromoTypeColor(promo.type) }} />
                      <span
                        className="text-xs uppercase tracking-widest font-bold"
                        style={{ color: getPromoTypeColor(promo.type) }}
                      >
                        {getPromoTypeLabel(promo.type)}
                      </span>
                    </div>
                    <span className={`badge ${promo.active ? 'badge-success' : 'badge-error'}`}>
                      {promo.active ? 'Active' : 'Inactive'}
                    </span>
                  </div>

                  <h3 className="text-lg font-medium mb-2" style={{ fontFamily: 'Outfit, sans-serif' }}>
                    {promo.name}
                  </h3>

                  <p className="text-sm mb-3" style={{ color: '#52525B' }}>
                    {promo.description}
                  </p>

                  <div className="mb-3 p-3 rounded-lg" style={{ background: '#F9FAFB' }}>
                    <p className="text-xs uppercase tracking-widest font-bold mb-1" style={{ color: '#52525B' }}>
                      Condition
                    </p>
                    <p className="text-sm" style={{ color: '#0A0A0A' }}>
                      {formatRules(promo.rules)}
                    </p>
                  </div>

                  <div className="flex items-center justify-between">
                    <span className="text-2xl font-medium" style={{ color: '#002FA7', fontFamily: 'Outfit, sans-serif' }}>
                      {formatDiscount(promo)}
                    </span>
                    <span className="text-xs" style={{ color: '#52525B' }}>
                      Priority: {promo.priority}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          )}

          {!loading && promotions.length === 0 && (
            <div className="text-center py-12">
              <p style={{ color: '#52525B' }}>No promotions found</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default PromotionsPage;
