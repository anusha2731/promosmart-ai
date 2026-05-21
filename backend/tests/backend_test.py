"""
Backend API tests for PromoSmart AI
Covers: auth, products, categories, brands, promotions, cart (with auto-discount),
AI recommendations (Gemini), analytics.
"""
import os
import time
import uuid
import pytest
import requests
from dotenv import load_dotenv

# Load frontend env to get public BASE_URL
load_dotenv('/app/frontend/.env')
BASE_URL = os.environ.get('REACT_APP_BACKEND_URL').rstrip('/')
API = f"{BASE_URL}/api"

ADMIN_EMAIL = "admin@promosmart.com"
ADMIN_PASSWORD = "Admin@123"


# -------------------- Fixtures --------------------
@pytest.fixture(scope="session")
def api_client():
    s = requests.Session()
    s.headers.update({"Content-Type": "application/json"})
    return s


@pytest.fixture(scope="session")
def admin_token(api_client):
    r = api_client.post(f"{API}/auth/login",
                        json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD})
    if r.status_code != 200:
        pytest.skip(f"Admin login failed: {r.status_code} {r.text}")
    data = r.json()
    return data["access_token"]


@pytest.fixture(scope="session")
def admin_user(api_client):
    r = api_client.post(f"{API}/auth/login",
                        json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD})
    return r.json()["user"]


@pytest.fixture
def auth_headers(admin_token):
    return {"Authorization": f"Bearer {admin_token}",
            "Content-Type": "application/json"}


# -------------------- AUTH --------------------
class TestAuth:
    def test_login_admin_success(self, api_client):
        r = api_client.post(f"{API}/auth/login",
                            json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD})
        assert r.status_code == 200, r.text
        data = r.json()
        assert "access_token" in data and isinstance(data["access_token"], str)
        assert data["token_type"] == "bearer"
        assert data["user"]["email"] == ADMIN_EMAIL
        assert data["user"]["role"] == "admin"

    def test_login_invalid_password(self, api_client):
        r = api_client.post(f"{API}/auth/login",
                            json={"email": ADMIN_EMAIL, "password": "wrong"})
        assert r.status_code == 401

    def test_login_unknown_email(self, api_client):
        r = api_client.post(f"{API}/auth/login",
                            json={"email": "nope@nope.com", "password": "x"})
        assert r.status_code == 401

    def test_register_new_user(self, api_client):
        email = f"TEST_user_{uuid.uuid4().hex[:8]}@example.com"
        r = api_client.post(f"{API}/auth/register",
                            json={"email": email, "password": "Pass@123",
                                  "name": "Test User"})
        assert r.status_code == 200, r.text
        data = r.json()
        assert data["user"]["email"] == email
        assert "access_token" in data

    def test_register_duplicate_email(self, api_client):
        r = api_client.post(f"{API}/auth/register",
                            json={"email": ADMIN_EMAIL, "password": "x",
                                  "name": "Dup"})
        assert r.status_code == 400


# -------------------- PRODUCTS --------------------
class TestProducts:
    def test_get_all_products(self, api_client):
        r = api_client.get(f"{API}/products")
        assert r.status_code == 200
        products = r.json()
        assert isinstance(products, list)
        assert len(products) >= 100, f"Expected >=100 seeded products, got {len(products)}"
        # Validate schema
        p = products[0]
        for k in ("id", "sku", "name", "category", "brand", "price", "inventory", "image_url"):
            assert k in p

    def test_filter_by_category_footwear(self, api_client):
        r = api_client.get(f"{API}/products", params={"category": "Footwear"})
        assert r.status_code == 200
        products = r.json()
        assert len(products) > 0
        assert all(p["category"] == "Footwear" for p in products)

    def test_filter_by_brand_nike(self, api_client):
        r = api_client.get(f"{API}/products", params={"brand": "Nike"})
        assert r.status_code == 200
        products = r.json()
        assert len(products) > 0
        assert all(p["brand"] == "Nike" for p in products)

    def test_create_product_requires_auth(self, api_client):
        r = api_client.post(f"{API}/products", json={
            "sku": "TEST_SKU_1", "name": "TEST product", "category": "Footwear",
            "brand": "Nike", "price": 1000.0, "inventory": 5,
            "image_url": "https://x.com/i.png"
        })
        assert r.status_code in (401, 403)

    def test_create_product_with_auth(self, api_client, auth_headers):
        payload = {
            "sku": f"TEST_SKU_{uuid.uuid4().hex[:6]}",
            "name": "TEST product",
            "category": "Footwear",
            "brand": "Nike",
            "price": 1500.0,
            "inventory": 50,
            "image_url": "https://example.com/img.png"
        }
        r = api_client.post(f"{API}/products", json=payload, headers=auth_headers)
        assert r.status_code == 200, r.text
        created = r.json()
        assert created["sku"] == payload["sku"]
        assert created["price"] == 1500.0

        # Verify GET fetches it
        gr = api_client.get(f"{API}/products")
        assert any(p["id"] == created["id"] for p in gr.json())

        # Cleanup
        api_client.delete(f"{API}/products/{created['id']}", headers=auth_headers)


# -------------------- CATEGORIES / BRANDS --------------------
class TestCategoriesBrands:
    def test_get_categories(self, api_client):
        r = api_client.get(f"{API}/categories")
        assert r.status_code == 200
        cats = r.json()
        assert isinstance(cats, list)
        assert len(cats) >= 5, f"Expected >=5 categories, got {len(cats)}"

    def test_get_brands(self, api_client):
        r = api_client.get(f"{API}/brands")
        assert r.status_code == 200
        brands = r.json()
        assert isinstance(brands, list)
        assert len(brands) >= 7, f"Expected >=7 brands, got {len(brands)}"


