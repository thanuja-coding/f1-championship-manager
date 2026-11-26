
import { useState } from "react";
import DashboardLayout from "../components/DashboardLayout";
import { apiRequest, getToken } from "../services/api";

function Races() {
  const role = localStorage.getItem("role");

  const [championshipId, setChampionshipId] = useState("");
  const [raceName, setRaceName] = useState("");
  const [raceDate, setRaceDate] = useState("");
  const [message, setMessage] = useState("");

  async function scheduleRace(e) {
    e.preventDefault();

    try {
      await apiRequest(
        `/championships/${championshipId}/races`,
        "POST",
        {
          race_name: raceName,
          race_date: raceDate
        },
        getToken()
      );

      setMessage("Race scheduled successfully!");
      setRaceName("");
      setRaceDate("");
    } catch (err) {
      setMessage(err.message);
    }
  }

  return (
    <DashboardLayout role={role}>
      <div className="page-header">
        <div>
          <h1>Race Control</h1>
          <p>Schedule and manage racing events</p>
        </div>
      </div>

      {role === "organizer" && (
        <div className="card form-card">
          <h2>Schedule a Race</h2>

          <form onSubmit={scheduleRace}>
            <input
              type="number"
              placeholder="Championship ID"
              value={championshipId}
              onChange={(e) => setChampionshipId(e.target.value)}
              required
            />

            <input
              type="text"
              placeholder="Race name"
              value={raceName}
              onChange={(e) => setRaceName(e.target.value)}
              required
            />

            <input
              type="date"
              value={raceDate}
              onChange={(e) => setRaceDate(e.target.value)}
              required
            />

            <button className="primary-button">
              Schedule Race
            </button>
          </form>

          {message && <p>{message}</p>}
        </div>
      )}

      <div className="card">
        <h2>Scheduled Races</h2>
        <p>
          Race listings will appear here once the GET races
          backend endpoint is connected.
        </p>
      </div>
    </DashboardLayout>
  );
}

export default Races;
