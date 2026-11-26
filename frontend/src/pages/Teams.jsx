
import { useEffect, useState } from "react";
import DashboardLayout from "../components/DashboardLayout";
import { apiRequest, getToken } from "../services/api";

function Teams() {
  const [teams, setTeams] = useState([]);
  const [error, setError] = useState("");
  const role = localStorage.getItem("role");

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

  async function applyToTeam(teamId) {
    try {
      await apiRequest(
        `/teams/${teamId}/apply`,
        "POST",
        null,
        getToken()
      );

      alert("Application submitted successfully!");
    } catch (err) {
      alert(err.message);
    }
  }

  return (
    <DashboardLayout role={role}>
      <div className="page-header">
        <div>
          <h1>Racing Teams</h1>
          <p>Explore all registered racing teams</p>
        </div>
      </div>

      {error && <p className="error-message">{error}</p>}

      <div className="team-grid">
        {teams.map((team) => (
          <div className="card team-card" key={team.team_id}>
            <h2>{team.team_name}</h2>
            <p>Country: {team.country}</p>
            <p>Manager ID: {team.manager_id}</p>
            <p>Team ID: {team.team_id}</p>

            {role === "driver" && (
              <button
                className="primary-button"
                onClick={() => applyToTeam(team.team_id)}
              >
                Apply to Join
              </button>
            )}
          </div>
        ))}
      </div>

      {teams.length === 0 && !error && (
        <div className="card">
          No racing teams found.
        </div>
      )}
    </DashboardLayout>
  );
}

export default Teams;
