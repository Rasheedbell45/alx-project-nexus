import axios from "axios";

const API_URL = "https://api.themoviedb.org/3";
const API_KEY = process.env.NEXT_PUBLIC_TMDB_API_KEY;

export const fetchMovies = async () => {
  const res = await axios.get(`${API_URL}/movie/popular?api_key=${API_KEY}`);
  return res.data.results;
};

export const fetchMovieById = async (id: string) => {
  const res = await axios.get(`${API_URL}/movie/${id}?api_key=${API_KEY}`);
  return res.data;
};
