import React from "react";
import { useQuery } from "@apollo/client";
import { GET_LOCATIONS } from "../graphql/queries";

const Feed: React.FC = () => {
  const { loading, error, data } = useQuery(GET_LOCATIONS);

  if (loading) return <p>Loading feed...</p>;
  if (error) return <p>Error loading feed: {error.message}</p>;

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6 p-4">
      {data.locations.map((loc: any) => (
        <div
          key={loc.id}
          className="border rounded-lg shadow-md p-4 hover:shadow-lg transition"
        >
          <img
            src={loc.photo}
            alt={loc.name}
            className="w-full h-48 object-cover rounded-md mb-3"
          />
          <h3 className="text-lg font-bold">{loc.name}</h3>
          <p className="text-sm text-gray-600">{loc.description}</p>
        </div>
      ))}
    </div>
  );
};

export default Feed;
