import json
import logging
import urllib.request
from openai import OpenAI
from config import (
    GEMINI_API_KEY_1, GEMINI_API_KEY_2, GEMINI_API_KEY_3,
    GEMINI_API_KEY_4, GEMINI_API_KEY_5,
    OPENAI_API_KEY, OPENAI_FALLBACK_API_KEY
)

logger = logging.getLogger(__name__)

GEMINI_MODEL = "gemini-2.5-flash"
GEMINI_KEYS = [GEMINI_API_KEY_1, GEMINI_API_KEY_2, GEMINI_API_KEY_3, GEMINI_API_KEY_4, GEMINI_API_KEY_5]

# Initialize OpenAI clients (fallback only)
openai_client = None
if OPENAI_API_KEY:
    try:
        openai_client = OpenAI(api_key=OPENAI_API_KEY)
        logger.info("OpenAI primary client initialized (fallback).")
    except Exception as e:
        logger.error(f"Failed to initialize OpenAI primary client: {e}")

openai_fallback_client = None
if OPENAI_FALLBACK_API_KEY:
    try:
        openai_fallback_client = OpenAI(api_key=OPENAI_FALLBACK_API_KEY)
        logger.info("OpenAI fallback client initialized (fallback).")
    except Exception as e:
        logger.error(f"Failed to initialize OpenAI fallback client: {e}")

