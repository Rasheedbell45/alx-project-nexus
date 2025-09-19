import React, { useState } from "react";

export default function PollForm({ onCreate }) {
  const [question, setQuestion] = useState("");
  const [options, setOptions] = useState(["", ""]);

  const handleAddOption = () => setOptions([...options, ""]);
  const handleOptionChange = (idx, value) => {
    const arr = [...options];
    arr[idx] = value;
    setOptions(arr);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const opts = options.filter(Boolean).map((t) => ({ text: t }));
    if (!question || opts.length < 2) {
      alert("Provide a question and at least two options");
      return;
    }
    onCreate({ question, options: opts });
    setQuestion("");
    setOptions(["", ""]);
  };

  return (
    <form onSubmit={handleSubmit} className="bg-white p-4 rounded shadow">
      <h2 className="text-xl font-semibold mb-2">Create a Poll</h2>
      <input
        className="w-full p-2 border rounded mb-2"
        placeholder="Poll question"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
      />
      <div className="mb-2">
        {options.map((opt, idx) => (
          <input
            key={idx}
            className="w-full p-2 border rounded mb-2"
            placeholder={`Option ${idx + 1}`}
            value={opt}
            onChange={(e) => handleOptionChange(idx, e.target.value)}
          />
        ))}
      </div>
      <div className="flex gap-2">
        <button type="button" onClick={handleAddOption} className="px-3 py-1 bg-gray-200 rounded">
          + Add option
        </button>
        <button type="submit" className="px-4 py-1 bg-blue-600 text-white rounded">
          Create Poll
        </button>
      </div>
    </form>
  );
}
