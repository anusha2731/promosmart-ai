from typing import List, Dict, Any, Tuple
from models import Cart, CartItem, Promotion


class PromotionEngine:
    @staticmethod
    def calculate_cart_totals(cart: Cart, products: List[Dict], 
                             promotions: List[Dict]) -> Tuple[float, float, float, List[str]]:
        subtotal = sum(item.price * item.quantity for item in cart.items)
        
        applicable_promos = [p for p in promotions if p.get('active', True)]
        applicable_promos.sort(key=lambda x: x.get('priority', 1), reverse=True)
        
        total_discount = 0.0
        applied_promotions = []
        
        for promo in applicable_promos:
            discount = PromotionEngine._apply_promotion(cart, products, promo)
            if discount > 0:
                total_discount += discount
                applied_promotions.append(promo['name'])
        
        final_total = max(0, subtotal - total_discount)
        
        return subtotal, total_discount, final_total, applied_promotions
    
    @staticmethod
    def _apply_promotion(cart: Cart, products: List[Dict], promo: Dict) -> float:
        promo_type = promo.get('type', '')
        rules = promo.get('rules', {})
        conditions = rules.get('conditions', {})
        discount_type = promo.get('discount_type', 'percentage')
        discount_value = promo.get('discount_value', 0)
        
        if promo_type == 'bundle':
            return PromotionEngine._apply_bundle_promo(cart, products, conditions, 
                                                       discount_type, discount_value)
        elif promo_type == 'threshold':
            return PromotionEngine._apply_threshold_promo(cart, conditions, 
                                                          discount_type, discount_value)
        elif promo_type == 'category':
            return PromotionEngine._apply_category_promo(cart, products, conditions, 
                                                         discount_type, discount_value)
        elif promo_type == 'brand':
            return PromotionEngine._apply_brand_promo(cart, products, conditions, 
                                                      discount_type, discount_value)
        
        return 0.0
    
    @staticmethod
    def _apply_bundle_promo(cart: Cart, products: List[Dict], conditions: Dict,
                           discount_type: str, discount_value: float) -> float:
        required_products = conditions.get('products', [])
        
        cart_product_ids = [item.product_id for item in cart.items if item.quantity > 0]
        
        has_all_products = all(pid in cart_product_ids for pid in required_products)
        
        if not has_all_products:
            return 0.0
        
        bundle_items = [item for item in cart.items if item.product_id in required_products]
        bundle_total = sum(item.price * item.quantity for item in bundle_items)
        
        if discount_type == 'percentage':
            return bundle_total * (discount_value / 100)
        else:
            return discount_value
    
    @staticmethod
    def _apply_threshold_promo(cart: Cart, conditions: Dict,
                              discount_type: str, discount_value: float) -> float:
        min_spend = conditions.get('min_spend', 0)
        subtotal = sum(item.price * item.quantity for item in cart.items)
        
        if subtotal >= min_spend:
            if discount_type == 'percentage':
                return subtotal * (discount_value / 100)
            else:
                return discount_value
        
        return 0.0
    
    @staticmethod
    def _apply_category_promo(cart: Cart, products: List[Dict], conditions: Dict,
                             discount_type: str, discount_value: float) -> float:
        target_category = conditions.get('category', '')
        min_quantity = conditions.get('min_quantity', 1)
        
        product_map = {p['id']: p for p in products}
        
        category_items = [
            item for item in cart.items 
            if product_map.get(item.product_id, {}).get('category') == target_category
        ]
        
        total_quantity = sum(item.quantity for item in category_items)
        
        if total_quantity >= min_quantity:
            category_total = sum(item.price * item.quantity for item in category_items)
            
            if discount_type == 'percentage':
                return category_total * (discount_value / 100)
            else:
                return discount_value
        
        return 0.0
    
    @staticmethod
    def _apply_brand_promo(cart: Cart, products: List[Dict], conditions: Dict,
                          discount_type: str, discount_value: float) -> float:
        target_brand = conditions.get('brand', '')
        min_quantity = conditions.get('min_quantity', 1)
        
        product_map = {p['id']: p for p in products}
        
        brand_items = [
            item for item in cart.items 
            if product_map.get(item.product_id, {}).get('brand') == target_brand
        ]
        
        total_quantity = sum(item.quantity for item in brand_items)
        
        if total_quantity >= min_quantity:
            brand_total = sum(item.price * item.quantity for item in brand_items)
            
            if discount_type == 'percentage':
                return brand_total * (discount_value / 100)
            else:
                return discount_value
        
        return 0.0