def get_ai_recommendations(user_query: str, products: list):
    """
    Given the user preference prompt and all catalog products,
    uses OpenAI GPT to return recommended product IDs and reasons.
    """
    # Prepare a condensed representation of products
    product_summaries = [
        {
            "id": p["id"],
            "title": p["title"],
            "category": p["category"],
            "price": p["price"],
            "specs": p["specs"],
            "description": p["description"]
        }
        for p in products
    ]

    system_prompt = (
        "You are an expert AI product recommendation assistant. "
        "Your task is to analyze user preferences and select the best matching products from the provided catalog.\n"
        "Rules:\n"
        "1. Strictly only pick products that match the user's intent, price range, category, or features.\n"
        "2. For each recommended product, provide a concise, compelling 1-sentence reason explaining why it matches.\n"
        "3. Include a high-level summary overview.\n"
        "4. Return STRICT JSON with keys: 'summary' (string) and 'recommendations' (array of objects with 'id' (int) and 'reason' (string)).\n"
        "5. If no items match, return an empty array for recommendations and explain politely in 'summary'."
    )

    user_content = (
        f"User Preference: \"{user_query}\"\n\n"
        f"Product Catalog:\n{json.dumps(product_summaries, indent=2)}"
    )

    # Fallback heuristic if API key quota is exhausted or fails
    def fallback_recommendations():
        q = user_query.lower()
        matched = []
        
        # Check explicit price limit like "under 500" or "$500"
        import re
        max_price_limit = None
        price_matches = re.findall(r'(?:under|<|\$)\s*(\d+)', q) or re.findall(r'(\d+)\s*(?:dollars|\$)?', q)
        if price_matches:
            try:
                max_price_limit = float(price_matches[0])
            except ValueError:
                pass

        # Detect multi-category intent using whole-word matching
        categories_intent = set()

        def has_word(words):
            return any(re.search(r'\b' + re.escape(w) + r'\b', q) for w in words)

        if has_word(["headphone", "headphones", "audio", "earphone", "earphones", "sound", "earbuds", "noise"]):
            categories_intent.add("Audio")
        if has_word(["laptop", "laptops", "computer", "notebook", "pc"]):
            categories_intent.add("Laptops")
        if has_word(["mouse", "keyboard", "monitor", "accessory", "accessories"]):
            categories_intent.add("Accessories")
        if has_word(["watch", "smartwatch", "fitness", "wearable", "wearables"]):
            categories_intent.add("Wearables")
        if has_word(["phone", "phones", "smartphone", "smartphones", "mobile", "android", "iphone"]):
            categories_intent.add("Smartphones")

        # Check if query has any relevant intent or keywords
        irrelevant_words = {"hi", "hii", "hello", "hey", "test", "testing", "asdf", "xyz", "what", "ok", "cool", "tell", "me"}
        tokens = [w for w in re.findall(r'\b[a-zA-Z0-9]+\b', q) if w not in ["i", "want", "a", "the", "for", "with", "show", "me", "find", "give", "need", "tell", "and"]]

        if not categories_intent and max_price_limit is None:
            # Check if any significant token matches catalog titles, categories, or specs
            has_relevant_keywords = any(
                any(t in (p['title'] + " " + p['category'] + " " + p['description'] + " " + " ".join(p['specs'])).lower() for t in tokens if len(t) >= 3 and t not in irrelevant_words)
                for p in products
            )
            if not has_relevant_keywords or all(t in irrelevant_words for t in tokens):
                return {
                    "summary": f"No matches found for \"{user_query}\". Please try entering a product type, budget, or preferred feature (e.g., 'phone under $500' or 'wireless headphones').",
                    "recommendations": []
                }

        for p in products:
            # 1. Multi-category check if user requested one or more categories
            if categories_intent and p['category'] not in categories_intent:
                continue

            # 2. Strict price check if user stated a budget
            if max_price_limit is not None and p['price'] > max_price_limit:
                continue

            # 3. If keyword search without specific category, require at least one relevant token match
            if not categories_intent and max_price_limit is None:
                p_text = f"{p['title']} {p['category']} {p['description']} {' '.join(p['specs'])}".lower()
                if not any(t in p_text for t in tokens if len(t) >= 3 and t not in irrelevant_words):
                    continue

            # 4. Descriptive reason matching user request
            specs_snippet = ", ".join(p['specs'][:2]) if p['specs'] else "premium build"
            matched.append({
                "id": p["id"],
                "reason": f"Top pick in {p['category']} priced at ${p['price']:.2f} with {specs_snippet}."
            })

        summary_text = (
            f"Found {len(matched)} matching items for \"{user_query}\"."
            if matched else
            f"No matches found for \"{user_query}\". Try searching for phones, laptops, headphones, or accessories under a specific budget."
        )

        return {
            "summary": summary_text,
            "recommendations": matched
        }

    def call_gemini(api_key, key_label):
        """Call Gemini API with the given key and return parsed JSON result."""
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={api_key}"
        gemini_prompt = (
            f"{system_prompt}\n\n"
            f"IMPORTANT: Return ONLY valid JSON, no markdown, no code fences.\n\n"
            f"{user_content}"
        )
        payload = json.dumps({
            "contents": [{"parts": [{"text": gemini_prompt}]}],
            "generationConfig": {"temperature": 0.2}
        }).encode("utf-8")
        req = urllib.request.Request(
            url, data=payload,
            headers={"Content-Type": "application/json"}
        )
        resp = urllib.request.urlopen(req, timeout=15)
        data = json.loads(resp.read())
        raw_text = data["candidates"][0]["content"]["parts"][0]["text"].strip()
        # Strip markdown code fences if present
        if raw_text.startswith("```"):
            raw_text = raw_text.split("\n", 1)[-1].rsplit("```", 1)[0].strip()
        result = json.loads(raw_text)
        logger.info(f"Gemini response received using {key_label}.")
        return result

    def call_openai(api_client, key_label):
        """Attempt an OpenAI API call with the given client."""
        response = api_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            response_format={"type": "json_object"},
            temperature=0.2
        )
        content = response.choices[0].message.content
        logger.info(f"OpenAI response received using {key_label}.")
        return json.loads(content)

    # --- Step 1: Try Gemini keys (primary - FREE) ---
    gemini_key_labels = ["GEMINI KEY1", "GEMINI KEY2", "GEMINI KEY3"]
    for api_key, label in zip(GEMINI_KEYS, gemini_key_labels):
        if not api_key:
            continue
        try:
            return call_gemini(api_key, label)
        except Exception as e:
            logger.warning(f"{label} failed: {e}. Trying next...")

    # --- Step 2: Try OpenAI primary key ---
    if openai_client:
        try:
            return call_openai(openai_client, "OPENAI PRIMARY")
        except Exception as e:
            logger.warning(f"OpenAI primary failed: {e}. Trying OpenAI fallback...")

    # --- Step 3: Try OpenAI fallback key ---
    if openai_fallback_client:
        try:
            return call_openai(openai_fallback_client, "OPENAI FALLBACK")
        except Exception as e:
            logger.warning(f"OpenAI fallback failed: {e}. Using heuristic fallback.")

    # --- Step 4: Local heuristic fallback ---
    logger.warning("All AI keys failed. Using local heuristic fallback.")
    return fallback_recommendations()
