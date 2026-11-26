
import { useState } from "react";
import DashboardLayout from "../components/DashboardLayout";
import { apiRequest } from "../services/api";

function Standings() {
  const role = localStorage.getItem("role");
  const [championshipId, setChampionshipId] = useState("");
  const [standings, setStandings] = useState([]);
  const [error, setError] = useState("");

  async function loadStandings(e) {
    e.preventDefault();

    try {
      const data = await apiRequest(
        `/championships/${championshipId}/standings`
      );

      setStandings(data);
      setError("");
    } catch (err) {
      setError(err.message);
      setStandings([]);
    }
  }

  return (
    <DashboardLayout role={role}>
      <div className="page-header">
        <div>
          <h1>Championship Standings</h1>
          <p>Track the drivers competing for the title</p>
        </div>
      </div>

      <div className="card form-card">
        <form onSubmit={loadStandings}>
          <input
            type="number"
            placeholder="Enter Championship ID"
            value={championshipId}
            onChange={(e) => setChampionshipId(e.target.value)}
            required
          />

          <button className="primary-button">
            View Standings
          </button>
        </form>
      </div>

      {error && <p className="error-message">{error}</p>}

      <div className="card">
        <h2>Driver Rankings</h2>

        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>Position</th>
                <th>Driver</th>
                <th>Number</th>
                <th>Points</th>
                <th>Wins</th>
                <th>Podiums</th>
              </tr>
            </thead>

            <tbody>
              {standings.map((driver, index) => (
                <tr key={driver.driver_id}>
                  <td>{index + 1}</td>
                  <td>{driver.full_name}</td>
                  <td>{driver.racing_number}</td>
                  <td>{driver.total_points}</td>
                  <td>{driver.wins}</td>
                  <td>{driver.podiums}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {standings.length === 0 && (
          <p>No standings available. Enter a championship ID.</p>
        )}
      </div>
    </DashboardLayout>
  );
}

export default Standings;
