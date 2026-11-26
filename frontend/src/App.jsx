=
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";

import Login from "./pages/Login";
import Register from "./pages/Register";

import AdminDashboard from "./pages/admin/AdminDashboard";
import OrganizerDashboard from "./pages/organizer/OrganizerDashboard";
import DriverDashboard from "./pages/driver/DriverDashboard";

import Teams from "./pages/Teams";
import Championships from "./pages/Championships";
import Standings from "./pages/Standings";
import Races from "./pages/Races";
import Profile from "./pages/Profile";

import "./App.css";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to="/login" />} />

        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        <Route path="/admin" element={<AdminDashboard />} />
        <Route path="/organizer" element={<OrganizerDashboard />} />
        <Route path="/driver" element={<DriverDashboard />} />

        <Route path="/teams" element={<Teams />} />
        <Route path="/championships" element={<Championships />} />
        <Route path="/standings" element={<Standings />} />
        <Route path="/races" element={<Races />} />
        <Route path="/profile" element={<Profile />} />

        <Route path="*" element={<Navigate to="/login" />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
