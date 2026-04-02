import Product from "./Product";

const products = [
  {
    name: "Mouse",
    price: 999,
    brand: "Logitech",
    description: "Wireless mouse",
    quantity: 10,
  },
  {
    name: "Keyboard",
    price: 1999,
    brand: "HP",
    description: "Mechanical keyboard",
    quantity: 5,
  },
  {
    name: "USB Cable",
    price: 299,
    brand: "Boat",
    description: "Fast charging cable",
    quantity: 20,
  },
];

const ProductList = () => {
  return (
    <div>
      {products.map((product, index) => (
        <Product key={index} {...product} />
      ))}
    </div>
  );
};

export default ProductList;
