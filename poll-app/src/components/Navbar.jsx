import { Link, useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";

function Navbar() {
  const [isLoggedIn, setIsLoggedIn] = useState(
    !!localStorage.getItem("token")
  );
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("token");
    setIsLoggedIn(false);
    navigate("/login");
  };

  useEffect(() => {
    const handleLoginEvent = () => {
      setIsLoggedIn(true);
    };

    window.addEventListener("login", handleLoginEvent);

    return () => {
      window.removeEventListener("login", handleLoginEvent);
    };
  }, []);

  return (
    <nav className="bg-blue-600 text-white px-6 py-4 flex justify-between items-center">
      <h1 className="text-2xl font-bold">Polling App</h1>

      <div className="space-x-4 flex items-center">
        <Link to="/" className="hover:underline">Home</Link>
        <Link to="/about" className="hover:underline">About</Link>
        <Link to="/contact" className="hover:underline">Contact</Link>

        {isLoggedIn ? (
          <button
            onClick={handleLogout}
            className="bg-white text-blue-600 px-3 py-1 rounded-lg hover:bg-gray-200"
          >
            Logout
          </button>
        ) : (
          <>
            <Link to="/login" className="hover:underline">Login</Link>
            <Link
              to="/register"
              className="bg-white text-blue-600 px-3 py-1 rounded-lg hover:bg-gray-200"
            >
              Get Started
            </Link>
          </>
        )}
      </div>
    </nav>
  );
}

export default Navbar;
