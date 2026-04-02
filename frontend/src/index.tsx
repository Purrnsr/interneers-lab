import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";

const root = ReactDOM.createRoot(
  document.getElementById("product-container") as HTMLElement, // Added comma here
);

root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>, // Added comma here
);
