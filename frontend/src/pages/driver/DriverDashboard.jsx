
import DashboardLayout from "../../components/DashboardLayout";
import StatCard from "../../components/StatCard";

function DriverDashboard() {
  return (
    <DashboardLayout role="driver">
      <div className="page-header">
        <div>
          <h1>Driver Dashboard</h1>
          <p>Your racing career starts here</p>
        </div>
      </div>

      <div className="stats-grid">
        <StatCard
          title="Championship Points"
          value="—"
          description="Your total points"
        />

        <StatCard
          title="Race Wins"
          value="—"
          description="First place finishes"
        />

        <StatCard
          title="Podiums"
          value="—"
          description="Top three finishes"
        />

        <StatCard
          title="Your Role"
          value="Driver"
          description="Registered racer"
        />
      </div>

      <div className="card">
        <h2>Welcome to the Championship</h2>
        <p>
          Explore racing teams, apply to join a team
          and track your performance.
        </p>
      </div>
    </DashboardLayout>
  );
}

export default DriverDashboard;
