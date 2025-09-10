import React from "react";
import ProductList from "./components/ProductList";
import Feed from "./components/Feed";

function App() {
  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-blue-600 text-white p-4 text-center text-xl font-bold">
         E-Commerce Catalog
         Social Media Feed
      </header>
      <main className="p-4">
        <ProductList />
        <Feed />
      </main>
    </div>
  );
}

export default App;
