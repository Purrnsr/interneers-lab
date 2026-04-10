import Header from "./components/Header";
import Navbar from "./components/Navbar";
import ProductList from "./components/ProductList";
import ProductDetail from "./pages/ProductDetail";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { Navigate } from "react-router-dom";
import CategoryPage from "./pages/CategoryPage";

function App() {
  return (
    <Router>
      <Header />
      <Navbar />

      <div style={{ padding: "40px", maxWidth: "800px", margin: "0 auto" }}>
        <Routes>
          <Route path="/" element={<Navigate to="/products" />} />
          <Route path="/products" element={<ProductList />} />
          <Route path="/products/:id" element={<ProductDetail />} />
          <Route path="/categories/:id" element={<CategoryPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
