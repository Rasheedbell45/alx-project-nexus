import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { getResults } from "../api";

export default function Results() {
  const { id } = useParams();
  const [data, setData] = useState(null);

  const fetchResults = async () => {
    try {
      const res = await getResults(id);
      setData(res.data);
    } catch (err) {
      console.error(err);
      alert("Failed to fetch results");
    }
  };

  useEffect(() => {
    fetchResults();
    const interval = setInterval(fetchResults, 5000); // poll every 5s for "real-time" feel
    return () => clearInterval(interval);
  }, [id]);

  if (!data) return <div className="p-6">Loading...</div>;

  return (
    <div className="p-6 max-w-3xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">{data.question}</h1>
      <div className="space-y-3">
        {data.options.map((opt) => (
          <div key={opt.id} className="p-3 bg-white rounded shadow flex justify-between">
            <div>{opt.label}</div>
            <div className="font-semibold">{opt.votes_count}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
