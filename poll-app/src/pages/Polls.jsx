import React, { useEffect, useState } from "react";
import { getPolls, votePoll, createPoll } from "../api";
import PollForm from "../components/PollForm";
import PollCard from "../components/PollCard";

export default function Polls() {
  const [polls, setPolls] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchPolls = async () => {
    try {
      setLoading(true);
      const res = await getPolls();
      setPolls(res.data);
    } catch (err) {
      console.error(err);
      alert("Failed to load polls");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPolls();
  }, []);

  const handleVote = async (pollId, optionId) => {
    try {
      await votePoll(pollId, optionId);
      alert("Vote recorded");
      fetchPolls(); // refresh
    } catch (err) {
      console.error(err);
      const msg = err.response?.data?.detail || "Failed to vote";
      alert(msg);
    }
  };

  const handleCreate = async (payload) => {
    try {
      await createPoll(payload);
      alert("Poll created");
      fetchPolls();
    } catch (err) {
      console.error(err);
      alert("Failed to create poll");
    }
  };

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-4">Polls</h1>

      <div className="mb-6">
        <PollForm onCreate={handleCreate} />
      </div>

      {loading ? (
        <p>Loading...</p>
      ) : (
        <div className="space-y-4">
          {polls.map((p) => (
            <PollCard key={p.id} poll={p} onVote={handleVote} />
          ))}
        </div>
      )}
    </div>
  );
}
