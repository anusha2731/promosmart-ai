import Sidebar from '../components/Sidebar';
import Header from '../components/Header';
import { useAuth } from '../AuthContext';

const SettingsPage = () => {
  const { user } = useAuth();

  return (
    <div className="dashboard-layout">
      <Sidebar />
      <div className="main-content">
        <Header title="Settings" subtitle="Manage your account and preferences" />
        <div className="page-content">
          <div className="card" data-testid="user-info">
            <h3 className="text-xl font-medium mb-4" style={{ fontFamily: 'Outfit, sans-serif' }}>
              User Information
            </h3>
            <div className="space-y-4">
              <div>
                <label className="text-xs uppercase tracking-widest font-bold" style={{ color: '#52525B' }}>
                  Name
                </label>
                <p className="mt-1" style={{ color: '#0A0A0A' }}>{user?.name}</p>
              </div>
              <div>
                <label className="text-xs uppercase tracking-widest font-bold" style={{ color: '#52525B' }}>
                  Email
                </label>
                <p className="mt-1" style={{ color: '#0A0A0A' }}>{user?.email}</p>
              </div>
              <div>
                <label className="text-xs uppercase tracking-widest font-bold" style={{ color: '#52525B' }}>
                  Role
                </label>
                <p className="mt-1">
                  <span className="badge badge-success">{user?.role}</span>
                </p>
              </div>
            </div>
          </div>

          <div className="card mt-6" data-testid="app-info">
            <h3 className="text-xl font-medium mb-4" style={{ fontFamily: 'Outfit, sans-serif' }}>
              About PromoSmart AI
            </h3>
            <p style={{ color: '#52525B', lineHeight: '1.6' }}>
              PromoSmart AI is an AI-powered retail promotion optimization platform that helps sales associates recommend products to maximize customer savings while boosting revenue.
            </p>
            <div className="mt-4 p-4 rounded-lg" style={{ background: '#F9FAFB' }}>
              <p className="text-xs uppercase tracking-widest font-bold mb-2" style={{ color: '#52525B' }}>
                Powered By
              </p>
              <p style={{ color: '#0A0A0A' }}>Google Gemini 3 Flash • FastAPI • React • MongoDB</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SettingsPage;