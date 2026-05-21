import os
from dotenv import load_dotenv
from emergentintegrations.llm.chat import LlmChat, UserMessage
from typing import List, Dict, Any
import json

load_dotenv()

EMERGENT_LLM_KEY = os.environ.get("EMERGENT_LLM_KEY")


class AIRecommendationService:
    def __init__(self):
        self.chat = LlmChat(
            api_key=EMERGENT_LLM_KEY,
            session_id="promosmart-recommendations",
            system_message="""You are an expert retail promotion analyst for PromoSmart AI. 
            Your role is to analyze shopping carts and active promotions to recommend products that maximize customer savings.
            Always provide clear, customer-friendly explanations of how the recommendations unlock discounts.
            Be specific about which promotions are activated and the exact savings amount."""
        ).with_model("gemini", "gemini-3-flash-preview")

    async def generate_recommendation(self, cart_items: List[Dict[str, Any]], 
                                     all_products: List[Dict[str, Any]], 
                                     active_promotions: List[Dict[str, Any]]) -> Dict[str, Any]:
        prompt = f"""
Analyze the following shopping cart and recommend products that will maximize discounts:

Current Cart:
{json.dumps(cart_items, indent=2)}

Available Products:
{json.dumps(all_products[:50], indent=2)}

Active Promotions:
{json.dumps(active_promotions, indent=2)}

Provide recommendations in the following JSON format:
{{
    "recommended_products": [
        {{
            "product_id": "...",
            "name": "...",
            "price": 0.00,
            "reason": "..."
        }}
    ],
    "explanation": "Clear explanation of the savings strategy",
    "additional_spend": 0.00,
    "discount_earned": 0.00,
    "promotions_activated": ["promotion names"]
}}

Focus on:
1. Bundle promotions (e.g., buy product A + B for discount)
2. Threshold promotions (e.g., spend ₹X to unlock ₹Y off)
3. Category promotions (e.g., buy N items from category)
4. Brand promotions (e.g., buy N items from brand)

Recommend 2-3 products maximum that provide the highest savings.
"""

        user_message = UserMessage(text=prompt)
        response = await self.chat.send_message(user_message)
        
        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                json_str = response[json_start:json_end]
                return json.loads(json_str)
            else:
                return {
                    "recommended_products": [],
                    "explanation": response,
                    "additional_spend": 0.0,
                    "discount_earned": 0.0,
                    "promotions_activated": []
                }
        except Exception as e:
            return {
                "recommended_products": [],
                "explanation": f"Unable to parse recommendation: {str(e)}",
                "additional_spend": 0.0,
                "discount_earned": 0.0,
                "promotions_activated": []
            }

    async def explain_promotion(self, promotion: Dict[str, Any], cart: Dict[str, Any]) -> str:
        prompt = f"""
Explain how this promotion applies to the customer's cart in simple, friendly language:

Promotion:
{json.dumps(promotion, indent=2)}

Current Cart:
{json.dumps(cart, indent=2)}

Provide a 2-3 sentence explanation that a customer would easily understand.
"""
        
        user_message = UserMessage(text=prompt)
        response = await self.chat.send_message(user_message)
        return response

    async def suggest_alternatives(self, product_name: str, category: str, 
                                  available_products: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        prompt = f"""
The product "{product_name}" from category "{category}" is out of stock.
Suggest 2-3 alternative products from this list:

{json.dumps(available_products[:30], indent=2)}

Return JSON array of alternatives:
[
    {{
        "product_id": "...",
        "name": "...",
        "price": 0.00,
        "reason": "why this is a good alternative"
    }}
]
"""
        
        user_message = UserMessage(text=prompt)
        response = await self.chat.send_message(user_message)
        
        try:
            json_start = response.find('[')
            json_end = response.rfind(']') + 1
            if json_start != -1 and json_end > json_start:
                json_str = response[json_start:json_end]
                return json.loads(json_str)
            else:
                return []
        except:
            return []


ai_service = AIRecommendationService()