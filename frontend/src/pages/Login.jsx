import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { apiRequest, saveTokens } from "../services/api";

const DASHBOARD_BY_ROLE = {
  admin: "/admin",
  organizer: "/organizer",
  driver: "/driver",
};

function Login() {
  const navigate = useNavigate();

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleLogin(e) {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const data = await apiRequest("/auth/login", "POST", {
        username: username,
        password: password,
      });

      const dashboard = DASHBOARD_BY_ROLE[data.role];
      if (!dashboard) {
        throw new Error(`Unknown account role: ${data.role}`);
      }

      saveTokens(data.access_token, data.refresh_token);
      localStorage.setItem("username", data.username);
      localStorage.setItem("role", data.role);

      navigate(dashboard);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="auth-page">
      <div className="auth-card">
        <h1>F1 <span>MANAGER</span></h1>
        <p>Welcome back to the championship</p>

        <form onSubmit={handleLogin}>
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
            required
          />

          <button className="primary-button" disabled={loading}>
            {loading ? "Logging in..." : "Login"}
          </button>
        </form>

        {error && <p className="error-message">{error}</p>}

        <p>
          Don't have an account? <Link to="/register">Register</Link>
        </p>
      </div>
    </div>
  );
}

export default Login;