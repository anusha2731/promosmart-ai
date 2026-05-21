from fastapi import FastAPI, APIRouter, HTTPException, Depends
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from typing import List, Optional
from datetime import datetime

from models import (
    Product, ProductCreate, Category, CategoryCreate, Brand, BrandCreate,
    Promotion, PromotionCreate, Cart, CartUpdate, User, UserCreate, UserLogin, Token,
    RecommendationRequest, Recommendation, CartItem
)
from auth import get_password_hash, verify_password, create_access_token, get_current_user
from promotion_engine import PromotionEngine
from ai_service import ai_service


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

app = FastAPI()
api_router = APIRouter(prefix="/api")


@api_router.post("/auth/register", response_model=Token)
async def register(user_data: UserCreate):
    existing = await db.users.find_one({"email": user_data.email}, {"_id": 0})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user = User(**user_data.model_dump())
    user.password = get_password_hash(user.password)
    
    doc = user.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    await db.users.insert_one(doc)
    
    access_token = create_access_token(data={"sub": user.email, "id": user.id, "role": user.role})
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        user={"id": user.id, "email": user.email, "name": user.name, "role": user.role}
    )


@api_router.post("/auth/login", response_model=Token)
async def login(credentials: UserLogin):
    user_doc = await db.users.find_one({"email": credentials.email}, {"_id": 0})
    if not user_doc:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not verify_password(credentials.password, user_doc['password']):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(
        data={"sub": user_doc['email'], "id": user_doc['id'], "role": user_doc['role']}
    )
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        user={"id": user_doc['id'], "email": user_doc['email'], "name": user_doc['name'], "role": user_doc['role']}
    )


@api_router.get("/products", response_model=List[Product])
async def get_products(category: Optional[str] = None, brand: Optional[str] = None):
    query = {}
    if category:
        query['category'] = category
    if brand:
        query['brand'] = brand
    
    products = await db.products.find(query, {"_id": 0}).to_list(1000)
    
    for p in products:
        if isinstance(p.get('created_at'), str):
            p['created_at'] = datetime.fromisoformat(p['created_at'])
    
    return products


@api_router.post("/products", response_model=Product)
async def create_product(product_data: ProductCreate, current_user: dict = Depends(get_current_user)):
    product = Product(**product_data.model_dump())
    
    doc = product.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    await db.products.insert_one(doc)
    
    return product


@api_router.put("/products/{product_id}", response_model=Product)
async def update_product(product_id: str, product_data: ProductCreate, current_user: dict = Depends(get_current_user)):
    doc = product_data.model_dump()
    result = await db.products.update_one({"id": product_id}, {"$set": doc})
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    
    updated = await db.products.find_one({"id": product_id}, {"_id": 0})
    if isinstance(updated.get('created_at'), str):
        updated['created_at'] = datetime.fromisoformat(updated['created_at'])
    
    return Product(**updated)


