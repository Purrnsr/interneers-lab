import { useState } from "react";
import "./Product.css";

type ProductProps = {
  name: string;
  price: number;
  brand: string;
  description: string;
  quantity: number;
};

const Product = ({
  name,
  price,
  brand,
  description,
  quantity,
}: ProductProps) => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div
      className="product-card"
      onClick={() => setIsOpen(!isOpen)}
      style={{ cursor: "pointer" }}
    >
      <div className="product-name">{name}</div>
      <div className="product-price">₹{price}</div>
      <div className="product-brand">{brand}</div>

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
