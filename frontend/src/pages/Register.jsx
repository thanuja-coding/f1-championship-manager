
import { useState } from "react";
import { Link } from "react-router-dom";
import { apiRequest } from "../services/api";

function Register() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  async function handleRegister(e) {
    e.preventDefault();

    try {
      const data = await apiRequest(
        "/auth/register",
        "POST",
        {
          username: username,
          password: password,
          role: "driver"
        }
      );

      setMessage(data.message);
      setError("");
      setUsername("");
      setPassword("");
    } catch (err) {
      setError(err.message);
      setMessage("");
    }
  }

  return (
    <div className="auth-page">
      <div className="auth-card">
        <h1>JOIN <span>F1 MANAGER</span></h1>
        <p>Create your driver account</p>

        <form onSubmit={handleRegister}>
          <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />

          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            minLength="6"
            required
          />

          <button className="primary-button">
            Register
          </button>
        </form>

        {error && <p className="error-message">{error}</p>}
        {message && <p className="success-message">{message}</p>}

        <p>
          Already registered? <Link to="/login">Login</Link>
        </p>
      </div>
    </div>
  );
}

export default Register;
