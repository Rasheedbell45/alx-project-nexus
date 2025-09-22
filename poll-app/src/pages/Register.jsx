import { useState } from "react";
import { register } from "../api";
import { useNavigate, Link } from "react-router-dom";

function Register() {
  const [form, setForm] = useState({ username: "", email: "", password: "" });
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");

    try {
      await register(form);
      setSuccess("Registration successful! Redirecting to login...");
      setTimeout(() => navigate("/login"), 1500);
    } catch (err) {
      setError("Registration failed. Please try again.");
    }
  };

  return (
    <div className="flex h-screen justify-center items-center bg-gray-100">
      <form className="bg-white shadow-lg rounded-2xl p-8 w-96" onSubmit={handleSubmit}>
        <h2 className="text-2xl font-bold mb-6 text-center">Register</h2>

        {error && <div className="text-red-500 mb-4 text-center">{error}</div>}
        {success && <div className="text-green-500 mb-4 text-center">{success}</div>}

        <input
          type="text"
          placeholder="Username"
          className="w-full mb-4 px-4 py-2 border rounded-lg"
          value={form.username}
          onChange={(e) => setForm({ ...form, username: e.target.value })}
          required
        />
        <input
          type="email"
          placeholder="Email"
          className="w-full mb-4 px-4 py-2 border rounded-lg"
          value={form.email}
          onChange={(e) => setForm({ ...form, email: e.target.value })}
          required
        />
        <input
          type="password"
          placeholder="Password"
          className="w-full mb-2 px-4 py-2 border rounded-lg"
          value={form.password}
          onChange={(e) => setForm({ ...form, password: e.target.value })}
          required
        />

        <div className="flex justify-end mb-4 text-sm">
          <Link to="/login" className="text-blue-600 hover:underline">
            Already have an account? Login
          </Link>
        </div>

        <button
          type="submit"
          className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700"
        >
          Register
        </button>
      </form>
    </div>
  );
}

export default Register;
