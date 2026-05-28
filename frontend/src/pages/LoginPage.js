import { useState } from 'react';
import { useAuth } from '../AuthContext';
import { useNavigate } from 'react-router-dom';
import { toast } from 'sonner';

const LoginPage = () => {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [loading, setLoading] = useState(false);
  const { login, register } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    if (isLogin) {
      const result = await login(email, password);
      if (result.success) {
        toast.success('Login successful!');
        navigate('/dashboard');
      } else {
        toast.error(result.error);
      }
    } else {
      if (!name || !email || !password) {
        toast.error('Please fill all fields');
        setLoading(false);
        return;
      }
      const result = await register(name, email, password);
      if (result.success) {
        toast.success('Registration successful!');
        navigate('/dashboard');
      } else {
        toast.error(result.error);
      }
    }
    setLoading(false);
  };

  return (
    <div className="login-page">
      <div className="w-full max-w-md px-6">
        <div className="bg-white shadow-2xl rounded-3xl p-10" style={{ border: '1px solid #E4E4E7', borderRadius: '8px', padding: '3rem' }}>
          <div className="text-center mb-8">
            <img
              src="https://static.prod-images.emergentagent.com/jobs/4b4426ad-0a51-424f-b61e-d333d18a9829/images/c267655e5a20db84937ee3b894efe117f0c8f8b8ee20a993f11113ad2ade5c7b.png"
              alt="PromoSmart AI"
              className="h-20 w-auto mx-auto mb-6"
            />
            <h1 className="text-6xl text-red-500 font-bold" style={{ fontFamily: 'Outfit, sans-serif', color: '#0A0A0A' }}>
              PromoSmart AI
            </h1>
            <p className="text-sm mt-2" style={{ color: '#52525B' }}>
              AI-Powered Retail Promotion Optimizer
            </p>
          </div>

          <form onSubmit={handleSubmit} data-testid="login-form">
            {!isLogin && (
              <div className="mb-4">
                <label className="block text-xs tracking-widest uppercase font-bold mb-2" style={{ color: '#52525B' }}>
                  Name
                </label>
                <input
                  type="text"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600"
                  placeholder="Enter your name"
                  data-testid="name-input"
                  style={{ fontFamily: 'IBM Plex Sans, sans-serif' }}
                />
              </div>
            )}

            <div className="mb-4">
              <label className="block text-xs tracking-widest uppercase font-bold mb-2" style={{ color: '#52525B' }}>
                Email
              </label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600"
                placeholder="Enter your email"
                data-testid="email-input"
                style={{ fontFamily: 'IBM Plex Sans, sans-serif' }}
              />
            </div>

            <div className="mb-6">
              <label className="block text-xs tracking-widest uppercase font-bold mb-2" style={{ color: '#52525B' }}>
                Password
              </label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600"
                placeholder="Enter your password"
                data-testid="password-input"
                style={{ fontFamily: 'IBM Plex Sans, sans-serif' }}
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="btn-primary w-full"
              data-testid="submit-button"
              style={{ padding: '0.875rem', fontSize: '1rem' }}
            >
              {loading ? 'Processing...' : isLogin ? 'Sign In' : 'Create Account'}
            </button>
          </form>

          <div className="mt-6 text-center">
            <button
              onClick={() => setIsLogin(!isLogin)}
              className="text-sm"
              style={{ color: '#002FA7', fontWeight: 500 }}
              data-testid="toggle-auth-mode"
            >
              {isLogin ? "Don't have an account? Sign Up" : 'Already have an account? Sign In'}
            </button>
          </div>

          <div className="mt-6 p-4 bg-gray-50 rounded-lg">
            <p className="text-xs font-bold mb-2" style={{ color: '#52525B', textTransform: 'uppercase', letterSpacing: '0.1em' }}>
              Demo Credentials
            </p>
            <p className="text-sm" style={{ fontFamily: 'monospace', color: '#0A0A0A' }}>
              admin@promosmart.com / Admin@123
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;