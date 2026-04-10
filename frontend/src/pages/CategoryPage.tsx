import { useParams } from "react-router-dom";
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

type Category = {
  id: string;
  title: string;
};

const CategoryPage = () => {
  const { id } = useParams<{ id: string }>();

  const [products, setProducts] = useState<ProductType[]>([]);
  const [category, setCategory] = useState<Category | null>(null);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!id) return;

    const fetchData = async () => {
      try {
        setLoading(true);

        const catRes = await fetch(`http://127.0.0.1:8001/categories/${id}/`);
        const catData = await catRes.json();

        const prodRes = await fetch(
          `http://127.0.0.1:8001/categories/${id}/products/`,
        );
        const prodData = await prodRes.json();

        setCategory(catData.data);
        setProducts(prodData.data);
      } catch {
        setError("Failed to load category data");
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [id]);

  if (loading) return <Loader />;
  if (error)
    return <div style={{ background: "#ffe6e6", padding: 10 }}>{error}</div>;

  return (
    <div style={{ padding: "20px", maxWidth: "900px", margin: "0 auto" }}>
      <button onClick={() => window.history.back()}>← Back</button>

      <h2>Category: {category?.title}</h2>

      {products.length === 0 ? (
        <p>No products found in this category</p>
      ) : (
        products.map((product) => (
          <Product key={product.id} {...product} showCategoryLink={false} />
        ))
      )}
    </div>
  );
};

export default CategoryPage;
