import os
import json
from typing import Dict, List
from anthropic import Anthropic

class CopyGenerator:
    """Generate Facebook ad copy using Claude API"""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
        self.client = Anthropic(api_key=self.api_key)

    def generate_ad_copy(
        self,
        product_name: str,
        price: str,
        features: str,
        market: str,
        objective: str,
        description: str = ""
    ) -> Dict:
        """
        Generate 3 Facebook ad copy variants

        Args:
            product_name: Name of the product
            price: Product price
            features: Key features/benefits
            market: Target market (SI, DE, IT, AT, etc.)
            objective: Ad objective (Awareness, Conversion, Engagement)
            description: Additional product description

        Returns:
            Dictionary with 3 ad copy variants
        """
        try:
            prompt = self._build_prompt(
                product_name, price, features, market, objective, description
            )

            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2000,
                temperature=0.7,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            # Extract JSON from response
            response_text = message.content[0].text

            # Try to parse JSON from response
            try:
                # Look for JSON in code blocks or raw text
                if '```json' in response_text:
                    json_str = response_text.split('```json')[1].split('```')[0].strip()
                elif '```' in response_text:
                    json_str = response_text.split('```')[1].split('```')[0].strip()
                else:
                    json_str = response_text.strip()

                result = json.loads(json_str)

                # Add engagement scores
                for variant in result.values():
                    if isinstance(variant, dict):
                        variant['engagement_score'] = self._calculate_engagement_score(variant)

                return result

            except json.JSONDecodeError:
                # Fallback: return template-based copy
                return self._generate_template_copy(product_name, price, features, market, objective)

        except Exception as e:
            print(f"Error generating copy: {str(e)}")
            # Fallback to template
            return self._generate_template_copy(product_name, price, features, market, objective)

    def _build_prompt(
        self,
        product_name: str,
        price: str,
        features: str,
        market: str,
        objective: str,
        description: str
    ) -> str:
        """Build the prompt for Claude API"""

        market_context = {
            'SI': 'Slovenian market - use casual Slovenian language, emphasize local trust and fast delivery from EU',
            'DE': 'German market - professional yet friendly tone, emphasize quality and efficiency',
            'IT': 'Italian market - warm, family-oriented tone, emphasize style and value',
            'AT': 'Austrian market - similar to German but slightly more casual, emphasize reliability',
            'HR': 'Croatian market - similar to Slovenian, casual and friendly',
            'BA': 'Bosnian market - warm, straightforward tone'
        }

        market_tone = market_context.get(market, 'European market - professional and trustworthy tone')

        prompt = f"""You are an expert Facebook ads copywriter specializing in dropshipping products for European markets.

Product: {product_name}
Price: {price}
Features: {features}
Description: {description}
Target Market: {market} - {market_tone}
Ad Objective: {objective}

Generate 3 Facebook ad copy variants optimized for {objective}.

CRITICAL REQUIREMENTS:
1. Hook must grab attention in first 3 words
2. MUST emphasize "Ships from EU warehouse - 2-3 day delivery" (NOT from China) - this is the main differentiator vs Temu/AliExpress
3. Include trust signals: "100% money-back guarantee", "Thousands of satisfied customers", or "Verified reviews"
4. Use casual, conversational tone (UGC-style, not corporate)
5. Keep under 150 words per variant
6. Include 2-3 relevant emojis
7. Each variant tests different angle:
   - Variant 1: Pain point (what problem does this solve?)
   - Variant 2: Benefit/transformation (how will life improve?)
   - Variant 3: Social proof (what are others saying?)

Format as JSON:
{{
  "variant_1": {{
    "angle": "pain_point",
    "hook": "First 3 words that grab attention",
    "body": "Main ad copy text (conversational, casual tone)",
    "cta": "Call to action (e.g., Shop Now, Get Yours, Limited Stock)",
    "character_count": X
  }},
  "variant_2": {{
    "angle": "benefit",
    "hook": "First 3 words that grab attention",
    "body": "Main ad copy text (conversational, casual tone)",
    "cta": "Call to action",
    "character_count": X
  }},
  "variant_3": {{
    "angle": "social_proof",
    "hook": "First 3 words that grab attention",
    "body": "Main ad copy text (conversational, casual tone)",
    "cta": "Call to action",
    "character_count": X
  }}
}}

Make each variant feel authentic and human - like a friend recommending a product, not a salesy ad.
Use emojis naturally (not overboard).
The EU shipping advantage is MANDATORY to mention in every variant.
"""
        return prompt

    def _calculate_engagement_score(self, variant: Dict) -> int:
        """
        Calculate simple heuristic engagement score (0-100)

        Factors:
        - Hook length (shorter is better)
        - Emoji usage (2-3 is ideal)
        - Character count (under 125 is better)
        - Trust signals present
        - CTA clarity
        """
        score = 50  # Base score

        full_text = f"{variant.get('hook', '')} {variant.get('body', '')} {variant.get('cta', '')}"

        # Hook length (shorter = better)
        hook_words = len(variant.get('hook', '').split())
        if hook_words <= 3:
            score += 15
        elif hook_words <= 5:
            score += 10
        else:
            score += 5

        # Emoji count (2-3 ideal)
        emoji_count = sum(1 for char in full_text if ord(char) > 127000)
        if 2 <= emoji_count <= 3:
            score += 15
        elif emoji_count == 1 or emoji_count == 4:
            score += 10
        else:
            score += 5

        # Character count (under 125 ideal for mobile)
        char_count = variant.get('character_count', 150)
        if char_count < 125:
            score += 10
        elif char_count < 150:
            score += 5

        # Trust signals
        trust_keywords = ['guarantee', 'reviews', 'verified', 'satisfied', 'customers', 'money-back']
        body_lower = variant.get('body', '').lower()
        if any(keyword in body_lower for keyword in trust_keywords):
            score += 10

        # EU shipping mention
        eu_keywords = ['eu warehouse', 'eu shipping', 'ships from eu', 'fast delivery', 'quick delivery']
        if any(keyword in body_lower for keyword in eu_keywords):
            score += 10  # Bonus for critical differentiator

        return min(score, 100)

    def _generate_template_copy(
        self,
        product_name: str,
        price: str,
        features: str,
        market: str,
        objective: str
    ) -> Dict:
        """Fallback template-based copy generation"""

        return {
            "variant_1": {
                "angle": "pain_point",
                "hook": "Tired of waiting?",
                "body": f"Get your {product_name} delivered in just 2-3 days from our EU warehouse! 🚚 No more month-long shipping from China. {features} Now just {price}. 100% money-back guarantee! ✅",
                "cta": "Shop Now - Fast EU Delivery!",
                "character_count": 150,
                "engagement_score": 75
            },
            "variant_2": {
                "angle": "benefit",
                "hook": "Imagine this...",
                "body": f"Your {product_name} arrives in 2-3 days (yes, really! 🎉). Ships from EU warehouse - no customs, no delays. {features} Limited stock at {price}. Thousands of happy customers across Europe! 💯",
                "cta": "Get Yours Today!",
                "character_count": 145,
                "engagement_score": 78
            },
            "variant_3": {
                "angle": "social_proof",
                "hook": "Everyone's talking about...",
                "body": f"The {product_name} that's gone viral! ⭐ Verified 5-star reviews. Fast 2-3 day EU shipping (not from China!). {features} Only {price} with money-back guarantee. Don't miss out!",
                "cta": "Join Thousands of Happy Customers!",
                "character_count": 140,
                "engagement_score": 82
            }
        }
