import { Link } from "react-router-dom";

function Navbar() {
  return (
    <nav className="bg-blue-600 text-white px-6 py-4 flex justify-between items-center">
      <h1 className="text-2xl font-bold">Polling App</h1>
      <div className="space-x-4">
        <Link to="/" className="hover:underline">Home</Link>
        <Link to="/about" className="hover:underline">About</Link>
        <Link to="/contact" className="hover:underline">Contact</Link>
        <Link to="/login" className="bg-white text-blue-600 px-3 py-1 rounded-lg hover:bg-gray-200">
          Get Started
        </Link>
      </div>
    </nav>
  );
}

export default Navbar;
