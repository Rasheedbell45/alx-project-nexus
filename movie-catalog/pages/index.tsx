import { GetServerSideProps } from "next";
import Link from "next/link";
import { fetchMovies } from "../lib/api";

interface Movie {
  id: number;
  title: string;
  poster_path: string;
}

interface Props {
  movies: Movie[];
}

export default function Home({ movies }: Props) {
  return (
    <div>
      <h1>🎬 Popular Movies</h1>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: "1rem" }}>
        {movies.map((movie) => (
          <Link key={movie.id} href={`/movies/${movie.id}`}>
            <div style={{ cursor: "pointer" }}>
              <img
                src={`https://image.tmdb.org/t/p/w500${movie.poster_path}`}
                alt={movie.title}
                style={{ width: "100%", borderRadius: "8px" }}
              />
              <h3>{movie.title}</h3>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}

export const getServerSideProps: GetServerSideProps = async () => {
  const movies = await fetchMovies();
  return { props: { movies } };
};
