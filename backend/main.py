from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session

from database import engine, get_db, Base
from models import Product
from seed_data import seed_database
from ai_service import get_ai_recommendations

# Initialize Database Schema
Base.metadata.create_all(bind=engine)

# Auto-seed sample products
with next(get_db()) as db:
    seed_database(db)

app = FastAPI(
    title="Product Recommendation AI API",
    description="FastAPI + MySQL/SQLite + OpenAI Recommendation Service",
    version="1.0.0"
)

# Enable CORS for React frontend (development & production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_private_network=True,
)

class RecommendationRequest(BaseModel):
    query: str

class RecommendationItem(BaseModel):
    product: dict
    reason: str

class RecommendationResponse(BaseModel):
    summary: str
    query: str
    total_found: int
    recommendations: List[RecommendationItem]

@app.get("/")
def health_check():
    return {"status": "ok", "service": "Product Recommendation API", "version": "1.0.0"}

@app.get("/api/products")
def list_products(
    category: Optional[str] = None,
    max_price: Optional[float] = None,
    db: Session = Depends(get_db)
):
    """Retrieve catalog products with optional category and max price filters."""
    query = db.query(Product)
    if category and category.lower() != "all":
        query = query.filter(Product.category.ilike(category))
    if max_price is not None:
        query = query.filter(Product.price <= max_price)
    
    products = query.all()
    return [p.to_dict() for p in products]

@app.get("/api/categories")
def list_categories(db: Session = Depends(get_db)):
    """Retrieve all available product categories."""
    categories = db.query(Product.category).distinct().all()
    return ["All"] + [c[0] for c in categories]

@app.post("/api/recommend", response_model=RecommendationResponse)
def recommend_products(req: RecommendationRequest, db: Session = Depends(get_db)):
    """AI Recommendation endpoint that analyzes user input and matches catalog products."""
    user_query = req.query.strip()
    if not user_query:
        raise HTTPException(status_code=400, detail="Query prompt cannot be empty.")

    # Fetch all catalog products from database
    all_products = [p.to_dict() for p in db.query(Product).all()]

    # Ask AI engine
    ai_result = get_ai_recommendations(user_query, all_products)

    # Map back to full product details
    product_map = {p["id"]: p for p in all_products}
    matched_items = []
    
    for rec in ai_result.get("recommendations", []):
        pid = rec.get("id")
        if pid in product_map:
            matched_items.append({
                "product": product_map[pid],
                "reason": rec.get("reason", "Recommended based on your preferences.")
            })

    return {
        "summary": ai_result.get("summary", "Here are the best matches for your search."),
        "query": user_query,
        "total_found": len(matched_items),
        "recommendations": matched_items
    }
