import { useState } from "react";
import { login } from "../api";
import { useNavigate, Link } from "react-router-dom";

function Login() {
  const [form, setForm] = useState({ username: "", password: "" });
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");

    try {
      const res = await login(form);
      localStorage.setItem("token", res.data.access);

      // Notify Navbar and other components
      window.dispatchEvent(new Event("login"));

      setSuccess("Login successful! Redirecting...");
      setTimeout(() => navigate("/polls"), 1000);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          "Login failed. Please check your username and password."
      );
    }
  };

  return (
    <div className="flex h-screen justify-center items-center bg-gray-100">
      <form
        onSubmit={handleSubmit}
        className="bg-white shadow-lg rounded-2xl p-8 w-96"
      >
        <h2 className="text-2xl font-bold mb-6 text-center">Login</h2>

        {error && <div className="text-red-500 mb-4 text-center">{error}</div>}
        {success && (
          <div className="text-green-500 mb-4 text-center">{success}</div>
        )}

        <input
          type="text"
          name="username"
          placeholder="Username"
          className="w-full mb-4 px-4 py-2 border rounded-lg"
          value={form.username}
          onChange={handleChange}
        />
        <input
          type="password"
          name="password"
          placeholder="Password"
          className="w-full mb-2 px-4 py-2 border rounded-lg"
          value={form.password}
          onChange={handleChange}
        />

        <div className="flex justify-between mb-4 text-sm">
          <Link to="/forgot-password" className="text-blue-600 hover:underline">
            Forgot password?
          </Link>
          <Link to="/register" className="text-blue-600 hover:underline">
            No account? Register
          </Link>
        </div>

        <button
          type="submit"
          className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700"
        >
          Login
        </button>
      </form>
    </div>
  );
}

export default Login;
