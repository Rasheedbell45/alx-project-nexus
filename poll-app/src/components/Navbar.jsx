import { NavLink, useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";

function Navbar() {
  const [isLoggedIn, setIsLoggedIn] = useState(
    Boolean(localStorage.getItem("token"))
  );
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("token");
    setIsLoggedIn(false);
    window.dispatchEvent(new Event("logout")); // notify other components
    navigate("/login");
  };

  useEffect(() => {
    const handleLoginEvent = () => setIsLoggedIn(true);
    const handleLogoutEvent = () => setIsLoggedIn(false);

    window.addEventListener("login", handleLoginEvent);
    window.addEventListener("logout", handleLogoutEvent);

    return () => {
      window.removeEventListener("login", handleLoginEvent);
      window.removeEventListener("logout", handleLogoutEvent);
    };
  }, []);

  const linkClass = ({ isActive }) =>
    isActive ? "underline font-bold" : "hover:underline";

  return (
    <nav className="bg-blue-600 text-white px-6 py-4 flex justify-between items-center">
      <h1 className="text-2xl font-bold">Polling App</h1>

      <div className="space-x-4 flex items-center">
        <NavLink to="/" className={linkClass}>Home</NavLink>
        <NavLink to="/about" className={linkClass}>About</NavLink>
        <NavLink to="/contact" className={linkClass}>Contact</NavLink>

        {isLoggedIn ? (
          <button
            onClick={handleLogout}
            className="bg-white text-blue-600 px-3 py-1 rounded-lg hover:bg-gray-200"
          >
            Logout
          </button>
        ) : (
          <>
            <NavLink to="/login" className={linkClass}>Login</NavLink>
            <NavLink
              to="/register"
              className="bg-white text-blue-600 px-3 py-1 rounded-lg hover:bg-gray-200"
            >
              Get Started
            </NavLink>
          </>
        )}
      </div>
    </nav>
  );
}

export default Navbar;
