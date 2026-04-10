import { useEffect, useState } from "react";
import Product from "../components/Product";
import Loader from "../components/Loader";

type ProductType = {
  id: string;
  name: string;
  price: number;
  brand: string;
  description: string;
  quantity: number;
  category?: string;
};

const ProductList = () => {
  const [products, setProducts] = useState<ProductType[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        setLoading(true);

        const res = await fetch("http://127.0.0.1:8001/products/");
        const data = await res.json();

        setProducts(data.data.data);
      } catch {
        setError("Failed to load products");
      } finally {
        setLoading(false);
      }
    };

    fetchProducts();
  }, []);

  if (loading) return <Loader />;
  if (error)
    return <div style={{ background: "#ffe6e6", padding: 10 }}>{error}</div>;

  return (
    <div style={{ padding: "20px", maxWidth: "900px", margin: "0 auto" }}>
      <h2>Product List</h2>

      {products.length === 0 ? (
        <p>No products found</p>
      ) : (
        products.map((product) => <Product key={product.id} {...product} />)
      )}
    </div>
  );
};

export default ProductList;
