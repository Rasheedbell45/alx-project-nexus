import React from "react";
import ProductList from "./components/ProductList";

function App() {
  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-blue-600 text-white p-4 text-center text-xl font-bold">
        🛒 E-Commerce Catalog
      </header>
      <main className="p-4">
        <ProductList />
      </main>
    </div>
  );
}

export default App;