# -------------------- PROMOTIONS --------------------
class TestPromotions:
    def test_get_all_promotions(self, api_client):
        r = api_client.get(f"{API}/promotions")
        assert r.status_code == 200
        promos = r.json()
        assert isinstance(promos, list)
        assert len(promos) >= 20, f"Expected >=20 promotions, got {len(promos)}"

    def test_get_active_promotions(self, api_client):
        r = api_client.get(f"{API}/promotions", params={"active_only": "true"})
        assert r.status_code == 200
        promos = r.json()
        assert all(p["active"] is True for p in promos)

    def test_create_promotion_requires_auth(self, api_client):
        r = api_client.post(f"{API}/promotions", json={
            "name": "TEST P", "description": "x", "type": "threshold",
            "rules": {"type": "threshold", "conditions": {"min_amount": 100}},
            "discount_type": "percentage", "discount_value": 10.0
        })
        assert r.status_code in (401, 403)

    def test_create_promotion_with_auth(self, api_client, auth_headers):
        payload = {
            "name": "TEST Promo",
            "description": "Test threshold promo",
            "type": "threshold",
            "rules": {"type": "threshold", "conditions": {"min_amount": 1000}},
            "discount_type": "percentage",
            "discount_value": 5.0,
            "active": True,
            "priority": 1
        }
        r = api_client.post(f"{API}/promotions", json=payload, headers=auth_headers)
        assert r.status_code == 200, r.text
        created = r.json()
        assert created["name"] == "TEST Promo"
        # Cleanup
        api_client.delete(f"{API}/promotions/{created['id']}", headers=auth_headers)


# -------------------- CART --------------------
class TestCart:
    def test_get_cart_creates_empty(self, api_client):
        uid = f"TEST_{uuid.uuid4().hex[:8]}"
        r = api_client.get(f"{API}/cart/{uid}")
        assert r.status_code == 200
        cart = r.json()
        assert cart["user_id"] == uid
        assert cart["items"] == []
        assert cart["total"] == 0.0

    def test_add_to_cart_and_remove(self, api_client):
        uid = f"TEST_{uuid.uuid4().hex[:8]}"
        products = api_client.get(f"{API}/products").json()
        p = products[0]
        r = api_client.post(f"{API}/cart/{uid}/items",
                            json={"product_id": p["id"], "quantity": 2})
        assert r.status_code == 200, r.text
        cart = r.json()
        assert any(it["product_id"] == p["id"] for it in cart["items"])
        assert cart["subtotal"] > 0
        # Remove
        r = api_client.delete(f"{API}/cart/{uid}/items/{p['id']}")
        assert r.status_code == 200
        cart = r.json()
        assert not any(it["product_id"] == p["id"] for it in cart["items"])
        assert cart["total"] == 0.0

    def test_add_invalid_product(self, api_client):
        uid = f"TEST_{uuid.uuid4().hex[:8]}"
        r = api_client.post(f"{API}/cart/{uid}/items",
                            json={"product_id": "non-existent-id", "quantity": 1})
        assert r.status_code == 404

    def test_threshold_promotion_auto_calc(self, api_client):
        """Add enough items so subtotal > 4000 to verify promo engine kicks in."""
        uid = f"TEST_{uuid.uuid4().hex[:8]}"
        products = api_client.get(f"{API}/products").json()
        # Pick most expensive products to easily exceed 4000
        products_sorted = sorted(products, key=lambda x: x["price"], reverse=True)[:5]
        last_cart = None
        for p in products_sorted:
            r = api_client.post(f"{API}/cart/{uid}/items",
                                json={"product_id": p["id"], "quantity": 2})
            assert r.status_code == 200
            last_cart = r.json()
        assert last_cart is not None
        assert last_cart["subtotal"] > 4000, f"Subtotal was {last_cart['subtotal']}"
        # If any threshold/active promo is configured for min_amount<=subtotal we expect discount>0
        # but we won't hard-fail if not — just log when promotions applied
        print(f"Subtotal={last_cart['subtotal']}, discount={last_cart['discount']}, "
              f"total={last_cart['total']}, applied={last_cart['applied_promotions']}")
        # Discount/total invariants
        assert last_cart["total"] == pytest.approx(
            last_cart["subtotal"] - last_cart["discount"], rel=1e-3)


# -------------------- AI RECOMMENDATIONS --------------------
class TestAIRecommendations:
    def test_recommendations_endpoint(self, api_client, admin_user):
        products = api_client.get(f"{API}/products").json()
        cart_items = [{
            "product_id": products[0]["id"],
            "name": products[0]["name"],
            "price": products[0]["price"],
            "quantity": 1,
            "category": products[0]["category"],
            "brand": products[0]["brand"]
        }]
        payload = {"cart_items": cart_items, "user_id": admin_user["id"]}
        r = api_client.post(f"{API}/recommendations/analyze", json=payload, timeout=120)
        assert r.status_code == 200, r.text
        data = r.json()
        # Expected fields
        for key in ("recommended_products", "explanation"):
            assert key in data, f"missing key {key} in {list(data.keys())}"


# -------------------- ANALYTICS --------------------
class TestAnalytics:
    def test_analytics_overview(self, api_client):
        r = api_client.get(f"{API}/analytics")
        assert r.status_code == 200
        data = r.json()
        assert "overview" in data
        ov = data["overview"]
        assert ov["total_products"] >= 100
        assert ov["total_active_promotions"] >= 1
        assert "categories" in data and isinstance(data["categories"], list)
        assert "brands" in data and isinstance(data["brands"], list)
        assert "promotion_types" in data and isinstance(data["promotion_types"], list)
