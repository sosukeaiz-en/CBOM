const mongoose = require("mongoose");

const riskAssessmentSchema = new mongoose.Schema(
    {
        assetId: {
            type: mongoose.Schema.Types.ObjectId,
            ref: "CryptoAsset",
            required: true
        },

        quantumVulnerable: {
            type: Boolean,
            default: false
        },

        quantumImpact: {
            type: String,
            enum: ["SHOR", "GROVER", "CLASSICAL", "NONE", "UNKNOWN"],
            default: "UNKNOWN"
        },

        businessCriticality: {
            type: String,
            enum: ["LOW", "MEDIUM", "HIGH", "CRITICAL"],
            default: "MEDIUM"
        },

        dataLifetimeYears: {
            type: Number,
            min: 0,
            default: null
        },

        migrationTimeYears: {
            type: Number,
            min: 0,
            default: null
        },

        crqcHorizonYears: {
            type: Number,
            min: 0,
            default: 10
        },

        requiredProtectionWindowYears: {
            type: Number,
            min: 0,
            default: null
        },

        moscaTriggered: {
            type: Boolean,
            default: false
        },

        riskFactors: {
            quantumVulnerability: {
                score: {
                    type: Number,
                    min: 0,
                    max: 100,
                    default: 0
                },
                weight: {
                    type: Number,
                    min: 0,
                    max: 100,
                    default: 30
                }
            },

            businessCriticality: {
                score: {
                    type: Number,
                    min: 0,
                    max: 100,
                    default: 0
                },
                weight: {
                    type: Number,
                    min: 0,
                    max: 100,
                    default: 20
                }
            },

            dataLifetime: {
                score: {
                    type: Number,
                    min: 0,
                    max: 100,
                    default: 0
                },
                weight: {
                    type: Number,
                    min: 0,
                    max: 100,
                    default: 20
                }
            },

            migrationDifficulty: {
                score: {
                    type: Number,
                    min: 0,
                    max: 100,
                    default: 0
                },
                weight: {
                    type: Number,
                    min: 0,
                    max: 100,
                    default: 15
                }
            },

            exposure: {
                score: {
                    type: Number,
                    min: 0,
                    max: 100,
                    default: 0
                },
                weight: {
                    type: Number,
                    min: 0,
                    max: 100,
                    default: 10
                }
            },

            detectionConfidence: {
                score: {
                    type: Number,
                    min: 0,
                    max: 100,
                    default: 0
                },
                weight: {
                    type: Number,
                    min: 0,
                    max: 100,
                    default: 5
                }
            }
        },

        riskScore: {
            type: Number,
            min: 0,
            max: 100,
            default: null
        },

        riskLevel: {
            type: String,
            enum: ["LOW", "MEDIUM", "HIGH", "CRITICAL"],
            default: null
        },

        explanation: {
            type: String,
            default: null,
            trim: true
        },

        assessmentVersion: {
            type: String,
            default: "1.0",
            trim: true
        },

        assessedAt: {
            type: Date,
            default: Date.now
        }
    },
    {
        timestamps: true
    }
);

const RiskAssessment = mongoose.model(
    "RiskAssessment",
    riskAssessmentSchema
);

module.exports = RiskAssessment;