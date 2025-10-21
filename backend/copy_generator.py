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
        description: str = "",
        model: str = "fast"
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
            model: Model selection - "fast" (Haiku 4.5 - default) or "smart" (Sonnet 4.5)

        Returns:
            Dictionary with 3 ad copy variants
        """
        try:
            prompt = self._build_prompt(
                product_name, price, features, market, objective, description
            )

            # Model selection: fast (Haiku 4.5) or smart (Sonnet 4.5)
            model_map = {
                "fast": "claude-haiku-4-5-20251001",    # Fast, cost-effective
                "smart": "claude-sonnet-4-5-20250929"   # Premium quality
            }
            selected_model = model_map.get(model, "claude-haiku-4-5-20251001")

            message = self.client.messages.create(
                model=selected_model,
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
        """Build the prompt for Claude API using vigoshop.si best practices"""

        market_context = {
            'SI': '''Slovenian market (vigoshop.si style):
- Tone: Casual, friend-recommending-product style (not corporate)
- Use phrases like "Ni problema!" (No problem!), "Samo rezultati!" (Just results!)
- Question hooks: "Ste naveličani...?" (Tired of...?)
- Emphasize local trust: "Tisoči zadovoljnih kupcev po Sloveniji" (Thousands of satisfied customers in Slovenia)
- Fast EU delivery is critical differentiator''',
            'DE': '''German market (vigoshop.si style):
- Tone: Professional but accessible, avoid overly formal language
- Use "Warum zahlen..." (Why pay...) for comparative pricing
- Emphasize quality ("Deutsche Qualität") and efficiency
- Avoid superlatives - use measured enthusiasm
- "Jetzt einkaufen" (Shop now) for CTAs''',
            'IT': '''Italian market (vigoshop.si style):
- Tone: Warm, family-oriented, emotionally engaging
- Use "Per la tua famiglia" (For your family)
- Emphasize style, beauty, and value together
- "La soluzione perfetta" (The perfect solution)
- Family and community language resonates''',
            'AT': '''Austrian market (vigoshop.si style):
- Tone: Similar to German but slightly more casual
- Emphasize reliability and quality
- Professional yet approachable
- Focus on practical benefits''',
            'HR': '''Croatian market (vigoshop.si style):
- Tone: Casual, friendly (similar to Slovenian)
- Direct, straightforward language
- Community-focused messaging
- Emphasize local presence and fast delivery''',
            'BA': '''Bosnian market (vigoshop.si style):
- Tone: Warm, straightforward, no-nonsense
- Direct benefit communication
- Family and practical value emphasis
- Simple, clear language'''
        }

        market_tone = market_context.get(market, 'European market - professional and trustworthy tone, vigoshop.si style')

        prompt = f"""You are an expert Facebook ads copywriter for vigoshop.si, specializing in dropshipping products for European markets.

Product: {product_name}
Price: {price}
Features: {features}
Description: {description}
Target Market: {market}
Market Guidance: {market_tone}
Ad Objective: {objective}

Generate 3 Facebook ad copy variants optimized for {objective} using the proven vigoshop.si advertising formula.

VIGOSHOP.SI FORMULA - CRITICAL REQUIREMENTS:

HOOK STRUCTURE (8-12 words):
- Variant 1: Question hook identifying pain point (e.g., "Ste naveličani...?" / "Tired of...?")
- Variant 2: Benefit-statement hook (e.g., "Hitro do..." / "Quickly to..." / "Imagine this...")
- Variant 3: Social proof hook (e.g., "Everyone's talking about..." / "Join 10,000+...")

BODY COPY STRUCTURE (vigoshop.si PAS framework):
1. Problem-Agitate-Solution opening (2-3 sentences)
2. Benefits formatted as EMOJI-PREFIXED BULLETS:
   🔥 Benefit 1 - Brief explanation
   🎯 Benefit 2 - Brief explanation
   ✅ Benefit 3 - Brief explanation
   💪 Benefit 4 - Brief explanation (if needed)
3. Use effort-elimination language: "brez napora" (without effort), "brez potenja" (no sweating), "samo rezultati" (just results)
4. Time efficiency framing: Quantify time savings (e.g., "20 minut = 2 km tek!")
5. MANDATORY: "Ships from EU warehouse - 2-3 day delivery" (NOT from China) - this is THE key differentiator vs Temu/AliExpress

TRUST SIGNALS (include 2-3):
- "100% money-back guarantee" / "Garancija vračila denarja"
- "Thousands of satisfied customers" / "Tisoči zadovoljnih kupcev"
- "Verified 5-star reviews" / "Verificirane ocene"
- Specific customer testimonial quote (for social proof variant)

