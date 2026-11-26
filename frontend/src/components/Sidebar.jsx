
import { NavLink, useNavigate } from "react-router-dom";
import { logout } from "../services/api";

function Sidebar({ role }) {
  const navigate = useNavigate();

  const menus = {
    admin: [
      { name: "Dashboard", path: "/admin" },
      { name: "Teams", path: "/teams" },
      { name: "Championships", path: "/championships" }
    ],
    organizer: [
      { name: "Dashboard", path: "/organizer" },
      { name: "Championships", path: "/championships" },
      { name: "Races", path: "/races" },
      { name: "Standings", path: "/standings" }
    ],
    driver: [
      { name: "Dashboard", path: "/driver" },
      { name: "Teams", path: "/teams" },
      { name: "Championships", path: "/championships" },
      { name: "Standings", path: "/standings" },
      { name: "Profile", path: "/profile" }
    ]
  };

  function handleLogout() {
    logout();
    navigate("/login");
  }

  return (
    <aside className="sidebar">
      <div className="sidebar-logo">
        <h2>F1<span> MANAGER</span></h2>
        <p>CHAMPIONSHIP CONTROL</p>
      </div>

      <p className="menu-title">MAIN MENU</p>

      <nav className="sidebar-menu">
        {(menus[role] || []).map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            end
            className={({ isActive }) =>
              isActive ? "nav-link active" : "nav-link"
            }
          >
            {item.name}
          </NavLink>
        ))}
      </nav>

      <button className="logout-button" onClick={handleLogout}>
        Logout
      </button>
    </aside>
  );
}

export default Sidebar;
