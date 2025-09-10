import axios from "axios";

const API_URL = "https://fakestoreapi.com/products"; // sample API

export const fetchProducts = async () => {
  try {
    const response = await axios.get(API_URL);
    return response.data;
  } catch (error) {
    console.error("Error fetching products:", error);
    return [];
  }
};
