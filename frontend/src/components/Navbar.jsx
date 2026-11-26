
function Navbar({ username, role }) {
  return (
    <header className="navbar">
      <div>
        <p className="navbar-label">F1 CHAMPIONSHIP MANAGER</p>
        <h3>Welcome, {username || "Racer"}</h3>
      </div>

      <div className="navbar-user">
        <div className="user-avatar">
          {(username || "U").charAt(0).toUpperCase()}
        </div>

        <div>
          <strong>{username || "User"}</strong>
          <p>{role}</p>
        </div>
      </div>
    </header>
  );
}

export default Navbar;