@api_router.delete("/products/{product_id}")
async def delete_product(product_id: str, current_user: dict = Depends(get_current_user)):
    result = await db.products.delete_one({"id": product_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted"}


@api_router.get("/categories", response_model=List[Category])
async def get_categories():
    categories = await db.categories.find({}, {"_id": 0}).to_list(100)
    for c in categories:
        if isinstance(c.get('created_at'), str):
            c['created_at'] = datetime.fromisoformat(c['created_at'])
    return categories


@api_router.post("/categories", response_model=Category)
async def create_category(category_data: CategoryCreate, current_user: dict = Depends(get_current_user)):
    category = Category(**category_data.model_dump())
    doc = category.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    await db.categories.insert_one(doc)
    return category


@api_router.get("/brands", response_model=List[Brand])
async def get_brands():
    brands = await db.brands.find({}, {"_id": 0}).to_list(100)
    for b in brands:
        if isinstance(b.get('created_at'), str):
            b['created_at'] = datetime.fromisoformat(b['created_at'])
    return brands


@api_router.post("/brands", response_model=Brand)
async def create_brand(brand_data: BrandCreate, current_user: dict = Depends(get_current_user)):
    brand = Brand(**brand_data.model_dump())
    doc = brand.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    await db.brands.insert_one(doc)
    return brand


@api_router.get("/promotions", response_model=List[Promotion])
async def get_promotions(active_only: bool = False):
    query = {"active": True} if active_only else {}
    promotions = await db.promotions.find(query, {"_id": 0}).to_list(100)
    
    for p in promotions:
        if isinstance(p.get('created_at'), str):
            p['created_at'] = datetime.fromisoformat(p['created_at'])
    
    return promotions


@api_router.post("/promotions", response_model=Promotion)
async def create_promotion(promo_data: PromotionCreate, current_user: dict = Depends(get_current_user)):
    promo = Promotion(**promo_data.model_dump())
    doc = promo.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    doc['rules'] = doc['rules']
    await db.promotions.insert_one(doc)
    return promo


@api_router.put("/promotions/{promo_id}", response_model=Promotion)
async def update_promotion(promo_id: str, promo_data: PromotionCreate, current_user: dict = Depends(get_current_user)):
    doc = promo_data.model_dump()
    result = await db.promotions.update_one({"id": promo_id}, {"$set": doc})
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Promotion not found")
    
    updated = await db.promotions.find_one({"id": promo_id}, {"_id": 0})
    if isinstance(updated.get('created_at'), str):
        updated['created_at'] = datetime.fromisoformat(updated['created_at'])
    
    return Promotion(**updated)


@api_router.delete("/promotions/{promo_id}")
async def delete_promotion(promo_id: str, current_user: dict = Depends(get_current_user)):
    result = await db.promotions.delete_one({"id": promo_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Promotion not found")
    return {"message": "Promotion deleted"}


@api_router.get("/cart/{user_id}", response_model=Cart)
async def get_cart(user_id: str):
    cart_doc = await db.carts.find_one({"user_id": user_id}, {"_id": 0})
    
    if not cart_doc:
        cart = Cart(user_id=user_id)
        doc = cart.model_dump()
        doc['updated_at'] = doc['updated_at'].isoformat()
        await db.carts.insert_one(doc)
        return cart
    
    if isinstance(cart_doc.get('updated_at'), str):
        cart_doc['updated_at'] = datetime.fromisoformat(cart_doc['updated_at'])
    
    return Cart(**cart_doc)


@api_router.post("/cart/{user_id}/items")
async def add_to_cart(user_id: str, cart_update: CartUpdate):
    cart_doc = await db.carts.find_one({"user_id": user_id}, {"_id": 0})
    
    if not cart_doc:
        cart = Cart(user_id=user_id)
        cart_doc = cart.model_dump()
        cart_doc['updated_at'] = cart_doc['updated_at'].isoformat()
    
    product = await db.products.find_one({"id": cart_update.product_id}, {"_id": 0})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    items = cart_doc.get('items', [])
    existing_item = next((item for item in items if item['product_id'] == cart_update.product_id), None)
    
    if existing_item:
        existing_item['quantity'] = cart_update.quantity
    else:
        items.append({
            "product_id": cart_update.product_id,
            "quantity": cart_update.quantity,
            "price": product['price']
        })
    
    cart_doc['items'] = items
    
    cart_obj = Cart(**cart_doc)
    products = await db.products.find({}, {"_id": 0}).to_list(1000)
    promotions = await db.promotions.find({"active": True}, {"_id": 0}).to_list(100)
    
    subtotal, discount, total, applied_promos = PromotionEngine.calculate_cart_totals(
        cart_obj, products, promotions
    )
    
    cart_doc['subtotal'] = subtotal
    cart_doc['discount'] = discount
    cart_doc['total'] = total
    cart_doc['applied_promotions'] = applied_promos
    cart_doc['updated_at'] = datetime.now().isoformat()
    
    await db.carts.update_one(
        {"user_id": user_id},
        {"$set": cart_doc},
        upsert=True
    )
    
    return cart_doc


@api_router.delete("/cart/{user_id}/items/{product_id}")
async def remove_from_cart(user_id: str, product_id: str):
    cart_doc = await db.carts.find_one({"user_id": user_id}, {"_id": 0})
    
    if not cart_doc:
        raise HTTPException(status_code=404, detail="Cart not found")
    
    items = [item for item in cart_doc.get('items', []) if item['product_id'] != product_id]
    cart_doc['items'] = items
    
    if items:
        cart_obj = Cart(**cart_doc)
        products = await db.products.find({}, {"_id": 0}).to_list(1000)
        promotions = await db.promotions.find({"active": True}, {"_id": 0}).to_list(100)
        
        subtotal, discount, total, applied_promos = PromotionEngine.calculate_cart_totals(
            cart_obj, products, promotions
        )
        
        cart_doc['subtotal'] = subtotal
        cart_doc['discount'] = discount
        cart_doc['total'] = total
        cart_doc['applied_promotions'] = applied_promos
    else:
        cart_doc['subtotal'] = 0.0
        cart_doc['discount'] = 0.0
        cart_doc['total'] = 0.0
        cart_doc['applied_promotions'] = []
    
    cart_doc['updated_at'] = datetime.now().isoformat()
    
    await db.carts.update_one({"user_id": user_id}, {"$set": cart_doc})
    
    return cart_doc


@api_router.post("/recommendations/analyze")
async def analyze_recommendations(request: RecommendationRequest):
    products = await db.products.find({"inventory": {"$gt": 0}}, {"_id": 0}).to_list(1000)
    promotions = await db.promotions.find({"active": True}, {"_id": 0}).to_list(100)
    
    ai_recommendation = await ai_service.generate_recommendation(
        request.cart_items, products, promotions
    )
    
    return ai_recommendation


@api_router.get("/analytics")
async def get_analytics():
    total_products = await db.products.count_documents({})
    total_promotions = await db.promotions.count_documents({"active": True})
    total_users = await db.users.count_documents({})
    
    products = await db.products.find({}, {"_id": 0}).to_list(1000)
    promotions = await db.promotions.find({}, {"_id": 0}).to_list(100)
    
    low_stock_products = [p for p in products if p.get('inventory', 0) < 10]
    
    categories = {}
    brands = {}
    for p in products:
        cat = p.get('category', 'Unknown')
        brand = p.get('brand', 'Unknown')
        categories[cat] = categories.get(cat, 0) + 1
        brands[brand] = brands.get(brand, 0) + 1
    
    promo_types = {}
    for p in promotions:
        ptype = p.get('type', 'Unknown')
        promo_types[ptype] = promo_types.get(ptype, 0) + 1
    
    return {
        "overview": {
            "total_products": total_products,
            "total_active_promotions": total_promotions,
            "total_users": total_users,
            "low_stock_items": len(low_stock_products)
        },
        "categories": [{"name": k, "count": v} for k, v in categories.items()],
        "brands": [{"name": k, "count": v} for k, v in brands.items()],
        "promotion_types": [{"type": k, "count": v} for k, v in promo_types.items()],
        "low_stock_products": low_stock_products[:10]
    }


app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
