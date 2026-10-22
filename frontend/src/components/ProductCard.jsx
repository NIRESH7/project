import React from "react";
import { Sparkles, Star } from "lucide-react";

export default function ProductCard({ product, recommendationReason, onSelect }) {
  const isRecommended = Boolean(recommendationReason);

  return (
    <div className={`product-card ${isRecommended ? "is-recommended" : ""}`} onClick={() => onSelect && onSelect(product)}>
      <div className="product-image-container">
        {isRecommended && (
          <div className="recommended-ribbon">
            ★ AI Pick
          </div>
        )}
        <img
          src={product.image_url || "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=600&auto=format&fit=crop&q=80"}
          alt={product.title}
          className="product-image"
          loading="lazy"
        />
      </div>

      <div className="product-card-body">
        <div className="product-meta-row">
          <span className="product-category">{product.category}</span>
          <span className="product-rating">
            <Star size={13} fill="#f59e0b" color="#f59e0b" />
            {product.rating} ({product.reviews_count})
          </span>
        </div>

        <h3 className="product-title">{product.title}</h3>
        <p className="product-description">{product.description}</p>

        {/* AI Explanation Callout */}
        {isRecommended && (
          <div className="ai-reason-box">
            <span className="ai-reason-label">Why it matches:</span>
            {recommendationReason}
          </div>
        )}

        {/* Specifications pills */}
        <div className="product-specs-list">
          {product.specs?.slice(0, 3).map((spec, index) => (
            <span key={index} className="spec-badge">
              {spec}
            </span>
          ))}
        </div>

        <div className="product-card-footer">
          <span className="product-price">${Number(product.price).toFixed(2)}</span>
          <button
            className="btn-view"
            type="button"
            onClick={(e) => {
              e.stopPropagation();
              onSelect && onSelect(product);
            }}
          >
            View Details
          </button>
        </div>
      </div>
    </div>
  );
}
