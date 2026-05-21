# API Documentation

Base URL: `http://localhost:8001/api`

All protected endpoints (marked 🔒) require `Authorization: Bearer <token>` header.

## Authentication

### POST `/api/auth/register`
Register a new user.

**Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "securepass",
  "role": "user"
}
```

**Response 200:**
```json
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer",
  "user": {"id": "...", "email": "...", "name": "...", "role": "user"}
}
```

### POST `/api/auth/login`
Login with credentials.

**Body:**
```json
{
  "email": "admin@promosmart.com",
  "password": "Admin@123"
}
```

**Response 200:** Same as register.

---

## Products

### GET `/api/products`
List all products with optional filters.

**Query params:** `category`, `brand`

### POST `/api/products` 🔒
Create a product.

```json
{
  "sku": "NIKE-001",
  "name": "Running Shoes",
  "category": "Footwear",
  "brand": "Nike",
  "price": 3000,
  "inventory": 50,
  "image_url": "https://..."
}
```

### PUT `/api/products/{product_id}` 🔒
Update a product.

### DELETE `/api/products/{product_id}` 🔒
Delete a product.

---

## Categories & Brands

### GET `/api/categories`
List all categories.

### POST `/api/categories` 🔒
Body: `{"name": "..."}`

### GET `/api/brands`
List all brands.

### POST `/api/brands` 🔒
Body: `{"name": "..."}`

---

## Promotions

### GET `/api/promotions`
List all promotions. Query param: `active_only=true`.

### POST `/api/promotions` 🔒
Create a promotion.

**Threshold example:**
```json
{
  "name": "Spend ₹4000 Get ₹500 Off",
  "description": "Threshold deal",
  "type": "threshold",
  "rules": {
    "type": "threshold",
    "conditions": {"min_spend": 4000}
  },
  "discount_type": "fixed",
  "discount_value": 500,
  "active": true,
  "priority": 3
}
```

**Bundle example:**
```json
{
  "rules": {
    "type": "bundle",
    "conditions": {"products": ["product_id_1", "product_id_2"]}
  },
  "discount_type": "percentage",
  "discount_value": 10
}
```

**Category example:**
```json
{
  "rules": {
    "type": "category",
    "conditions": {"category": "Apparel", "min_quantity": 3}
  }
}
```

**Brand example:**
```json
{
  "rules": {
    "type": "brand",
    "conditions": {"brand": "Nike", "min_quantity": 2}
  }
}
```

### PUT `/api/promotions/{promo_id}` 🔒
### DELETE `/api/promotions/{promo_id}` 🔒

---

## Cart

### GET `/api/cart/{user_id}`
Fetch user's cart (creates empty cart if not exists).

```json
{
  "id": "...",
  "user_id": "...",
  "items": [{"product_id": "...", "quantity": 2, "price": 3000}],
  "subtotal": 6000,
  "discount": 1000,
  "total": 5000,
  "applied_promotions": ["Spend ₹6000 Get ₹1000 Off"]
}
```

### POST `/api/cart/{user_id}/items`
Add/update an item. Auto-recalculates promotions.

Body: `{"product_id": "...", "quantity": 2}`

### DELETE `/api/cart/{user_id}/items/{product_id}`
Remove an item from cart.

---

## AI Recommendations

### POST `/api/recommendations/analyze`
Get AI-powered product recommendations.

**Body:**
```json
{
  "cart_items": [
    {"product_id": "...", "name": "Running Shoes", "category": "Footwear", "brand": "Nike", "price": 3000, "quantity": 1}
  ],
  "user_id": "..."
}
```

**Response:**
```json
{
  "recommended_products": [
    {"product_id": "...", "name": "Sports Socks", "price": 300, "reason": "Activates Shoes+Socks bundle"}
  ],
  "explanation": "Adding socks activates the bundle promo...",
  "additional_spend": 1000,
  "discount_earned": 900,
  "promotions_activated": ["Shoes + Socks Bundle", "Spend ₹4000 Get ₹500 Off"]
}
```

---

## Analytics

### GET `/api/analytics`
Get dashboard analytics.

```json
{
  "overview": {
    "total_products": 100,
    "total_active_promotions": 20,
    "total_users": 5,
    "low_stock_items": 0
  },
  "categories": [{"name": "Footwear", "count": 20}],
  "brands": [{"name": "Nike", "count": 28}],
  "promotion_types": [{"type": "bundle", "count": 1}],
  "low_stock_products": []
}
```
