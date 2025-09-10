import React, { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { loadProducts } from "../store/productSlice";
import { RootState, AppDispatch } from "../store";

const ProductList: React.FC = () => {
  const dispatch = useDispatch<AppDispatch>();
  const { items, status } = useSelector((state: RootState) => state.products);

  useEffect(() => {
    dispatch(loadProducts());
  }, [dispatch]);

  if (status === "loading") return <p>Loading...</p>;
  if (status === "failed") return <p>Error loading products.</p>;

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 p-4">
      {items.map((product: any) => (
        <div key={product.id} className="border rounded-lg p-4 shadow hover:shadow-lg">
          <img src={product.image} alt={product.title} className="h-40 w-full object-contain mb-2" />
          <h3 className="text-sm font-semibold">{product.title}</h3>
          <p className="text-gray-500">${product.price}</p>
        </div>
      ))}
    </div>
  );
};

export default ProductList;
