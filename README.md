# PromoSmart AI

> AI-Powered Retail Promotion Optimization & Product Recommendation Platform

PromoSmart AI helps retail sales associates instantly identify the best combinations of products that unlock maximum discounts for customers. Powered by **Google Gemini 3 Flash**, it analyzes active promotions, basket contents, and inventory to recommend smart additions that maximize savings — with clear, customer-friendly explanations.

---

## Features

### Core Features
- **Product Catalog** — Full CRUD for products with SKU, category, brand, price, inventory, and images
- **Flexible Promotion Engine** — Supports 4 promotion types:
  - **Bundle**: Buy Product A + B → discount
  - **Threshold**: Spend ₹X → get ₹Y off
  - **Category**: Buy N items from a category → discount
  - **Brand**: Buy N items from a brand → discount
- **Shopping Cart Simulator** — Add/remove products, auto-applies all relevant promotions
- **AI Recommendation Engine** — Gemini 3 Flash analyzes cart and suggests products to unlock maximum savings
- **Explainable AI** — Every recommendation comes with clear reasoning
- **Alternative Recommendations** — Suggests replacements for out-of-stock items
- **Analytics Dashboard** — Charts for category/brand distribution, promotion types, low stock alerts
- **Admin Panel** — Manage products, promotions, categories, brands

### Technical Highlights
- JWT-based authentication
- Async MongoDB with Motor driver
- Modular promotion engine (priority-based ranking)
- Fully responsive UI

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | React 19, React Router, Recharts, TailwindCSS, Shadcn UI, Sonner |
| Backend | Python 3.11, FastAPI, Motor (async MongoDB), Pydantic v2 |
| Database | MongoDB |
| AI | Google Gemini 3 Flash (via Emergent Integrations) |
| Auth | JWT (passlib + python-jose) |
| Charts | Recharts |
| Deployment | Docker Compose |

---

## Project Structure

```
promosmart-ai/
├── backend/
│   ├── server.py              # FastAPI app entry + all routes
│   ├── models.py              # Pydantic models
│   ├── auth.py                # JWT auth utilities
│   ├── promotion_engine.py    # Promotion calculation logic
│   ├── ai_service.py          # Gemini AI integration
│   ├── seed_data.py           # Seeds 100 products + 20 promotions
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── App.js             # Main router
│   │   ├── api.js             # Axios instance
│   │   ├── AuthContext.js     # Auth state
│   │   ├── CartContext.js     # Cart state
│   │   ├── pages/             # All app pages
│   │   └── components/        # Sidebar, Header
│   ├── package.json
│   ├── Dockerfile
│   └── .env.example
├── docker-compose.yml
├── ARCHITECTURE.md
├── API.md
└── README.md
```

---

## Quick Start (Docker Compose)

```bash
# 1. Clone the repo
git clone https://github.com/anusha2731/promosmart-ai.git
cd promosmart-ai

# 2. Set up environment
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
# Edit backend/.env and add your EMERGENT_LLM_KEY or Gemini API key

# 3. Run with Docker Compose
docker-compose up --build

# 4. Seed the database (in another terminal)
docker-compose exec backend python seed_data.py
```

App will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8001/api
- API Docs (Swagger): http://localhost:8001/docs

---

## Local Development (without Docker)

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install emergentintegrations --extra-index-url https://d33sy5i8bnduwe.cloudfront.net/simple/
python seed_data.py
uvicorn server:app --host 0.0.0.0 --port 8001 --reload
```

### Frontend
```bash
cd frontend
yarn install
yarn start
```

---

## Default Credentials

| Email | Password | Role |
|-------|----------|------|
| admin@promosmart.com | Admin@123 | admin |

---

## API Documentation

Full API reference is in [API.md](./API.md). Live Swagger UI available at `/docs` when the backend is running.

Key endpoints:
- `POST /api/auth/login` — Authenticate
- `GET /api/products` — List products
- `GET /api/promotions` — List promotions
- `POST /api/cart/{user_id}/items` — Add to cart (auto-applies promotions)
- `POST /api/recommendations/analyze` — Get AI recommendations
- `GET /api/analytics` — Dashboard analytics

---

## Architecture

See [ARCHITECTURE.md](./ARCHITECTURE.md) for the full system design and component relationships.

---

## Testing

Backend tests:
```bash
cd backend
pytest tests/
```

22/22 tests passing (100% backend coverage).

---

## License

MIT — feel free to use, modify, and distribute.

---

## Acknowledgements

- Built with [Emergent](https://emergent.sh)
- Powered by [Google Gemini 3 Flash](https://deepmind.google/technologies/gemini/)