TONE & STYLE:
- Casual, friend-recommending-product (NOT corporate or salesy)
- Use exclamation points naturally (≈60% of sentences)
- Emoji density: 1 emoji per 15-20 words
- Keep under 150 words total per variant
- Short sentences, active voice, conversational phrases

URGENCY & SCARCITY (use strategically):
- "Samo danes!" (Only today!) / "Omejena ponudba!" (Limited offer!)
- "Limited stock" / "Don't miss out"
- Add 🎁 for special offers

CTA REQUIREMENTS:
- Direct, action-oriented: "Naročite zdaj" (Order now), "Kliknite zdaj" (Click now)
- Include urgency + benefit: "Shop Now - Fast EU Delivery!"
- Use directional emojis: 👇 ➡️

Format as JSON:
{{
  "variant_1": {{
    "angle": "pain_point",
    "hook": "Question hook identifying pain (8-12 words)",
    "body": "PAS framework body with emoji-bullet benefits. Casual tone. Include EU shipping, trust signals, effort-elimination language.",
    "cta": "Direct action CTA with urgency",
    "character_count": X
  }},
  "variant_2": {{
    "angle": "benefit",
    "hook": "Benefit-statement hook (8-12 words)",
    "body": "Transformation-focused body with emoji-bullet benefits. Time efficiency framing. EU shipping. Trust signals.",
    "cta": "Direct action CTA",
    "character_count": X
  }},
  "variant_3": {{
    "angle": "social_proof",
    "hook": "Social proof hook (8-12 words)",
    "body": "Community-focused body with customer testimonial. Emoji-bullet benefits. EU shipping. FOMO element.",
    "cta": "Community-joining CTA",
    "character_count": X
  }}
}}

EMOJI USAGE GUIDE (vigoshop.si patterns):
- Benefits: 🔥 (intensity), 🎯 (targeted), ✅ (confirmation), 💪 (strength), ⚙️ (technical), ⏱️ (time)
- Delivery: 🚀 (speed), 🚛 (logistics), 📦 (package)
- Deals: 🎁 (gift), 🎉 (celebration), 💰 (savings)
- Emotion: 🙃 (friendly), 😁 (happy), 💎 (value), ⭐ (quality)
- Direction: 👇 (down), ➡️ (right)

