# Architecture

## System Overview

PromoSmart AI is a 3-tier web application:

```
┌─────────────────────────────────────────────────────────────┐
│                      React Frontend                          │
│   (Pages: Login, Dashboard, Products, Promotions, Cart,      │
│    Recommendations, Analytics, Settings)                     │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTPS (JWT Bearer)
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                  FastAPI Backend (Port 8001)                 │
│   ┌──────────────────────────────────────────────────────┐  │
│   │  /api/auth      JWT auth (login/register)             │  │
│   │  /api/products  CRUD                                  │  │
│   │  /api/promotions CRUD + active filter                 │  │
│   │  /api/cart      Add/remove with auto-discount calc    │  │
│   │  /api/recommendations  ─── Gemini 3 Flash             │  │
│   │  /api/analytics dashboard stats                       │  │
│   └──────────────────────────────────────────────────────┘  │
│         │                          │                         │
│         ▼                          ▼                         │
│   Promotion Engine            AI Service                     │
│   (bundle/threshold/          (emergentintegrations          │
│    category/brand calc)        → Gemini 3 Flash)             │
└──────────────────────────┬──────────────────────────────────┘
                           │ Motor (async)
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                       MongoDB                                │
│   Collections: users, products, categories, brands,          │
│   promotions, carts                                          │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow: AI Recommendation

```
  User adds product to cart
          │
          ▼
  POST /api/cart/{user_id}/items
          │
          ▼
  PromotionEngine.calculate_cart_totals()
     - Loads all active promotions (sorted by priority)
     - Iterates each promo type (bundle/threshold/category/brand)
     - Returns: subtotal, discount, total, applied_promotions[]
          │
          ▼
  User clicks "Get AI Recommendations"
          │
          ▼
  POST /api/recommendations/analyze
     {cart_items: [...], user_id}
          │
          ▼
  AIRecommendationService.generate_recommendation()
     - Builds prompt with cart + all products + active promos
     - Sends to Gemini 3 Flash via emergentintegrations.LlmChat
     - Parses JSON response
          │
          ▼
  Returns:
     {
       recommended_products: [{id, name, price, reason}],
       explanation: "...",
       additional_spend,
       discount_earned,
       promotions_activated
     }
```

## Promotion Engine Logic

Four promotion types with priority-based application (highest first):

| Type | Condition | Example |
|------|-----------|---------|
| **bundle** | All required products in cart | Shoes + Socks → 10% off |
| **threshold** | Cart subtotal ≥ min_spend | Spend ₹4000 → ₹500 off |
| **category** | ≥ N items from category | 3 Apparel items → 20% off |
| **brand** | ≥ N items from brand | 2 Nike products → 10% off |

Discounts can be `percentage` or `fixed` (absolute amount).

## Authentication Flow

1. User submits credentials → `POST /api/auth/login`
2. Backend verifies bcrypt hash → issues JWT with `{sub, id, role}`
3. Frontend stores token in `localStorage`
4. All subsequent requests include `Authorization: Bearer <token>`
5. Protected endpoints verify token via `get_current_user` dependency

## Frontend State Management

- **AuthContext** — User session, login/register/logout
- **CartContext** — Cart items, add/remove, syncs with backend on every mutation
- **React Router** — Route guards via `PrivateRoute`/`PublicRoute`

## Deployment Notes

- All env vars loaded from `.env` (never hardcoded)
- Backend binds to `0.0.0.0:8001`
- MongoDB connection via `MONGO_URL`
- CORS configurable via `CORS_ORIGINS`
- Gemini key via `EMERGENT_LLM_KEY` (Emergent's universal LLM key)
