
import DashboardLayout from "../../components/DashboardLayout";
import StatCard from "../../components/StatCard";

function OrganizerDashboard() {
  return (
    <DashboardLayout role="organizer">
      <div className="page-header">
        <div>
          <h1>Organizer Dashboard</h1>
          <p>Manage championships and racing events</p>
        </div>
      </div>

      <div className="stats-grid">
        <StatCard
          title="Championships"
          value="—"
          description="Created by you"
        />

        <StatCard
          title="Scheduled Races"
          value="—"
          description="Upcoming events"
        />

        <StatCard
          title="Race Results"
          value="—"
          description="Published results"
        />

        <StatCard
          title="Your Role"
          value="Organizer"
          description="Championship management"
        />
      </div>

      <div className="card">
        <h2>Welcome to Race Control</h2>
        <p>
          Manage your championships, schedule racing events
          and publish race results from the navigation menu.
        </p>
      </div>
    </DashboardLayout>
  );
}

export default OrganizerDashboard;
