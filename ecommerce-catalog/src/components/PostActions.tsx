import React, { useState } from "react";

interface Props {
  postId: string;
}

const PostActions: React.FC<Props> = ({ postId }) => {
  const [likes, setLikes] = useState(0);
  const [comments, setComments] = useState<string[]>([]);
  const [input, setInput] = useState("");

  const handleLike = () => setLikes(likes + 1);
  const handleComment = () => {
    if (input.trim()) {
      setComments([...comments, input]);
      setInput("");
    }
  };

  const handleShare = () => {
    alert(`Post ${postId} shared! `);
  };

  return (
    <div className="mt-3">
      <div className="flex gap-4 mb-2">
        <button onClick={handleLike} className="px-3 py-1 bg-blue-500 text-white rounded">
           Like ({likes})
        </button>
        <button onClick={handleShare} className="px-3 py-1 bg-green-500 text-white rounded">
           Share
        </button>
      </div>
      <div>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Write a comment..."
          className="border px-2 py-1 rounded w-full mb-2"
        />
        <button onClick={handleComment} className="px-3 py-1 bg-purple-500 text-white rounded">
          💬 Comment
        </button>
      </div>
      <ul className="mt-2 text-sm text-gray-700">
        {comments.map((c, i) => (
          <li key={i} className="border-b py-1">{c}</li>
        ))}
      </ul>
    </div>
  );
};

export default PostActions;