Make each variant feel like a helpful friend sharing a clever solution, NOT a corporate ad.
The EU shipping advantage is MANDATORY in every variant - it's the core differentiator.
"""
        return prompt

    def _calculate_engagement_score(self, variant: Dict) -> int:
        """
        Calculate engagement score (0-100) based on vigoshop.si best practices

        Factors:
        - Hook length (8-12 words ideal for vigoshop)
        - Emoji usage (1 per 15-20 words, vigoshop standard)
        - Character count (under 125 is better for mobile)
        - Trust signals present
        - EU shipping mention (mandatory)
        - Problem-first structure (vigoshop PAS framework)
        - Emoji-bullet formatting
        - Effort-elimination language
        - Time/quantity specificity
        """
        score = 40  # Base score

        full_text = f"{variant.get('hook', '')} {variant.get('body', '')} {variant.get('cta', '')}"
        body = variant.get('body', '')
        body_lower = body.lower()
        hook = variant.get('hook', '')

        # Hook length (8-12 words ideal for vigoshop.si)
        hook_words = len(hook.split())
        if 8 <= hook_words <= 12:
            score += 15  # Perfect vigoshop range
        elif 5 <= hook_words <= 7 or 13 <= hook_words <= 15:
            score += 12  # Close to ideal
        elif hook_words <= 4:
            score += 8   # Too short
        else:
            score += 5   # Too long

        # Emoji count (vigoshop: 1 per 15-20 words)
        total_words = len(full_text.split())
        emoji_count = sum(1 for char in full_text if ord(char) > 127000)
        ideal_emoji_range = (total_words / 20, total_words / 15)

        if ideal_emoji_range[0] <= emoji_count <= ideal_emoji_range[1]:
            score += 12  # Optimal vigoshop density
        elif emoji_count >= 2 and emoji_count <= 5:
            score += 10  # Acceptable
        else:
            score += 5

        # Character count (under 125 ideal for mobile)
        char_count = variant.get('character_count', 150)
        if char_count < 125:
            score += 8
        elif char_count < 150:
            score += 5

        # Trust signals (vigoshop uses 2-3 per ad)
        trust_keywords = ['guarantee', 'reviews', 'verified', 'satisfied', 'customers', 'money-back',
                         'garancija', 'tisoči', 'thousands', 'testimonial']
        trust_count = sum(1 for keyword in trust_keywords if keyword in body_lower)
        if trust_count >= 2:
            score += 10
        elif trust_count == 1:
            score += 5

        # EU shipping mention (MANDATORY in vigoshop.si)
        eu_keywords = ['eu warehouse', 'eu shipping', 'ships from eu', 'eu skladišč',
                       'fast delivery', 'quick delivery', '2-3 day', '2-3 dni']
        if any(keyword in body_lower for keyword in eu_keywords):
            score += 10  # Critical differentiator
        else:
            score -= 10  # Penalty for missing this

        # Problem-first structure (vigoshop PAS framework)
        problem_indicators = ['tired of', 'struggling with', 'naveličani', 'problema',
                             'why pay', 'warum zahlen', 'zakaj plačati']
        if any(indicator in body_lower for indicator in problem_indicators):
            score += 8  # Bonus for vigoshop structure

        # Emoji-bullet formatting (vigoshop signature)
        emoji_bullets = ['🔥', '🎯', '✅', '💪', '⚙️', '⏱️']
        if any(bullet in body for bullet in emoji_bullets):
            score += 8  # Bonus for vigoshop formatting

        # Effort-elimination language (vigoshop positioning)
        effort_words = ['without effort', 'brez napora', 'effortless', 'brez potenja',
                       'just results', 'samo rezultati', 'no gym', 'brez fitnesa']
        if any(word in body_lower for word in effort_words):
            score += 5  # Bonus for vigoshop messaging

        # Time/quantity specificity (vigoshop quantification)
        import re
        if re.search(r'\d+\s*(min|minut|hour|dni|day|km|€)', body_lower):
            score += 5  # Bonus for specific claims

        # Urgency language (but penalize overuse)
        urgency_words = ['today', 'now', 'limited', 'danes', 'zdaj', 'omejen']
        urgency_count = sum(1 for word in urgency_words if word in body_lower)
        if urgency_count == 1:
            score += 5  # Appropriate urgency
        elif urgency_count >= 3:
            score -= 5  # Too much urgency (trains distrust per vigoshop analysis)

        return min(max(score, 0), 100)  # Clamp between 0-100

    def _generate_template_copy(
        self,
        product_name: str,
        price: str,
        features: str,
        market: str,
        objective: str
    ) -> Dict:
        """Fallback template-based copy generation (vigoshop.si style)"""

        # Extract first feature for specific benefit
        feature_list = features.split('|')
        first_feature = feature_list[0].strip() if feature_list else "premium quality"

        return {
            "variant_1": {
                "angle": "pain_point",
                "hook": "Tired of waiting weeks for products from China?",
                "body": f"Get your {product_name} delivered in just 2-3 days from our EU warehouse! No more endless waiting. 🚀\n\n🔥 Fast EU shipping - arrives in 2-3 days, not weeks\n🎯 {first_feature}\n✅ 100% money-back guarantee\n💪 Thousands of satisfied customers across Europe\n\nJust {price} with free shipping. Order now! 🎁",
                "cta": "Shop Now - Fast EU Delivery! 👉",
                "character_count": 148,
                "engagement_score": 78
            },
            "variant_2": {
                "angle": "benefit",
                "hook": "Imagine getting premium quality in just 2-3 days...",
                "body": f"Your {product_name} arrives fast from our EU warehouse - no customs, no delays! 😊\n\n🔥 Ships in 2-3 days from EU (not China!)\n🎯 {first_feature}\n⏱️ Save time - no month-long waiting\n✅ Verified 5-star reviews\n\nLimited stock at {price}. Thousands already ordered! 💎",
                "cta": "Get Yours Today! 🚀",
                "character_count": 142,
                "engagement_score": 82
            },
            "variant_3": {
                "angle": "social_proof",
                "hook": "Join 10,000+ happy customers across Europe!",
                "body": f"The {product_name} everyone's talking about! ⭐\n\n\"Best purchase this year - arrived in 2 days!\" - Real customer\n\n🔥 Fast 2-3 day EU shipping\n🎯 {first_feature}\n✅ Money-back guarantee\n💪 Verified reviews\n\nOnly {price}. Don't miss out! 🎁",
                "cta": "Join Thousands of Happy Customers! 👇",
                "character_count": 138,
                "engagement_score": 85
            }
        }
