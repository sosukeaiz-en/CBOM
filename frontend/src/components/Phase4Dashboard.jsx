import React, { useEffect, useState } from "react";

const API_URL = "http://localhost:5000";

function RiskCard({ title, value, description }) {
  return (
    <div className="bg-gray-800 border border-gray-700 rounded-lg p-5">
      <p className="text-xs text-gray-400 uppercase tracking-widest">
        {title}
      </p>

      <p className="text-3xl font-bold text-white mt-2">
        {value}
      </p>

      {description && (
        <p className="text-xs text-gray-500 mt-2">
          {description}
        </p>
      )}
    </div>
  );
}

function RiskBadge({ risk }) {
  const styles = {
    CRITICAL: "bg-red-900 text-red-300",
    HIGH: "bg-orange-900 text-orange-300",
    MEDIUM: "bg-yellow-900 text-yellow-300",
    LOW: "bg-green-900 text-green-300",
    UNKNOWN: "bg-gray-700 text-gray-300",
  };

  return (
    <span
      className={`inline-flex px-2.5 py-1 rounded-full text-xs font-medium ${
        styles[risk] || styles.UNKNOWN
      }`}
    >
      {risk}
    </span>
  );
}

function Phase4Dashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function loadRiskData() {
      try {
        setLoading(true);
        setError(null);

        const response = await fetch(
          `${API_URL}/api/phase4/analyze-batch`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              assets: [
                {
                  algorithm: "RSA-2048",
                  dataLifetime: 10,
                  migrationTime: 5,
                  quantumThreatTime: 15,
                  businessCriticality: "CRITICAL",
                },
                {
                  algorithm: "ECDSA",
                  dataLifetime: 8,
                  migrationTime: 4,
                  quantumThreatTime: 15,
                  businessCriticality: "HIGH",
                },
                {
                  algorithm: "AES-128",
                  dataLifetime: 5,
                  migrationTime: 2,
                  quantumThreatTime: 15,
                  businessCriticality: "MEDIUM",
                },
                {
                  algorithm: "AES-256",
                  dataLifetime: 5,
                  migrationTime: 2,
                  quantumThreatTime: 15,
                  businessCriticality: "LOW",
                },
                {
                  algorithm: "SHA-256",
                  dataLifetime: 5,
                  migrationTime: 1,
                  quantumThreatTime: 15,
                  businessCriticality: "LOW",
                },
              ],
            }),
          }
        );

        if (!response.ok) {
          throw new Error(
            `API request failed: ${response.status}`
          );
        }

        const result = await response.json();

        if (!result.success) {
          throw new Error(
            result.error || "Phase 4 analysis failed"
          );
        }

        setData(result);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }

    loadRiskData();
  }, []);

  if (loading) {
    return (
      <section className="mt-10">
        <div className="bg-gray-800 border border-gray-700 rounded-lg p-8">
          <p className="text-gray-400">
            Loading Phase 4 quantum risk analysis...
          </p>
        </div>
      </section>
    );
  }

  if (error) {
    return (
      <section className="mt-10">
        <div className="bg-red-950 border border-red-800 rounded-lg p-6">
          <h3 className="text-sm font-semibold text-red-300">
            Phase 4 API Error
          </h3>

          <p className="text-sm text-red-400 mt-2">
            {error}
          </p>

          <p className="text-xs text-gray-500 mt-3">
            Make sure the backend is running on port 5000.
          </p>
        </div>
      </section>
    );
  }

  const summary = data?.summary;
  const results = data?.results || [];

  return (
    <section className="mt-10">

      {/* Header */}
      <div className="mb-6">
        <h2 className="text-2xl font-semibold text-white">
          Quantum Risk Assessment
        </h2>

        <p className="text-gray-400 mt-1 text-sm">
          Phase 4 cryptographic risk analysis
        </p>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">

        <RiskCard
          title="Total Assets"
          value={summary?.totalAssets ?? 0}
          description="Cryptographic assets analyzed"
        />

        <RiskCard
          title="Critical"
          value={summary?.riskCounts?.CRITICAL ?? 0}
          description="Immediate attention required"
        />

        <RiskCard
          title="Medium"
          value={summary?.riskCounts?.MEDIUM ?? 0}
          description="Migration should be planned"
        />

        <RiskCard
          title="Low"
          value={summary?.riskCounts?.LOW ?? 0}
          description="Continue monitoring"
        />

      </div>

      {/* Quantum Summary */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mt-4">

        <RiskCard
          title="Quantum Vulnerable"
          value={summary?.quantumVulnerable ?? 0}
          description="Assets vulnerable to quantum attacks"
        />

        <RiskCard
          title="Immediate Migration"
          value={
            summary?.migrationPriorities?.IMMEDIATE ?? 0
          }
          description="Assets requiring immediate migration"
        />

      </div>

      {/* Asset Table */}
      <div className="bg-gray-800 border border-gray-700 rounded-lg mt-8 overflow-hidden">

        <div className="px-6 py-5 border-b border-gray-700">

          <h3 className="text-sm font-medium text-gray-300">
            Cryptographic Assets
          </h3>

          <p className="text-xs text-gray-500 mt-1">
            Phase 4 risk assessment results
          </p>

        </div>

        <div className="overflow-x-auto">

          <table className="w-full text-left">

            <thead className="bg-gray-900">

              <tr>

                <th className="px-6 py-3 text-xs text-gray-400 uppercase">
                  Algorithm
                </th>

                <th className="px-6 py-3 text-xs text-gray-400 uppercase">
                  Quantum Risk
                </th>

                <th className="px-6 py-3 text-xs text-gray-400 uppercase">
                  Mosca Risk
                </th>

                <th className="px-6 py-3 text-xs text-gray-400 uppercase">
                  Migration
                </th>

                <th className="px-6 py-3 text-xs text-gray-400 uppercase">
                  Recommendation
                </th>

              </tr>

            </thead>

            <tbody>

              {results.map((item, index) => (

                <tr
                  key={`${item.asset?.algorithm}-${index}`}
                  className="border-t border-gray-700"
                >

                  <td className="px-6 py-4 text-sm text-white font-medium">
                    {item.asset?.algorithm || "Unknown"}
                  </td>

                  <td className="px-6 py-4">

                    <RiskBadge
                      risk={
                        item.quantumAssessment?.risk ||
                        "UNKNOWN"
                      }
                    />

                  </td>

                  <td className="px-6 py-4">

                    <RiskBadge
                      risk={
                        item.moscaAssessment?.risk ||
                        "UNKNOWN"
                      }
                    />

                  </td>

                  <td className="px-6 py-4 text-sm text-gray-300">

                    {item.moscaAssessment
                      ?.migrationPriority || "N/A"}

                  </td>

                  <td className="px-6 py-4">

                    <div className="text-sm text-white">

                      {item.recommendation?.replacement ||
                        "N/A"}

                    </div>

                    <div className="text-xs text-gray-500 mt-1">

                      {item.recommendation?.category || ""}

                    </div>

                  </td>

                </tr>

              ))}

              {results.length === 0 && (

                <tr>

                  <td
                    colSpan="5"
                    className="px-6 py-8 text-center text-sm text-gray-500"
                  >
                    No cryptographic assets found.
                  </td>

                </tr>

              )}

            </tbody>

          </table>

        </div>

      </div>

    </section>
  );
}

export default Phase4Dashboard;