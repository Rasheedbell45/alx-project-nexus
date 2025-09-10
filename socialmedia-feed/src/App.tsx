import React from "react";
import Feed from "./components/Feed";

function App() {
  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-purple-600 text-white text-center p-4 text-xl font-bold">
        🌐 Social Media Feed
      </header>
      <main className="p-4">
        <Feed />
      </main>
    </div>
  );
}

export default App;
