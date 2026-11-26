
import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import "./App.css";

function Home() {
  return (
    <div className="home-page">
      <h1>F1 CHAMPIONSHIP MANAGER</h1>
      <p>Select a dashboard to continue</p>

      <div className="role-container">
        <Link to="/admin" className="role-card">
          <h2>Admin</h2>
          <p>Manage teams and organizers</p>
        </Link>

        <Link to="/organizer" className="role-card">
          <h2>Organizer</h2>
          <p>Manage championships and races</p>
        </Link>

        <Link to="/driver" className="role-card">
          <h2>Driver</h2>
          <p>View teams and performance</p>
        </Link>
      </div>
    </div>
  );
}

function AdminDashboard() {
  return <h1>Admin Dashboard</h1>;
}

function OrganizerDashboard() {
  return <h1>Organizer Dashboard</h1>;
}

function DriverDashboard() {
  return <h1>Driver Dashboard</h1>;
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/admin" element={<AdminDashboard />} />
        <Route path="/organizer" element={<OrganizerDashboard />} />
        <Route path="/driver" element={<DriverDashboard />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
