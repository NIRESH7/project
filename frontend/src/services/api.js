const getApiBaseUrl = () => {
  if (import.meta.env.VITE_API_BASE_URL) {
    return import.meta.env.VITE_API_BASE_URL;
  }
  if (typeof window !== "undefined") {
    // Vite local dev server (port 5173, 3000, etc.)
    if (window.location.port === "5173" || window.location.port === "3000") {
      return "http://localhost:8000";
    }
    // Production / Deployed environment:
    // Use relative path "" which goes through Nginx reverse proxy (/api/) on the same origin,
    // eliminating all CORS and Private Network Access restrictions.
    return "";
  }
  return "http://localhost:8000";
};

const API_BASE_URL = getApiBaseUrl();

export async function fetchProducts(category = "All", maxPrice = null) {
  try {
    let url = `${API_BASE_URL}/api/products`;
    const params = new URLSearchParams();
    if (category && category !== "All") params.append("category", category);
    if (maxPrice) params.append("max_price", maxPrice);
    if (params.toString()) url += `?${params.toString()}`;

    const res = await fetch(url);
    if (!res.ok) throw new Error("Failed to fetch products");
    return await res.json();
  } catch (err) {
    console.error("API error in fetchProducts:", err);
    throw err;
  }
}

export async function fetchCategories() {
  try {
    const res = await fetch(`${API_BASE_URL}/api/categories`);
    if (!res.ok) throw new Error("Failed to fetch categories");
    return await res.json();
  } catch (err) {
    console.error("API error in fetchCategories:", err);
    return ["All", "Smartphones", "Audio", "Laptops", "Accessories", "Wearables"];
  }
}

export async function getRecommendations(query) {
  try {
    const res = await fetch(`${API_BASE_URL}/api/recommend`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ query }),
    });
    if (!res.ok) {
      const errData = await res.json().catch(() => ({}));
      throw new Error(errData.detail || "Failed to generate recommendations");
    }
    return await res.json();
  } catch (err) {
    console.error("API error in getRecommendations:", err);
    throw err;
  }
}
