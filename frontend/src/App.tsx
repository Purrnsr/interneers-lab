import Header from "./components/Header";
import Navbar from "./components/Navbar";
import ProductList from "./components/ProductList";

function App() {
  return (
    <div>
      <Header />
      <Navbar />

      <div style={{ padding: "40px", maxWidth: "800px", margin: "0 auto" }}>
        <ProductList />
      </div>
    </div>
  );
}

export default App;
