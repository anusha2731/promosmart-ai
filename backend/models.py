from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
import uuid


class Product(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    sku: str
    name: str
    category: str
    brand: str
    price: float
    inventory: int
    image_url: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ProductCreate(BaseModel):
    sku: str
    name: str
    category: str
    brand: str
    price: float
    inventory: int
    image_url: str


class Category(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class CategoryCreate(BaseModel):
    name: str


class Brand(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class BrandCreate(BaseModel):
    name: str


class PromotionRule(BaseModel):
    type: str
    conditions: Dict[str, Any]


class Promotion(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    type: str
    rules: PromotionRule
    discount_type: str
    discount_value: float
    active: bool = True
    priority: int = 1
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class PromotionCreate(BaseModel):
    name: str
    description: str
    type: str
    rules: PromotionRule
    discount_type: str
    discount_value: float
    active: bool = True
    priority: int = 1


class CartItem(BaseModel):
    product_id: str
    quantity: int
    price: float


class Cart(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    items: List[CartItem] = []
    subtotal: float = 0.0
    discount: float = 0.0
    total: float = 0.0
    applied_promotions: List[str] = []
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class CartUpdate(BaseModel):
    product_id: str
    quantity: int


class RecommendationRequest(BaseModel):
    cart_items: List[Dict[str, Any]]
    user_id: str


class Recommendation(BaseModel):
    recommended_products: List[Dict[str, Any]]
    explanation: str
    additional_spend: float
    discount_earned: float
    final_savings: float
    savings_percentage: float
    promotions_activated: List[str]


class User(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: str
    password: str
    name: str
    role: str = "user"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class UserCreate(BaseModel):
    email: str
    password: str
    name: str
    role: str = "user"


class UserLogin(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
    user: Dict[str, Any]