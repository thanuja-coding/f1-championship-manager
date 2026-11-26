
import { useState } from "react";
import DashboardLayout from "../components/DashboardLayout";
import { apiRequest, getToken } from "../services/api";

function Championships() {
  const role = localStorage.getItem("role");
  const [name, setName] = useState("");
  const [message, setMessage] = useState("");

  async function createChampionship(e) {
    e.preventDefault();

    try {
      await apiRequest(
        "/championships",
        "POST",
        { championship_name: name },
        getToken()
      );

      setMessage("Championship created successfully!");
      setName("");
    } catch (err) {
      setMessage(err.message);
    }
  }

  return (
    <DashboardLayout role={role}>
      <div className="page-header">
        <div>
          <h1>Championships</h1>
          <p>Explore and manage racing championships</p>
        </div>
      </div>

      {role === "organizer" && (
        <div className="card form-card">
          <h2>Create Championship</h2>

          <form onSubmit={createChampionship}>
            <input
              type="text"
              placeholder="Championship name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
            />

            <button className="primary-button">
              Create Championship
            </button>
          </form>

          {message && <p>{message}</p>}
        </div>
      )}

      <div className="card">
        <h2>Available Championships</h2>
        <p>
          Championship listing will appear here once the
          GET /championships backend route is available.
        </p>
      </div>
    </DashboardLayout>
  );
}

export default Championships;
