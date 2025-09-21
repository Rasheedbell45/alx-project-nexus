import { useState } from "react";
import { sendPasswordResetEmail } from "../api"; // You need to implement this API call
import { Link } from "react-router-dom";

function ForgotPassword() {
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage("");
    setError("");

    try {
      await sendPasswordResetEmail({ email });
      setMessage("Password reset instructions have been sent to your email.");
    } catch (err) {
      setError("Failed to send reset instructions. Please try again.");
    }
  };

  return (
    <div className="flex h-screen justify-center items-center bg-gray-100">
      <form
        onSubmit={handleSubmit}
        className="bg-white shadow-lg rounded-2xl p-8 w-96"
      >
        <h2 className="text-2xl font-bold mb-6 text-center">Forgot Password</h2>

        {message && <p className="text-green-600 mb-4">{message}</p>}
        {error && <p className="text-red-600 mb-4">{error}</p>}

        <input
          type="email"
          placeholder="Enter your email"
          className="w-full mb-4 px-4 py-2 border rounded-lg"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />

        <button
          type="submit"
          className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700"
        >
          Send Reset Link
        </button>

        <div className="mt-4 text-center text-sm">
          <p>
            Remember your password?{" "}
            <Link to="/login" className="text-blue-600 hover:underline">
              Login
            </Link>
          </p>
          <p className="mt-2">
            Don't have an account?{" "}
            <Link to="/register" className="text-blue-600 hover:underline">
              Register
            </Link>
          </p>
        </div>
      </form>
    </div>
  );
}

export default ForgotPassword;
