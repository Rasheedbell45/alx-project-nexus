import { GetServerSideProps } from "next";
import { fetchMovieById } from "../../lib/api";

interface Movie {
  id: number;
  title: string;
  overview: string;
  poster_path: string;
}

export default function MoviePage({ movie }: { movie: Movie }) {
  return (
    <div>
      <h1>{movie.title}</h1>
      <img
        src={`https://image.tmdb.org/t/p/w500${movie.poster_path}`}
        alt={movie.title}
      />
      <p>{movie.overview}</p>
    </div>
  );
}

export const getServerSideProps: GetServerSideProps = async (context) => {
  const { id } = context.params!;
  const movie = await fetchMovieById(id as string);
  return { props: { movie } };
};
