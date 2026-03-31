// API LAYER

async function fetchProducts() {
    try {
        const response = await fetch("http://127.0.0.1:8001/products/");

        if (!response.ok) {
            throw new Error("Failed to fetch products");
        }

        const data = await response.json();
        return data?.data?.data || [];

    } catch (error) {
        console.error("API Error:", error);
        return [];
    }
}

// DOM RENDERING LAYER

function createProductCard(product) {
    const card = document.createElement("div");
    card.className = "product-card";

    const details = document.createElement("div");
    details.className = "product-details";

    details.innerHTML = `
        <div>Description: ${product.description || "N/A"}</div>
        <div>Quantity: ${product.quantity ?? 0}</div>
    `;

    card.innerHTML = `
        <div class="product-name">${product.name || "Unnamed"}</div>
        <div class="product-price">₹${product.price || 0}</div>
        <div class="product-brand">${product.brand || "Unknown"}</div>
    `;

    card.addEventListener("click", (e) => {
        e.stopPropagation();
        card.classList.toggle("active");
    });

    card.appendChild(details);

    return card;
}

function renderProducts(products) {
    const container = document.getElementById("product-container");

    container.innerHTML = "";

    if (!products || products.length === 0) {
        container.innerHTML = "<p>No products found 😔</p>";
        return;
    }

    products.forEach(product => {
        const card = createProductCard(product);
        container.appendChild(card);
    });
}

// INITIALIZATION

async function init() {
    console.log("Initializing product page...");

    const container = document.getElementById("product-container");
    container.innerHTML = "<p>Loading products...</p>";

    const products = await fetchProducts();

    console.log("Fetched products:", products);

    renderProducts(products);
}

document.addEventListener("DOMContentLoaded", init);