import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Product.css";

type ProductProps = {
  id: string;
  name: string;
  price: number;
  brand: string;
  description: string;
  quantity: number;
  category?: string;
  showCategoryLink?: boolean; // ✅ controls UI behavior
};

const Product = ({
  id,
  name,
  price,
  brand,
  description,
  quantity,
  category,
  showCategoryLink = true, // ✅ default behavior
}: ProductProps) => {
  const [isOpen, setIsOpen] = useState(false);
  const navigate = useNavigate();

  return (
    <div
      className="product-card"
      onClick={() => navigate(`/products/${id}`)}
      style={{ cursor: "pointer" }}
    >
      <div className="product-name">{name}</div>
      <div className="product-price">₹{price}</div>
      <div className="product-brand">{brand}</div>

      {/* 🔥 CATEGORY LINK (CONTROLLED) */}
      {showCategoryLink && category && (
        <p
          style={{ color: "blue", cursor: "pointer" }}
          onClick={(e) => {
            e.stopPropagation(); // ✅ prevents card click
            navigate(`/categories/${category}`);
          }}
        >
          View Category
        </p>
      )}

      {/* OPTIONAL DETAILS (if you want expand later) */}
      {isOpen && (
        <div className="product-details">
          <div>Description: {description}</div>
          <div>Quantity: {quantity}</div>
        </div>
      )}
    </div>
  );
};

export default Product;
