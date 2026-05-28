import os
import json
from typing import List, Dict, Any

from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

API_KEY = os.getenv("EMERGENT_LLM_KEY")

genai.configure(api_key=API_KEY)


model = genai.GenerativeModel("gemini-2.5-flash")


class AIRecommendationService:

    async def generate_recommendation(
        self,
        cart_items: List[Dict[str, Any]],
        all_products: List[Dict[str, Any]],
        active_promotions: List[Dict[str, Any]]
    ) -> Dict[str, Any]:

        prompt = f"""
Analyze the following shopping cart and recommend products that maximize discounts.

Current Cart:
{json.dumps(cart_items, indent=2)}

Available Products:
{json.dumps(all_products[:50], indent=2)}

Active Promotions:
{json.dumps(active_promotions, indent=2)}

Return ONLY valid JSON:
{{
    "recommended_products": [],
    "explanation": "",
    "additional_spend": 0,
    "discount_earned": 0,
    "promotions_activated": []
}}
"""

        response = model.generate_content(prompt)

        try:
            text = response.text
            start = text.find("{")
            end = text.rfind("}") + 1
            return json.loads(text[start:end])
        except Exception as e:
            return {
                "recommended_products": [],
                "explanation": str(e),
                "additional_spend": 0,
                "discount_earned": 0,
                "promotions_activated": []
            }

    async def explain_promotion(
        self,
        promotion: Dict[str, Any],
        cart: Dict[str, Any]
    ) -> str:

        prompt = f"""
Explain this promotion simply:

Promotion:
{json.dumps(promotion, indent=2)}

Cart:
{json.dumps(cart, indent=2)}
"""

        return model.generate_content(prompt).text

    async def suggest_alternatives(
        self,
        product_name: str,
        category: str,
        available_products: List[Dict[str, Any]]
    ):

        prompt = f"""
Suggest alternatives for:

Product: {product_name}
Category: {category}

Products:
{json.dumps(available_products[:30], indent=2)}

Return JSON array only.
"""

        try:
            text = model.generate_content(prompt).text
            start = text.find("[")
            end = text.rfind("]") + 1
            return json.loads(text[start:end])
        except Exception:
            return []


ai_service = AIRecommendationService()