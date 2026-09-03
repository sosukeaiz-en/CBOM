const express = require("express");

const {
  analyzeCryptoAsset,
} = require("../phase4/phase4Analyzer");

const {
  generateRiskSummary,
} = require("../phase4/riskSummary");

const router = express.Router();

/**
 * POST /api/phase4/analyze
 *
 * Analyze a single cryptographic asset.
 */
router.post("/analyze", (req, res) => {
  try {
    const {
      algorithm,
      dataLifetime = 0,
      migrationTime = 0,
      quantumThreatTime = 15,
      businessCriticality = "UNKNOWN",
    } = req.body;

    // Algorithm is required
    if (!algorithm) {
      return res.status(400).json({
        success: false,
        error: "algorithm is required",
      });
    }

    const result = analyzeCryptoAsset({
      algorithm,
      dataLifetime: Number(dataLifetime),
      migrationTime: Number(migrationTime),
      quantumThreatTime: Number(quantumThreatTime),
      businessCriticality,
    });

    return res.status(200).json({
      success: true,
      result,
    });
  } catch (error) {
    console.error("Phase 4 analysis error:", error);

    return res.status(500).json({
      success: false,
      error: error.message,
    });
  }
});


/**
 * POST /api/phase4/analyze-batch
 *
 * Analyze multiple cryptographic assets.
 */
router.post("/analyze-batch", (req, res) => {
  try {
    const { assets } = req.body;

    // Validate assets
    if (!Array.isArray(assets)) {
      return res.status(400).json({
        success: false,
        error: "assets must be an array",
      });
    }

    if (assets.length === 0) {
      return res.status(400).json({
        success: false,
        error: "assets array cannot be empty",
      });
    }

    // Analyze every asset
    const results = assets.map((asset) => {
      return analyzeCryptoAsset({
        algorithm: asset.algorithm,
        dataLifetime: Number(asset.dataLifetime || 0),
        migrationTime: Number(asset.migrationTime || 0),
        quantumThreatTime: Number(
          asset.quantumThreatTime || 15
        ),
        businessCriticality:
          asset.businessCriticality || "UNKNOWN",
      });
    });

    // Generate aggregate risk summary
    const summary = generateRiskSummary(results);

    return res.status(200).json({
      success: true,
      count: results.length,
      summary,
      results,
    });
  } catch (error) {
    console.error("Phase 4 batch analysis error:", error);

    return res.status(500).json({
      success: false,
      error: error.message,
    });
  }
});


module.exports = router;