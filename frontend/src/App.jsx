import React, { useState, useEffect } from "react";
import { Sparkles, Layers, RefreshCw, AlertCircle, ArrowDown } from "lucide-react";
import SearchSection from "./components/SearchSection";
import ProductCard from "./components/ProductCard";
import ProductModal from "./components/ProductModal";
import { fetchProducts, fetchCategories, getRecommendations } from "./services/api";

export default function App() {
  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState(["All"]);
  const [selectedCategory, setSelectedCategory] = useState("All");
  
  const [query, setQuery] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [recommendationResult, setRecommendationResult] = useState(null);
  const [errorMsg, setErrorMsg] = useState(null);
  const [selectedProduct, setSelectedProduct] = useState(null);

  // Load initial catalog & categories
  useEffect(() => {
    loadCatalog();
  }, []);

  const loadCatalog = async () => {
    try {
      const [prods, cats] = await Promise.all([
        fetchProducts(),
        fetchCategories()
      ]);
      setProducts(prods);
      setCategories(cats);
    } catch (err) {
      console.warn("Backend not yet active or connection error:", err);
    }
  };

  const handleSearch = async (userPrompt) => {
    setIsLoading(true);
    setErrorMsg(null);

    try {
      const result = await getRecommendations(userPrompt);
      setRecommendationResult(result);
    } catch (err) {
      setErrorMsg(err.message || "Unable to get AI recommendation. Please check your backend.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleResetSearch = () => {
    setQuery("");
    setRecommendationResult(null);
    setErrorMsg(null);
  };

  // Build recommendation mapping (id -> reason)
  const recommendationMap = React.useMemo(() => {
    if (!recommendationResult || !recommendationResult.recommendations) return {};
    const map = {};
    recommendationResult.recommendations.forEach((item) => {
      map[item.product.id] = item.reason;
    });
    return map;
  }, [recommendationResult]);

  // Determine which products to display
  const displayedProducts = React.useMemo(() => {
    if (recommendationResult) {
      const recProducts = recommendationResult.recommendations.map(r => r.product);
      return recProducts;
    }

    if (selectedCategory === "All") {
      return products;
    }
    return products.filter((p) => p.category.toLowerCase() === selectedCategory.toLowerCase());
  }, [products, selectedCategory, recommendationResult]);

  return (
    <div className="app-layout">
      {/* Top Navigation */}
      <header className="navbar">
        <div className="navbar-inner">
          <div className="brand-badge">
            <img src="/logo.svg" alt="SmartMatch Logo" className="brand-logo-img" />
            <div className="brand-text-block">
              <span className="brand-title">SmartMatch</span>
              <span className="brand-subtitle">AI Recommendations</span>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="main-content">
        <div className="hero-section">
          <h1 className="hero-heading">AI Product Recommendations</h1>
        </div>

        {/* Search & Prompt Box */}
        <SearchSection
          query={query}
          setQuery={setQuery}
          onSearch={handleSearch}
          isLoading={isLoading}
          onReset={handleResetSearch}
        />

        {/* Error notification */}
        {errorMsg && (
          <div style={{
            padding: "12px 16px",
            backgroundColor: "#fef2f2",
            border: "1px solid #fecaca",
            borderRadius: "8px",
            color: "#991b1b",
            fontSize: "14px",
            marginBottom: "24px",
            display: "flex",
            alignItems: "center",
            gap: "8px"
          }}>
            <AlertCircle size={18} />
            <span>{errorMsg}</span>
          </div>
        )}

        {/* AI Recommendation Summary Banner */}
        {recommendationResult && (
          <div className="recommendation-banner">
            <div className="rec-banner-header">
              <div className="rec-banner-title">
                <Sparkles size={16} className="rec-banner-sparkle" />
                <span>AI Recommendation Summary</span>
              </div>
              <div className="rec-banner-actions">
                <span className="rec-banner-badge">
                  {recommendationResult.total_found} matched
                </span>
                <button
                  type="button"
                  className="rec-clear-btn"
                  onClick={handleResetSearch}
                >
                  Clear AI Filter
                </button>
              </div>
            </div>
            <p className="rec-banner-summary">{recommendationResult.summary}</p>
          </div>
        )}

        {/* Catalog Toolbar */}
        {!recommendationResult && (
          <div className="catalog-toolbar">
            <div className="category-tabs">
              {categories.map((cat) => (
                <button
                  key={cat}
                  className={`tab-btn ${selectedCategory === cat ? "active" : ""}`}
                  onClick={() => setSelectedCategory(cat)}
                >
                  {cat}
                </button>
              ))}
            </div>
            <div className="results-count">
              Showing {displayedProducts.length} items
            </div>
          </div>
        )}

        {/* Product Grid */}
        {displayedProducts.length > 0 ? (
          <div className="products-grid">
            {displayedProducts.map((product) => (
              <ProductCard
                key={product.id}
                product={product}
                recommendationReason={recommendationMap[product.id]}
                onSelect={(p) => setSelectedProduct(p)}
              />
            ))}
          </div>
        ) : (
          <div className="empty-state">
            <h3 className="empty-state-title">No products found</h3>
            <p className="empty-state-desc">
              {recommendationResult?.summary || "Try adjusting your search criteria or resetting filters."}
            </p>
            <button
              type="button"
              className="btn-secondary"
              onClick={handleResetSearch}
            >
              Reset Filters
            </button>
          </div>
        )}

        {/* Product Detail Modal */}
        {selectedProduct && (
          <ProductModal
            product={selectedProduct}
            recommendationReason={recommendationMap[selectedProduct.id]}
            onClose={() => setSelectedProduct(null)}
          />
        )}

        {/* Mobile Floating Scroll Down Button */}
        <button
          type="button"
          className="mobile-scroll-down-btn"
          onClick={() => {
            window.scrollBy({ top: 500, behavior: "smooth" });
          }}
          aria-label="Scroll down"
        >
          <ArrowDown size={20} strokeWidth={2.5} />
        </button>
      </main>

      {/* Clean Minimal Footer */}
      <footer className="footer">
        Product Recommendation Engine • React & FastAPI
      </footer>
    </div>
  );
}
