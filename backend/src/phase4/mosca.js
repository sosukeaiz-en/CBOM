// Phase 4 - Mosca's Theorem Risk Assessment
//
// Mosca's inequality:
//
//     X + Y >= Z
//
// X = lifetime of the data
// Y = time required to migrate the system
// Z = estimated time until a cryptographically relevant quantum computer
//
// If X + Y >= Z, migration should be treated as urgent.

const RISK_LEVELS = {
  CRITICAL: "CRITICAL",
  HIGH: "HIGH",
  MEDIUM: "MEDIUM",
  LOW: "LOW",
};


/**
 * Calculate Mosca's risk.
 *
 * @param {Object} input
 * @param {number} input.dataLifetime - How many years the data must remain protected
 * @param {number} input.migrationTime - Estimated migration time in years
 * @param {number} input.quantumThreatTime - Estimated years until CRQC
 * @returns {Object} Mosca risk assessment
 */
function assessMoscaRisk({
  dataLifetime,
  migrationTime,
  quantumThreatTime,
}) {
  // Validate input
  if (
    typeof dataLifetime !== "number" ||
    typeof migrationTime !== "number" ||
    typeof quantumThreatTime !== "number"
  ) {
    throw new Error(
      "dataLifetime, migrationTime and quantumThreatTime must be numbers."
    );
  }

  if (
    dataLifetime < 0 ||
    migrationTime < 0 ||
    quantumThreatTime < 0
  ) {
    throw new Error(
      "dataLifetime, migrationTime and quantumThreatTime cannot be negative."
    );
  }

  // X + Y
  const protectionWindow = dataLifetime + migrationTime;

  // Difference between required protection window and quantum threat
  const margin = quantumThreatTime - protectionWindow;

  let risk;
  let migrationPriority;
  let message;

  if (protectionWindow >= quantumThreatTime) {
    risk = RISK_LEVELS.CRITICAL;
    migrationPriority = "IMMEDIATE";
    message =
      "The protection window reaches or exceeds the estimated quantum threat timeline. Migration should begin immediately.";
  } else if (margin <= 3) {
    risk = RISK_LEVELS.HIGH;
    migrationPriority = "URGENT";
    message =
      "The estimated quantum threat is approaching the protection window. Migration planning should begin urgently.";
  } else if (margin <= 7) {
    risk = RISK_LEVELS.MEDIUM;
    migrationPriority = "PLANNED";
    message =
      "There is some remaining time before the estimated quantum threat. PQC migration should be planned.";
  } else {
    risk = RISK_LEVELS.LOW;
    migrationPriority = "MONITOR";
    message =
      "The estimated quantum threat is currently outside the protection window. Continue monitoring and prepare for migration.";
  }

  return {
    dataLifetime,
    migrationTime,
    quantumThreatTime,
    protectionWindow,
    margin,
    risk,
    migrationPriority,
    moscaCondition: `${dataLifetime} + ${migrationTime} >= ${quantumThreatTime}`,
    conditionSatisfied: protectionWindow >= quantumThreatTime,
    message,
  };
}


/**
 * Calculate the Mosca risk using a default quantum threat estimate.
 *
 * This is useful when a scan does not provide its own quantum timeline.
 *
 * Default: 15 years
 */
function assessWithDefaultQuantumTimeline({
  dataLifetime,
  migrationTime,
  quantumThreatTime = 15,
}) {
  return assessMoscaRisk({
    dataLifetime,
    migrationTime,
    quantumThreatTime,
  });
}


module.exports = {
  assessMoscaRisk,
  assessWithDefaultQuantumTimeline,
  RISK_LEVELS,
};