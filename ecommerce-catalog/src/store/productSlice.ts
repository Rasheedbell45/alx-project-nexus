import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import { fetchProducts } from "../api/products";

export const loadProducts = createAsyncThunk("products/load", async () => {
  const products = await fetchProducts();
  return products;
});

interface ProductState {
  items: any[];
  status: "idle" | "loading" | "succeeded" | "failed";
}

const initialState: ProductState = {
  items: [],
  status: "idle",
};

const productSlice = createSlice({
  name: "products",
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(loadProducts.pending, (state) => {
        state.status = "loading";
      })
      .addCase(loadProducts.fulfilled, (state, action) => {
        state.status = "succeeded";
        state.items = action.payload;
      })
      .addCase(loadProducts.rejected, (state) => {
        state.status = "failed";
      });
  },
});

export default productSlice.reducer;
