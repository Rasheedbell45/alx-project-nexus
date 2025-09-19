import React from "react";
import { Link } from "react-router-dom";

export default function PollCard({ poll, onVote }) {
  return (
    <div className="bg-white shadow rounded p-4">
      <div className="flex justify-between items-center">
        <h3 className="text-lg font-semibold">{poll.question}</h3>
        <Link to={`/results/${poll.id}`} className="text-sm text-blue-600">Results</Link>
      </div>

      <div className="mt-3 space-y-2">
        {poll.options.map((opt) => (
          <div key={opt.id} className="flex gap-2 items-center">
            <button
              onClick={() => onVote(poll.id, opt.id)}
              className="px-3 py-1 bg-green-600 text-white rounded"
            >
              Vote
            </button>
            <div>
              <div className="font-medium">{opt.text}</div>
              <div className="text-xs text-gray-500">Votes: {opt.votes_count}</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
