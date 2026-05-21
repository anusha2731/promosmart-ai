import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os
from pathlib import Path
from datetime import datetime, timezone
import uuid
from passlib.context import CryptContext

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]


async def seed_database():
    print("Starting database seeding...")
    
    await db.users.delete_many({})
    await db.products.delete_many({})
    await db.categories.delete_many({})
    await db.brands.delete_many({})
    await db.promotions.delete_many({})
    await db.carts.delete_many({})
    
    print("Creating admin user...")
    admin_user = {
        "id": str(uuid.uuid4()),
        "email": "admin@promosmart.com",
        "password": pwd_context.hash("Admin@123"),
        "name": "Admin User",
        "role": "admin",
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    await db.users.insert_one(admin_user)
    
    print("Creating categories...")
    categories = [
        {"id": str(uuid.uuid4()), "name": "Footwear", "created_at": datetime.now(timezone.utc).isoformat()},
        {"id": str(uuid.uuid4()), "name": "Apparel", "created_at": datetime.now(timezone.utc).isoformat()},
        {"id": str(uuid.uuid4()), "name": "Accessories", "created_at": datetime.now(timezone.utc).isoformat()},
        {"id": str(uuid.uuid4()), "name": "Electronics", "created_at": datetime.now(timezone.utc).isoformat()},
        {"id": str(uuid.uuid4()), "name": "Sports", "created_at": datetime.now(timezone.utc).isoformat()},
    ]
    await db.categories.insert_many(categories)
    
    print("Creating brands...")
    brands = [
        {"id": str(uuid.uuid4()), "name": "Nike", "created_at": datetime.now(timezone.utc).isoformat()},
        {"id": str(uuid.uuid4()), "name": "Adidas", "created_at": datetime.now(timezone.utc).isoformat()},
        {"id": str(uuid.uuid4()), "name": "Puma", "created_at": datetime.now(timezone.utc).isoformat()},
        {"id": str(uuid.uuid4()), "name": "Apple", "created_at": datetime.now(timezone.utc).isoformat()},
        {"id": str(uuid.uuid4()), "name": "Samsung", "created_at": datetime.now(timezone.utc).isoformat()},
        {"id": str(uuid.uuid4()), "name": "Levi's", "created_at": datetime.now(timezone.utc).isoformat()},
        {"id": str(uuid.uuid4()), "name": "Ray-Ban", "created_at": datetime.now(timezone.utc).isoformat()},
    ]
    await db.brands.insert_many(brands)
    
    print("Creating 100 products...")
    products = []
    
    footwear_products = [
        {"name": "Running Shoes Pro", "brand": "Nike", "price": 3000, "image": "https://images.unsplash.com/photo-1768647417374-5a31c61dc5d0?w=300"},
        {"name": "Classic Sneakers", "brand": "Adidas", "price": 2500, "image": "https://images.pexels.com/photos/20755674/pexels-photo-20755674.jpeg?w=300"},
        {"name": "Sports Shoes Elite", "brand": "Puma", "price": 2800, "image": "https://images.unsplash.com/photo-1768647417374-5a31c61dc5d0?w=300"},
        {"name": "Walking Shoes Comfort", "brand": "Nike", "price": 2200, "image": "https://images.pexels.com/photos/20755674/pexels-photo-20755674.jpeg?w=300"},
        {"name": "Trail Running Shoes", "brand": "Adidas", "price": 3500, "image": "https://images.unsplash.com/photo-1768647417374-5a31c61dc5d0?w=300"},
    ]
    
    apparel_products = [
        {"name": "Cotton T-Shirt", "brand": "Levi's", "price": 800, "image": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=300"},
        {"name": "Denim Jeans", "brand": "Levi's", "price": 2000, "image": "https://images.unsplash.com/photo-1542272604-787c3835535d?w=300"},
        {"name": "Sports Jersey", "brand": "Nike", "price": 1500, "image": "https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=300"},
        {"name": "Hoodie Premium", "brand": "Adidas", "price": 2500, "image": "https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=300"},
        {"name": "Track Pants", "brand": "Puma", "price": 1800, "image": "https://images.unsplash.com/photo-1542272604-787c3835535d?w=300"},
    ]
    
    accessories_products = [
        {"name": "Sports Socks (3 Pack)", "brand": "Nike", "price": 300, "image": "https://images.unsplash.com/photo-1586350977771-b3b0abd50c82?w=300"},
        {"name": "Leather Belt", "brand": "Levi's", "price": 700, "image": "https://images.unsplash.com/photo-1624222247344-550fb60583bb?w=300"},
        {"name": "Sunglasses Classic", "brand": "Ray-Ban", "price": 5000, "image": "https://images.unsplash.com/photo-1511499767150-a48a237f0083?w=300"},
        {"name": "Sports Cap", "brand": "Nike", "price": 500, "image": "https://images.unsplash.com/photo-1588850561407-ed78c282e89b?w=300"},
        {"name": "Backpack Pro", "brand": "Adidas", "price": 3000, "image": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=300"},
    ]
    
    electronics_products = [
        {"name": "Smartwatch Series 5", "brand": "Apple", "price": 25000, "image": "https://images.unsplash.com/photo-1758348844348-acaf8d854665?w=300"},
        {"name": "Wireless Earbuds", "brand": "Samsung", "price": 8000, "image": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=300"},
        {"name": "Fitness Tracker", "brand": "Samsung", "price": 5000, "image": "https://images.pexels.com/photos/9142237/pexels-photo-9142237.jpeg?w=300"},
        {"name": "Bluetooth Speaker", "brand": "Samsung", "price": 3500, "image": "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=300"},
        {"name": "Power Bank 20000mAh", "brand": "Samsung", "price": 2000, "image": "https://images.unsplash.com/photo-1609091839311-d5365f9ff1c5?w=300"},
    ]
    
    sports_products = [
        {"name": "Yoga Mat Premium", "brand": "Nike", "price": 1500, "image": "https://images.unsplash.com/photo-1592432678016-e910b452f9a2?w=300"},
        {"name": "Dumbbell Set 5kg", "brand": "Puma", "price": 2000, "image": "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=300"},
        {"name": "Tennis Racket", "brand": "Nike", "price": 4000, "image": "https://images.unsplash.com/photo-1554068865-24cecd4e34b8?w=300"},
        {"name": "Football Size 5", "brand": "Adidas", "price": 1200, "image": "https://images.unsplash.com/photo-1614632537423-1e6f2fbb7c7b?w=300"},
        {"name": "Basketball Official", "brand": "Nike", "price": 1500, "image": "https://images.unsplash.com/photo-1546519638-68e109498ffc?w=300"},
    ]
    
    all_product_templates = [
        ("Footwear", footwear_products),
        ("Apparel", apparel_products),
        ("Accessories", accessories_products),
        ("Electronics", electronics_products),
        ("Sports", sports_products),
    ]
    
    for category, templates in all_product_templates:
        for i, template in enumerate(templates):
            for j in range(4):
                product_id = str(uuid.uuid4())
                products.append({
                    "id": product_id,
                    "sku": f"{category[:3].upper()}-{template['brand'][:3].upper()}-{i:03d}{j:02d}",
                    "name": f"{template['name']} {['', 'V2', 'Pro', 'Max'][j]}".strip(),
                    "category": category,
                    "brand": template['brand'],
                    "price": template['price'] + (j * 200),
                    "inventory": 50 + (j * 10),
                    "image_url": template['image'],
                    "created_at": datetime.now(timezone.utc).isoformat()
                })
    
    await db.products.insert_many(products)
    print(f"Created {len(products)} products")
    
    print("Creating 20 promotions...")
    product_ids = [p['id'] for p in products]
    
    promotions = [
        {
            "id": str(uuid.uuid4()),
            "name": "Shoes + Socks Bundle",
            "description": "Buy any shoes with socks and get 10% off",
            "type": "bundle",
            "rules": {
                "type": "bundle",
                "conditions": {
                    "products": [
                        next(p['id'] for p in products if 'Running Shoes Pro' in p['name']),
                        next(p['id'] for p in products if 'Sports Socks' in p['name'])
                    ]
                }
            },
            "discount_type": "percentage",
            "discount_value": 10,
            "active": True,
            "priority": 5,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Spend ₹4000 Get ₹500 Off",
            "description": "Spend ₹4000 or more and get ₹500 discount",
            "type": "threshold",
            "rules": {
                "type": "threshold",
                "conditions": {
                    "min_spend": 4000
                }
            },
            "discount_type": "fixed",
            "discount_value": 500,
            "active": True,
            "priority": 3,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Spend ₹6000 Get ₹1000 Off",
            "description": "Spend ₹6000 or more and get ₹1000 discount",
            "type": "threshold",
            "rules": {
                "type": "threshold",
                "conditions": {
                    "min_spend": 6000
                }
            },
            "discount_type": "fixed",
            "discount_value": 1000,
            "active": True,
            "priority": 4,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Buy 2 Accessories Get 15% Off",
            "description": "Purchase 2 or more accessories and save 15%",
            "type": "category",
            "rules": {
                "type": "category",
                "conditions": {
                    "category": "Accessories",
                    "min_quantity": 2
                }
            },
            "discount_type": "percentage",
            "discount_value": 15,
            "active": True,
            "priority": 4,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Buy 3 Apparel Items Get 20% Off",
            "description": "Buy 3 or more apparel items and get 20% discount",
            "type": "category",
            "rules": {
                "type": "category",
                "conditions": {
                    "category": "Apparel",
                    "min_quantity": 3
                }
            },
            "discount_type": "percentage",
            "discount_value": 20,
            "active": True,
            "priority": 5,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Nike Products - Buy 2 Get 10% Off",
            "description": "Purchase 2 Nike products and save 10%",
            "type": "brand",
            "rules": {
                "type": "brand",
                "conditions": {
                    "brand": "Nike",
                    "min_quantity": 2
                }
            },
            "discount_type": "percentage",
            "discount_value": 10,
            "active": True,
            "priority": 3,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Adidas Flash Sale",
            "description": "Buy 2 Adidas items get 12% off",
            "type": "brand",
            "rules": {
                "type": "brand",
                "conditions": {
                    "brand": "Adidas",
                    "min_quantity": 2
                }
            },
            "discount_type": "percentage",
            "discount_value": 12,
            "active": True,
            "priority": 3,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Electronics Mega Deal",
            "description": "Buy 2 electronics items and get ₹1500 off",
            "type": "category",
            "rules": {
                "type": "category",
                "conditions": {
                    "category": "Electronics",
                    "min_quantity": 2
                }
            },
            "discount_type": "fixed",
            "discount_value": 1500,
            "active": True,
            "priority": 6,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Sports Bundle Special",
            "description": "Buy 3 sports items get 18% discount",
            "type": "category",
            "rules": {
                "type": "category",
                "conditions": {
                    "category": "Sports",
                    "min_quantity": 3
                }
            },
            "discount_type": "percentage",
            "discount_value": 18,
            "active": True,
            "priority": 4,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Footwear Fest",
            "description": "Buy 2 footwear items and save ₹800",
            "type": "category",
            "rules": {
                "type": "category",
                "conditions": {
                    "category": "Footwear",
                    "min_quantity": 2
                }
            },
            "discount_type": "fixed",
            "discount_value": 800,
            "active": True,
            "priority": 4,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Samsung Tech Bundle",
            "description": "Buy 2 Samsung products get 15% off",
            "type": "brand",
            "rules": {
                "type": "brand",
                "conditions": {
                    "brand": "Samsung",
                    "min_quantity": 2
                }
            },
            "discount_type": "percentage",
            "discount_value": 15,
            "active": True,
            "priority": 5,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Levi's Denim Days",
            "description": "Buy 2 Levi's items get ₹600 off",
            "type": "brand",
            "rules": {
                "type": "brand",
                "conditions": {
                    "brand": "Levi's",
                    "min_quantity": 2
                }
            },
            "discount_type": "fixed",
            "discount_value": 600,
            "active": True,
            "priority": 3,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Puma Power Pack",
            "description": "Buy 3 Puma products and save 20%",
            "type": "brand",
            "rules": {
                "type": "brand",
                "conditions": {
                    "brand": "Puma",
                    "min_quantity": 3
                }
            },
            "discount_type": "percentage",
            "discount_value": 20,
            "active": True,
            "priority": 5,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Spend ₹8000 Get ₹1500 Off",
            "description": "Mega deal - spend ₹8000 or more and get ₹1500 off",
            "type": "threshold",
            "rules": {
                "type": "threshold",
                "conditions": {
                    "min_spend": 8000
                }
            },
            "discount_type": "fixed",
            "discount_value": 1500,
            "active": True,
            "priority": 7,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Spend ₹10000 Get ₹2000 Off",
            "description": "Premium deal - spend ₹10000 or more and get ₹2000 off",
            "type": "threshold",
            "rules": {
                "type": "threshold",
                "conditions": {
                    "min_spend": 10000
                }
            },
            "discount_type": "fixed",
            "discount_value": 2000,
            "active": True,
            "priority": 8,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Weekend Apparel Sale",
            "description": "Buy any 2 apparel items and get 12% off",
            "type": "category",
            "rules": {
                "type": "category",
                "conditions": {
                    "category": "Apparel",
                    "min_quantity": 2
                }
            },
            "discount_type": "percentage",
            "discount_value": 12,
            "active": True,
            "priority": 2,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Accessories Combo",
            "description": "Buy 3 accessories and save ₹400",
            "type": "category",
            "rules": {
                "type": "category",
                "conditions": {
                    "category": "Accessories",
                    "min_quantity": 3
                }
            },
            "discount_type": "fixed",
            "discount_value": 400,
            "active": True,
            "priority": 3,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Ray-Ban Premium",
            "description": "Special deal on Ray-Ban products - ₹1000 off on 1 item",
            "type": "brand",
            "rules": {
                "type": "brand",
                "conditions": {
                    "brand": "Ray-Ban",
                    "min_quantity": 1
                }
            },
            "discount_type": "fixed",
            "discount_value": 1000,
            "active": True,
            "priority": 6,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Apple Watch Bundle",
            "description": "Buy Apple products worth ₹25000+ and get ₹3000 off",
            "type": "brand",
            "rules": {
                "type": "brand",
                "conditions": {
                    "brand": "Apple",
                    "min_quantity": 1
                }
            },
            "discount_type": "fixed",
            "discount_value": 3000,
            "active": True,
            "priority": 7,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Complete Outfit Deal",
            "description": "Buy 4+ apparel items and get 25% off",
            "type": "category",
            "rules": {
                "type": "category",
                "conditions": {
                    "category": "Apparel",
                    "min_quantity": 4
                }
            },
            "discount_type": "percentage",
            "discount_value": 25,
            "active": True,
            "priority": 6,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
    ]
    
    await db.promotions.insert_many(promotions)
    print(f"Created {len(promotions)} promotions")
    
    print("Database seeding completed successfully!")
    print(f"Admin credentials: admin@promosmart.com / Admin@123")


if __name__ == "__main__":
    asyncio.run(seed_database())
