import React, { useState, useEffect } from "react";
import useHealthCheck from "./hooks/useHealthCheck";
import ZipUploader from "./components/ZipUploader";
import ScanList from "./components/ScanList";

function Header() {
  return (
    <header className="bg-gray-900 border-b border-gray-700 px-6 py-4">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-indigo-600 flex items-center justify-center font-bold text-white shadow-lg shadow-indigo-600/30">
            Q
          </div>
          <div>
            <h1 className="text-xl font-semibold text-white tracking-wide">
              QuantumShield
            </h1>
            <p className="text-xs text-gray-400">
              CBOM Cryptographic Bill of Materials & Risk Scanner
            </p>
          </div>
        </div>
        <nav className="flex items-center gap-6">
          <a href="#" className="text-sm text-white font-medium border-b-2 border-indigo-500 pb-0.5">
            Dashboard
          </a>
          <a href="#" className="text-sm text-gray-400 hover:text-white transition-colors">
            Scans
          </a>
          <a href="#" className="text-sm text-gray-400 hover:text-white transition-colors">
            PQC Advisor
          </a>
        </nav>
      </div>
    </header>
  );
}

function StatusBadge({ status }) {
  const variants = {
    ok: "bg-green-900/60 text-green-300 border border-green-700/50",
    error: "bg-red-900/60 text-red-300 border border-red-700/50",
    loading: "bg-gray-700 text-gray-400",
    pending: "bg-yellow-900/60 text-yellow-300 border border-yellow-700/50",
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

  return (
    <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium ${variants[status] || variants.pending}`}>
      <span className={`w-1.5 h-1.5 rounded-full ${dotVariants[status] || dotVariants.pending}`} />
      {labels[status] || "Unknown"}
    </span>
  );
}

function MainContent() {
  const { status, database, timestamp, error } = useHealthCheck();
  const [scans, setScans] = useState([]);
  const [isLoadingScans, setIsLoadingScans] = useState(true);

  const fetchScans = async () => {
    try {
      setIsLoadingScans(true);
      const response = await fetch("http://localhost:5000/api/scans");
      if (response.ok) {
        const data = await response.json();
        setScans(data.scans || []);
      }
    } catch (err) {
      console.error("Failed to fetch scans:", err);
    } finally {
      setIsLoadingScans(false);
    }
  };

  useEffect(() => {
    fetchScans();
  }, []);

  const handleScanCreated = (newScan) => {
    setScans((prev) => [newScan, ...prev]);
  };

  const handleDeleteScan = async (scanId) => {
    try {
      const res = await fetch(`http://localhost:5000/api/scans/${scanId}`, {
        method: "DELETE",
      });
      if (res.ok) {
        setScans((prev) => prev.filter((s) => s._id !== scanId));
      }
    } catch (err) {
      console.error("Failed to delete scan:", err);
    }
  };

  return (
    <main className="flex-1 max-w-7xl mx-auto w-full px-6 py-10">
      <div className="mb-8">
        <h2 className="text-2xl font-semibold text-white">Cryptographic Inventory Dashboard</h2>
        <p className="text-gray-400 mt-1 text-sm">
          Phase 3 — Source Code Scan & Upload Pipeline
        </p>
      </div>

      {/* Overview Metric Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-8">
        <div className="bg-gray-800 border border-gray-700 rounded-xl p-5 shadow-lg">
          <p className="text-xs text-gray-400 uppercase tracking-widest mb-2 font-medium">
            API Health
          </p>
          <StatusBadge status={status} />
          {timestamp && (
            <p className="text-xs text-gray-500 mt-2">
              Checked: {new Date(timestamp).toLocaleTimeString()}
            </p>
          )}
          {error && <p className="text-xs text-red-400 mt-1">Error: {error}</p>}
        </div>

        <div className="bg-gray-800 border border-gray-700 rounded-xl p-5 shadow-lg">
          <p className="text-xs text-gray-400 uppercase tracking-widest mb-2 font-medium">
            Database Status
          </p>
          <StatusBadge status={database === "connected" ? "ok" : database === "loading" ? "loading" : "error"} />
          <p className="text-xs text-gray-500 mt-2 capitalize">{database}</p>
        </div>

        <div className="bg-gray-800 border border-gray-700 rounded-xl p-5 shadow-lg">
          <p className="text-xs text-gray-400 uppercase tracking-widest mb-1 font-medium">
            Total Scanned Repositories
          </p>
          <p className="text-2xl font-bold text-white mt-1">{scans.length}</p>
        </div>
      </div>

      {/* Zip Upload Area */}
      <ZipUploader onScanCreated={handleScanCreated} />

      {/* Scans List Table */}
      <ScanList scans={scans} onDeleteScan={handleDeleteScan} isLoading={isLoadingScans} />
    </main>
  );
}

function Footer() {
  return (
    <footer className="border-t border-gray-800 px-6 py-4 mt-auto">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        <p className="text-xs text-gray-500">
          QuantumShield &copy; {new Date().getFullYear()} &mdash; Post-Quantum CBOM Scanner
        </p>
        <p className="text-xs text-gray-600">Phase 3 — Scan & Upload System</p>
      </div>
    </footer>
  );
}

export default function App() {
  return (
    <div className="min-h-screen bg-gray-950 text-white flex flex-col font-sans">
      <Header />
      <MainContent />
      <Footer />
    </div>
  );
}
