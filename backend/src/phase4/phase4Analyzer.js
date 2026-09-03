// Phase 4 - Combined Quantum Risk Analyzer
//
// Combines:
// 1. Quantum cryptographic risk
// 2. Mosca migration timeline assessment
// 3. PQC / Hybrid recommendations

const {
  assessQuantumRisk,
} = require("./quantumRisk");

const {
  getRecommendation,
} = require("./recommendations");

const {
  assessWithDefaultQuantumTimeline,
} = require("./mosca");


/**
 * Perform a complete Phase 4 analysis of a cryptographic asset.
 *
 * @param {Object} asset
 * @param {string} asset.algorithm - Cryptographic algorithm
 * @param {number} asset.dataLifetime - Required data protection lifetime in years
 * @param {number} asset.migrationTime - Estimated migration time in years
 * @param {number} asset.quantumThreatTime - Estimated years until CRQC
 * @param {string} asset.businessCriticality - Business importance
 *
 * @returns {Object} Complete Phase 4 analysis
 */
function analyzeCryptoAsset({
  algorithm,
  dataLifetime = 0,
  migrationTime = 0,
  quantumThreatTime = 15,
  businessCriticality = "UNKNOWN",
}) {
  // 1. Assess quantum vulnerability
  const quantumRisk = assessQuantumRisk(algorithm);

  // 2. Calculate Mosca risk
  const moscaRisk = assessWithDefaultQuantumTimeline({
    dataLifetime,
    migrationTime,
    quantumThreatTime,
  });

  // 3. Get PQC recommendation
  const recommendation = getRecommendation(algorithm);

  // 4. Calculate overall risk
  const overallRisk = calculateOverallRisk({
    quantumRisk,
    moscaRisk,
    businessCriticality,
  });

  // 5. Return complete Phase 4 result
  return {
    phase: 4,

    asset: {
      algorithm,
      businessCriticality,
    },

    quantumAssessment: {
      quantumVulnerable: quantumRisk.quantumVulnerable,
      risk: quantumRisk.risk,
      attack: quantumRisk.attack,
      reason: quantumRisk.reason,
    },

    moscaAssessment: {
      dataLifetime: moscaRisk.dataLifetime,
      migrationTime: moscaRisk.migrationTime,
      quantumThreatTime: moscaRisk.quantumThreatTime,
      protectionWindow: moscaRisk.protectionWindow,
      margin: moscaRisk.margin,
      risk: moscaRisk.risk,
      migrationPriority: moscaRisk.migrationPriority,
      conditionSatisfied: moscaRisk.conditionSatisfied,
      message: moscaRisk.message,
    },

    recommendation: {
      replacement: recommendation.replacement,
      hybrid: recommendation.hybrid,
      category: recommendation.category,
      priority: recommendation.priority,
      reason: recommendation.reason,
    },

    overallRisk,
  };
}


/**
 * Calculate the final overall risk.
 *
 * The most severe applicable risk is selected.
 */
function calculateOverallRisk({
  quantumRisk,
  moscaRisk,
  businessCriticality,
}) {
  const riskScores = {
    UNKNOWN: 0,
    LOW: 1,
    MEDIUM: 2,
    HIGH: 3,
    CRITICAL: 4,
  };

  const quantumScore = riskScores[quantumRisk.risk] || 0;
  const moscaScore = riskScores[moscaRisk.risk] || 0;

  let score = Math.max(quantumScore, moscaScore);

  // Increase priority for highly business-critical systems
  const criticality = String(businessCriticality).toUpperCase();

  if (criticality === "CRITICAL" && score < 4) {
    score += 1;
  }

  if (score > 4) {
    score = 4;
  }

  const riskByScore = {
    0: "UNKNOWN",
    1: "LOW",
    2: "MEDIUM",
    3: "HIGH",
    4: "CRITICAL",
  };

  return riskByScore[score];
}


module.exports = {
  analyzeCryptoAsset,
  calculateOverallRisk,
};