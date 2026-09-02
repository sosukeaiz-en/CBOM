import React from "react";
import useHealthCheck from "./hooks/useHealthCheck";

function Header() {
  return (
    <header className="bg-gray-900 border-b border-gray-700 px-6 py-4">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        <div>
          <h1 className="text-xl font-semibold text-white tracking-wide">
            QuantumShield
          </h1>
          <p className="text-xs text-gray-400 mt-0.5">
            Security Management Platform
          </p>
        </div>
        <nav className="flex items-center gap-6">
          <a
            href="#"
            className="text-sm text-gray-300 hover:text-white transition-colors"
          >
            Dashboard
          </a>
          <a
            href="#"
            className="text-sm text-gray-300 hover:text-white transition-colors"
          >
            Reports
          </a>
          <a
            href="#"
            className="text-sm text-gray-300 hover:text-white transition-colors"
          >
            Settings
          </a>
        </nav>
      </div>
    </header>
  );
}

function StatusBadge({ status }) {
  const variants = {
    ok: "bg-green-900 text-green-300",
    error: "bg-red-900 text-red-300",
    loading: "bg-gray-700 text-gray-400",
    pending: "bg-yellow-900 text-yellow-300",
  };

  const dotVariants = {
    ok: "bg-green-400",
    error: "bg-red-400",
    loading: "bg-gray-400 animate-pulse",
    pending: "bg-yellow-400",
  };

  const labels = {
    ok: "Operational",
    error: "Unreachable",
    loading: "Checking...",
    pending: "Pending",
  };

  const variant = variants[status] || variants.pending;
  const dot = dotVariants[status] || dotVariants.pending;
  const label = labels[status] || "Unknown";

  return (
    <span
      className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium ${variant}`}
    >
      <span className={`w-1.5 h-1.5 rounded-full ${dot}`} />
      {label}
    </span>
  );
}

function ApiStatusCard({ status, timestamp, error }) {
  return (
    <div className="bg-gray-800 border border-gray-700 rounded-lg p-5">
      <p className="text-xs text-gray-400 uppercase tracking-widest mb-2">
        API Status
      </p>
      <StatusBadge status={status} />
      {timestamp && (
        <p className="text-xs text-gray-500 mt-2">
          Last checked:{" "}
          {new Date(timestamp).toLocaleTimeString()}
        </p>
      )}
      {error && (
        <p className="text-xs text-red-400 mt-2">Error: {error}</p>
      )}
    </div>
  );
}

function MainContent() {
  const { status, timestamp, error } = useHealthCheck();

  return (
    <main className="flex-1 max-w-7xl mx-auto w-full px-6 py-10">
      <div className="mb-8">
        <h2 className="text-2xl font-semibold text-white">Dashboard</h2>
        <p className="text-gray-400 mt-1 text-sm">
          System overview and status
        </p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-10">
        <ApiStatusCard status={status} timestamp={timestamp} error={error} />

        <div className="bg-gray-800 border border-gray-700 rounded-lg p-5">
          <p className="text-xs text-gray-400 uppercase tracking-widest mb-2">
            Database
          </p>
          <StatusBadge status="pending" />
        </div>

        <div className="bg-gray-800 border border-gray-700 rounded-lg p-5">
          <p className="text-xs text-gray-400 uppercase tracking-widest mb-1">
            Active Sessions
          </p>
          <p className="text-2xl font-bold text-white mt-1">--</p>
        </div>
      </div>

      <div className="bg-gray-800 border border-gray-700 rounded-lg p-6">
        <h3 className="text-sm font-medium text-gray-300 mb-4">
          Recent Activity
        </h3>
        <p className="text-sm text-gray-500 italic">
          No activity to display yet. Connect MongoDB in Step 11 to populate
          this section.
        </p>
      </div>
    </main>
  );
}

function Footer() {
  return (
    <footer className="border-t border-gray-700 px-6 py-4">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        <p className="text-xs text-gray-500">
          QuantumShield &copy; {new Date().getFullYear()}
        </p>
        <p className="text-xs text-gray-600">Phase 1 &mdash; Foundation</p>
      </div>
    </footer>
  );
}

function App() {
  return (
    <div className="min-h-screen bg-gray-950 text-white flex flex-col">
      <Header />
      <MainContent />
      <Footer />
    </div>
  );
}

export default App;
