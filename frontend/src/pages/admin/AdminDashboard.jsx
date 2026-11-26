
import { useEffect, useState } from "react";
import DashboardLayout from "../../components/DashboardLayout";
import StatCard from "../../components/StatCard";
import { apiRequest, getToken } from "../../services/api";

function AdminDashboard() {
  const [teams, setTeams] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    loadTeams();
  }, []);

  async function loadTeams() {
    try {
      const data = await apiRequest("/teams");
      setTeams(data);
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <DashboardLayout role="admin">
      <div className="page-header">
        <div>
          <h1>Admin Dashboard</h1>
          <p>Manage your Formula Racing Championship</p>
        </div>
      </div>

      <div className="stats-grid">
        <StatCard
          title="Total Teams"
          value={teams.length}
          description="Registered racing teams"
        />

        <StatCard
          title="Active Teams"
          value={teams.length}
          description="Available teams"
        />

        <StatCard
          title="Platform"
          value="Active"
          description="Championship manager"
        />

        <StatCard
          title="Your Role"
          value="Admin"
          description="Platform administrator"
        />
      </div>

      <div className="card">
        <h2>Registered Teams</h2>

        {error && <p className="error-message">{error}</p>}

        {teams.length === 0 ? (
          <p>No teams registered yet.</p>
        ) : (
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Team ID</th>
                  <th>Team Name</th>
                  <th>Country</th>
                  <th>Manager ID</th>
                </tr>
              </thead>

              <tbody>
                {teams.map((team) => (
                  <tr key={team.team_id}>
                    <td>{team.team_id}</td>
                    <td>{team.team_name}</td>
                    <td>{team.country}</td>
                    <td>{team.manager_id}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </DashboardLayout>
  );
}

export default AdminDashboard;
