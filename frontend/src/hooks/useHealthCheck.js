import { useState, useEffect } from "react";

function useHealthCheck() {
  const [status, setStatus] = useState("loading");
  const [timestamp, setTimestamp] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    let cancelled = false;

    async function fetchHealth() {
      try {
        const response = await fetch("/api/health");
        if (!response.ok) {
          throw new Error(`HTTP ${response.status}`);
        }
        const data = await response.json();
        if (!cancelled) {
          setStatus(data.status);
          setTimestamp(data.timestamp);
          setError(null);
        }
      } catch (err) {
        if (!cancelled) {
          setStatus("error");
          setError(err.message);
        }
      }
    }

    fetchHealth();

    return () => {
      cancelled = true;
    };
  }, []);

  return { status, timestamp, error };
}

export default useHealthCheck;
