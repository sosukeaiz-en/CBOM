// Phase 4 - Risk Summary
// Creates aggregate statistics from Phase 4 analysis results.

function generateRiskSummary(results) {
  if (!Array.isArray(results)) {
    throw new Error("results must be an array");
  }

  const summary = {
    totalAssets: results.length,

    riskCounts: {
      CRITICAL: 0,
      HIGH: 0,
      MEDIUM: 0,
      LOW: 0,
      UNKNOWN: 0,
    },

    quantumVulnerable: 0,

    migrationPriorities: {
      IMMEDIATE: 0,
      URGENT: 0,
      PLANNED: 0,
      MONITOR: 0,
    },

    algorithms: {},
  };

  results.forEach((result) => {
    const risk = result.overallRisk || "UNKNOWN";

    if (summary.riskCounts[risk] !== undefined) {
      summary.riskCounts[risk]++;
    } else {
      summary.riskCounts.UNKNOWN++;
    }

    if (
      result.quantumAssessment &&
      result.quantumAssessment.quantumVulnerable
    ) {
      summary.quantumVulnerable++;
    }

    if (result.moscaAssessment) {
      const priority =
        result.moscaAssessment.migrationPriority;

      if (summary.migrationPriorities[priority] !== undefined) {
        summary.migrationPriorities[priority]++;
      }
    }

    const algorithm =
      result.asset?.algorithm || "UNKNOWN";

    summary.algorithms[algorithm] =
      (summary.algorithms[algorithm] || 0) + 1;
  });

  return summary;
}

module.exports = {
  generateRiskSummary,
};