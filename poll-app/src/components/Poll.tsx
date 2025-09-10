import React from "react";
import { useSelector, useDispatch } from "react-redux";
import { RootState } from "../store";
import { vote } from "../features/pollSlice";

export default function Poll() {
  const poll = useSelector((state: RootState) => state.poll);
  const dispatch = useDispatch();

  return (
    <div>
      <h2>{poll.question}</h2>
      {poll.options.map((option) => (
        <button
          key={option.id}
          onClick={() => dispatch(vote(option.id))}
          style={{ display: "block", margin: "0.5rem 0" }}
        >
          {option.text} ({option.votes} votes)
        </button>
      ))}
    </div>
  );
}
