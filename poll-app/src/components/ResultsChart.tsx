import React from "react";
import { useSelector } from "react-redux";
import { RootState } from "../store";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

export default function ResultsChart() {
  const poll = useSelector((state: RootState) => state.poll);

  return (
    <div style={{ height: 300, marginTop: "1rem" }}>
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={poll.options}>
          <XAxis dataKey="text" />
          <YAxis allowDecimals={false} />
          <Tooltip />
          <Bar dataKey="votes" fill="#4f46e5" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
