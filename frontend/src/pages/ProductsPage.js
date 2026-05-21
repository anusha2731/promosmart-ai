import { useEffect, useState } from 'react';
import Sidebar from '../components/Sidebar';
import Header from '../components/Header';
import api from '../api';
import { Plus, Edit2, Trash2, Search } from 'lucide-react';
import { toast } from 'sonner';
import { useCart } from '../CartContext';

const ProductsPage = () => {
  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [brands, setBrands] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterCategory, setFilterCategory] = useState('');
  const [filterBrand, setFilterBrand] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [editingProduct, setEditingProduct] = useState(null);
  const { addToCart } = useCart();

  useEffect(() => {
    fetchData();
  }, [filterCategory, filterBrand]);

  const fetchData = async () => {
    try {
      setLoading(true);
      const params = {};
      if (filterCategory) params.category = filterCategory;
      if (filterBrand) params.brand = filterBrand;
      
      const [productsRes, categoriesRes, brandsRes] = await Promise.all([
        api.get('/products', { params }),
        api.get('/categories'),
        api.get('/brands'),
      ]);
      
      setProducts(productsRes.data);
      setCategories(categoriesRes.data);
      setBrands(brandsRes.data);
    } catch (error) {
      toast.error('Failed to fetch data');
    } finally {
      setLoading(false);
    }
  };

  const handleAddToCart = async (productId) => {
    const result = await addToCart(productId, 1);
    if (result.success) {
      toast.success('Added to cart!');
    } else {
      toast.error(result.error);
    }
  };

  const handleDelete = async (productId) => {
    if (!window.confirm('Are you sure you want to delete this product?')) return;
    
    try {
      await api.delete(`/products/${productId}`);
      toast.success('Product deleted');
      fetchData();
    } catch (error) {
      toast.error('Failed to delete product');
    }
  };

  const filteredProducts = products.filter((product) =>
    product.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="dashboard-layout">
      <Sidebar />
      <div className="main-content">
        <Header title="Products" subtitle="Manage your product catalog" />
        <div className="page-content">
          <div className="flex flex-wrap gap-4 mb-6">
            <div className="flex-1 min-w-[250px]">
              <div className="relative">
                <Search className="absolute left-3 top-3" size={20} style={{ color: '#52525B' }} />
                <input
                  type="text"
                  placeholder="Search products..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg"
                  data-testid="search-products-input"
                />
              </div>
            </div>

            <select
              value={filterCategory}
              onChange={(e) => setFilterCategory(e.target.value)}
              className="px-4 py-3 border border-gray-300 rounded-lg"
              data-testid="filter-category"
            >
              <option value="">All Categories</option>
              {categories.map((cat) => (
                <option key={cat.id} value={cat.name}>{cat.name}</option>
              ))}
            </select>

            <select
              value={filterBrand}
              onChange={(e) => setFilterBrand(e.target.value)}
              className="px-4 py-3 border border-gray-300 rounded-lg"
              data-testid="filter-brand"
            >
              <option value="">All Brands</option>
              {brands.map((brand) => (
                <option key={brand.id} value={brand.name}>{brand.name}</option>
              ))}
            </select>
          </div>

          {loading ? (
            <p>Loading products...</p>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6" data-testid="products-grid">
              {filteredProducts.map((product) => (
                <div key={product.id} className="card" data-testid={`product-card-${product.id}`}>
                  <img
                    src={product.image_url}
                    alt={product.name}
                    className="product-image mb-4"
                  />
                  <h3 className="text-lg font-medium mb-1" style={{ fontFamily: 'Outfit, sans-serif' }}>
                    {product.name}
                  </h3>
                  <p className="text-xs mb-2" style={{ color: '#52525B' }}>
                    {product.brand} • {product.category}
                  </p>
                  <div className="flex items-center justify-between mb-3">
                    <span className="text-2xl font-medium" style={{ color: '#002FA7', fontFamily: 'Outfit, sans-serif' }}>
                      ₹{product.price}
                    </span>
                    <span className={`badge ${product.inventory > 10 ? 'badge-success' : 'badge-warning'}`}>
                      {product.inventory} in stock
                    </span>
                  </div>
                  <div className="flex gap-2">
                    <button
                      onClick={() => handleAddToCart(product.id)}
                      className="btn-primary flex-1"
                      data-testid={`add-to-cart-${product.id}`}
                    >
                      Add to Cart
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}

          {!loading && filteredProducts.length === 0 && (
            <div className="text-center py-12">
              <p style={{ color: '#52525B' }}>No products found</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ProductsPage;
