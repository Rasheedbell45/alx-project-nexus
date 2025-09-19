import { Link } from "react-router-dom";

function Home() {
  return (
    <div className="flex flex-col items-center justify-center h-screen bg-gradient-to-r from-blue-500 to-indigo-600 text-white text-center px-6">
      <h1 className="text-5xl font-bold mb-6">Welcome to Polling App</h1>
      <p className="text-lg mb-8 max-w-xl">
        Create polls, vote, and view results in real-time. A simple yet powerful
        way to collect opinions.
      </p>
      <Link
        to="/login"
        className="bg-white text-blue-600 px-6 py-3 rounded-lg font-semibold hover:bg-gray-100"
      >
        Get Started
      </Link>
    </div>
  );
}

export default Home;
