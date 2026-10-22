import React from "react";
import { X, Star, CheckCircle, ShieldCheck, Truck } from "lucide-react";

export default function ProductModal({ product, recommendationReason, onClose }) {
  if (!product) return null;

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <button className="modal-close-btn" onClick={onClose} aria-label="Close modal">
          <X size={20} />
        </button>

        <div className="modal-grid">
          <div className="modal-image-col">
            <img
              src={product.image_url || "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=600&auto=format&fit=crop&q=80"}
              alt={product.title}
              className="modal-image"
            />
          </div>

          <div className="modal-info-col">
            <div className="modal-badge-row">
              <span className="product-category">{product.category}</span>
              {recommendationReason && (
                <span className="modal-ai-tag">★ AI Recommended</span>
              )}
            </div>

            <h2 className="modal-title">{product.title}</h2>

            <div className="modal-rating-row">
              <div className="product-rating">
                <Star size={15} fill="#f59e0b" color="#f59e0b" />
                <span style={{ fontWeight: 700, marginLeft: 4 }}>{product.rating}</span>
                <span style={{ color: "#64748b", marginLeft: 4 }}>
                  ({product.reviews_count} verified customer reviews)
                </span>
              </div>
            </div>

            <div className="modal-price">${Number(product.price).toFixed(2)}</div>

            {recommendationReason && (
              <div className="ai-reason-box" style={{ margin: "16px 0" }}>
                <span className="ai-reason-label">Why it matches your search:</span>
                {recommendationReason}
              </div>
            )}

            <div className="modal-section-title">Overview</div>
            <p className="modal-desc">{product.description}</p>

            <div className="modal-section-title">Specifications</div>
            <div className="modal-specs-list">
              {product.specs?.map((spec, idx) => (
                <div key={idx} className="modal-spec-item">
                  <CheckCircle size={14} color="#10b981" />
                  <span>{spec}</span>
                </div>
              ))}
            </div>

            <div className="modal-perks">
              <div className="modal-perk-item">
                <Truck size={16} />
                <span>Free 2-day delivery</span>
              </div>
              <div className="modal-perk-item">
                <ShieldCheck size={16} />
                <span>1-Year Manufacturer Warranty</span>
              </div>
            </div>

            <button className="btn-primary" style={{ width: "100%", justifyContent: "center", marginTop: 20 }} onClick={onClose}>
              Close Preview
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
