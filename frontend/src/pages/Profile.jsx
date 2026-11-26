
import { useState } from "react";
import DashboardLayout from "../components/DashboardLayout";
import { apiRequest } from "../services/api";

function Profile() {
  const role = localStorage.getItem("role");
  const username = localStorage.getItem("username");

  const [performance, setPerformance] = useState(null);
  const [error, setError] = useState("");

  async function loadPerformance() {
    try {
      const data = await apiRequest(
        `/drivers/${encodeURIComponent(username)}/performance`
      );

      setPerformance(data);
      setError("");
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <DashboardLayout role={role}>
      <div className="page-header">
        <div>
          <h1>Driver Profile</h1>
          <p>Your personal racing information</p>
        </div>
      </div>

      <div className="card">
        <h2>{username}</h2>
        <p>Account role: {role}</p>

        <button
          className="primary-button"
          onClick={loadPerformance}
        >
          Load Performance
        </button>

        {error && <p className="error-message">{error}</p>}

        {performance && (
          <pre className="performance-data">
            {JSON.stringify(performance, null, 2)}
          </pre>
        )}
      </div>
    </DashboardLayout>
  );
}

export default Profile;
