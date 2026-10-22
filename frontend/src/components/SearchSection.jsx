import React from "react";
import { Sparkles, ArrowRight, Loader2 } from "lucide-react";

const SUGGESTIONS = [
  "I want a phone under $500 with a great camera",
  "Noise cancelling wireless headphones for travel",
  "Budget laptop for work and productivity under $700",
  "Ergonomic accessories for my desk setup"
];

export default function SearchSection({
  query,
  setQuery,
  onSearch,
  isLoading,
  onReset
}) {
  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim()) {
      onSearch(query);
    }
  };

  const handleSuggestionClick = (text) => {
    setQuery(text);
    onSearch(text);
  };

  return (
    <div className="search-card">
      <form onSubmit={handleSubmit}>
        <div className="search-input-wrapper">
          <textarea
            className="search-input search-textarea"
            placeholder="Search by preference (e.g., 'phone under $500', 'ANC headphones')..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            disabled={isLoading}
            rows={2}
          />
          <button
            type="submit"
            className="btn-primary"
            disabled={isLoading || !query.trim()}
          >
            {isLoading ? (
              <>
                <Loader2 size={16} className="btn-spinner" />
                <span>Analyzing...</span>
              </>
            ) : (
              <>
                <Sparkles size={16} />
                <span>Ask AI Recommender</span>
              </>
            )}
          </button>
        </div>
      </form>

      <div className="suggestions-container">
        <span className="suggestions-label">Try asking:</span>
        <div className="suggestions-chips-wrap">
          {SUGGESTIONS.map((suggestion, idx) => (
            <button
              key={idx}
              type="button"
              className="chip-btn"
              onClick={() => handleSuggestionClick(suggestion)}
              disabled={isLoading}
            >
              {suggestion}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
