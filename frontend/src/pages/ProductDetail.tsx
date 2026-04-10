import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import Loader from "../components/Loader";

type Product = {
  id: string;
  name: string;
  price: number;
  brand: string;
  description: string;
  quantity: number;
  category?: string | null;
};

type Category = {
  id: string;
  title: string;
};

const ProductDetail = () => {
  const { id } = useParams<{ id: string }>();

  const [product, setProduct] = useState<Product | null>(null);
  const [formData, setFormData] = useState<Product | null>(null);

  const [categories, setCategories] = useState<Category[]>([]);
  const [selectedCategory, setSelectedCategory] = useState("");

  const [loading, setLoading] = useState(true);
  const [updating, setUpdating] = useState(false);

  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  useEffect(() => {
    if (!id) return;

    const fetchData = async () => {
      try {
        setLoading(true);

        const productRes = await fetch(`http://127.0.0.1:8001/products/${id}/`);
        const productData = await productRes.json();

        const catRes = await fetch(`http://127.0.0.1:8001/categories/`);
        const catData = await catRes.json();

        setProduct(productData.data);
        setFormData(productData.data);
        setCategories(catData.data);
      } catch {
        setError("Failed to load data");
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [id]);

  const handleUpdate = async () => {
    if (!formData || !product) return;

    try {
      setUpdating(true);
      setError("");
      setSuccess("");

      // ❗ Remove category from PUT
      const { category, ...safeData } = formData;

      const res = await fetch(`http://127.0.0.1:8001/products/${product.id}/`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(safeData),
      });

      const data = await res.json();

      if (!res.ok) throw new Error(data?.error?.message);

      // Category update
      if (selectedCategory) {
        if (product.category) {
          await fetch(
            `http://127.0.0.1:8001/products/${product.id}/remove-category/`,
            { method: "DELETE" },
          );
        }

        const addRes = await fetch(
          `http://127.0.0.1:8001/categories/${selectedCategory}/products/${product.id}/`,
          { method: "POST" },
        );

        if (!addRes.ok) throw new Error("Category update failed");
      }

      // Refetch updated product
      const updatedRes = await fetch(
        `http://127.0.0.1:8001/products/${product.id}/`,
      );
      const updatedData = await updatedRes.json();

      setProduct(updatedData.data);
      setFormData(updatedData.data);

      setSuccess("Product updated successfully ✅");
    } catch {
      setError("Failed to update product");
    } finally {
      setUpdating(false);
    }
  };

  if (loading) return <Loader />;
  if (!product || !formData) return <p>Product not found</p>;

  return (
    <div style={{ padding: "20px", maxWidth: "900px", margin: "0 auto" }}>
      <h2>Edit Product</h2>

      {error && (
        <div style={{ background: "#ffe6e6", padding: 10, borderRadius: 8 }}>
          {error}
        </div>
      )}

      {success && (
        <div style={{ background: "#e6ffed", padding: 10, borderRadius: 8 }}>
          {success}
        </div>
      )}

      <input
        value={formData.name}
        onChange={(e) => setFormData({ ...formData, name: e.target.value })}
      />
      <br />
      <br />

      <input
        type="number"
        value={formData.price}
        onChange={(e) =>
          setFormData({ ...formData, price: Number(e.target.value) })
        }
      />
      <br />
      <br />

      <input
        value={formData.brand}
        onChange={(e) => setFormData({ ...formData, brand: e.target.value })}
      />
      <br />
      <br />

      <textarea
        value={formData.description}
        onChange={(e) =>
          setFormData({ ...formData, description: e.target.value })
        }
      />
      <br />
      <br />

      <input
        type="number"
        value={formData.quantity}
        onChange={(e) =>
          setFormData({ ...formData, quantity: Number(e.target.value) })
        }
      />
      <br />
      <br />

      <p>
        Current Category:{" "}
        {categories.find((c) => c.id === product.category)?.title || "None"}
      </p>

      <select
        value={selectedCategory}
        onChange={(e) => setSelectedCategory(e.target.value)}
      >
        <option value="">Select Category</option>
        {categories.map((cat) => (
          <option key={cat.id} value={cat.id}>
            {cat.title}
          </option>
        ))}
      </select>

      <br />
      <br />

      <button onClick={handleUpdate} disabled={updating}>
        {updating ? "Updating..." : "Update Product"}
      </button>
    </div>
  );
};

export default ProductDetail;
