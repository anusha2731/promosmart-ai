import { Link, useLocation } from 'react-router-dom';
import { Home, Package, Tag, ShoppingCart, Lightbulb, BarChart3, Settings, LogOut } from 'lucide-react';
import { useAuth } from '../AuthContext';

const Sidebar = () => {
  const location = useLocation();
  const { logout, user } = useAuth();

  const navItems = [
    { path: '/dashboard', label: 'Dashboard', icon: Home },
    { path: '/products', label: 'Products', icon: Package },
    { path: '/promotions', label: 'Promotions', icon: Tag },
    { path: '/cart', label: 'Cart Simulator', icon: ShoppingCart },
    { path: '/recommendations', label: 'Recommendations', icon: Lightbulb },
    { path: '/analytics', label: 'Analytics', icon: BarChart3 },
    { path: '/settings', label: 'Settings', icon: Settings },
  ];

  return (
    <div className="sidebar">
      <div className="p-6 border-b border-gray-200">
        <img
          src="https://static.prod-images.emergentagent.com/jobs/4b4426ad-0a51-424f-b61e-d333d18a9829/images/c267655e5a20db84937ee3b894efe117f0c8f8b8ee20a993f11113ad2ade5c7b.png"
          alt="PromoSmart AI"
          className="h-10 mb-2"
        />
        <h2 className="text-lg font-medium" style={{ fontFamily: 'Outfit, sans-serif', color: '#0A0A0A' }}>
          PromoSmart AI
        </h2>
      </div>

      <nav className="p-4">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = location.pathname === item.path;
          return (
            <Link
              key={item.path}
              to={item.path}
              data-testid={`nav-${item.label.toLowerCase().replace(' ', '-')}`}
              className="flex items-center px-4 py-3 mb-1 rounded-lg transition-all"
              style={{
                background: isActive ? '#002FA7' : 'transparent',
                color: isActive ? '#FFFFFF' : '#52525B',
                fontWeight: 500,
              }}
            >
              <Icon className="mr-3" size={20} />
              {item.label}
            </Link>
          );
        })}
      </nav>

      <div className="absolute bottom-0 left-0 right-0 p-4 border-t border-gray-200">
        <div className="px-4 py-2 mb-2">
          <p className="text-xs uppercase tracking-widest font-bold" style={{ color: '#52525B' }}>
            Logged in as
          </p>
          <p className="text-sm font-medium mt-1" style={{ color: '#0A0A0A' }}>
            {user?.name || user?.email}
          </p>
        </div>
        <button
          onClick={logout}
          data-testid="logout-button"
          className="flex items-center w-full px-4 py-3 rounded-lg transition-all"
          style={{ background: '#FEE2E2', color: '#DC2626', fontWeight: 500 }}
        >
          <LogOut className="mr-3" size={20} />
          Logout
        </button>
      </div>
    </div>
  );
};

export default Sidebar;