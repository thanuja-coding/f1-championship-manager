
import Sidebar from "./Sidebar";
import Navbar from "./Navbar";

function DashboardLayout({ role, children }) {
  const username = localStorage.getItem("username");

  return (
    <div className="app-layout">
      <Sidebar role={role} />

      <main className="main-content">
        <Navbar username={username} role={role} />
        {children}
      </main>
    </div>
  );
}

export default DashboardLayout;
