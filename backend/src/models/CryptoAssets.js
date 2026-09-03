const mongoose = require("mongoose");

const cryptoAssetSchema = new mongoose.Schema(
    {
        scanId: {
            type: mongoose.Schema.Types.ObjectId,
            ref: "Scan",
            required: true
        },

        artifact: {
            type: String,
            required: true,
            trim: true
        },

        artifactType: {
            type: String,
            enum: [
                "SOURCE_CODE",
                "BINARY",
                "LIBRARY",
                "DEPENDENCY",
                "CONTAINER",
                "CERTIFICATE",
                "CONFIGURATION",
                "KEY_MATERIAL",
                "PROTOCOL"
            ],
            required: true
        },

        file: {
            type: String,
            default: null,
            trim: true
        },

        line: {
            type: Number,
            default: null,
            min: 1
        },

        algorithm: {
            type: String,
            required: true,
            trim: true
        },

        version: {
            type: String,
            default: null,
            trim: true
        },

        mode: {
            type: String,
            default: null,
            trim: true
        },

        purpose: {
            type: String,
            enum: [
                "ENCRYPTION",
                "KEY_ESTABLISHMENT",
                "DIGITAL_SIGNATURE",
                "HASHING",
                "AUTHENTICATION",
                "KEY_DERIVATION",
                "MAC",
                "PROTOCOL",
                "UNKNOWN"
            ],
            default: "UNKNOWN"
        },

        keySize: {
            type: Number,
            default: null,
            min: 1
        },

        library: {
            type: String,
            default: null,
            trim: true
        },

        libraryVersion: {
            type: String,
            default: null,
            trim: true
        },

        confidence: {
            type: String,
            enum: ["HIGH", "MEDIUM", "LOW"],
            default: "MEDIUM"
        },

        businessCriticality: {
            type: String,
            enum: ["LOW", "MEDIUM", "HIGH", "CRITICAL"],
            default: "MEDIUM"
        },

        dataLifetimeYears: {
            type: Number,
            default: null,
            min: 0
        },

        migrationTimeYears: {
            type: Number,
            default: null,
            min: 0
        },

        quantumVulnerability: {
            type: String,
            enum: ["VULNERABLE", "REDUCED_MARGIN", "RESISTANT", "UNKNOWN"],
            default: "UNKNOWN"
        },

        riskScore: {
            type: Number,
            default: null,
            min: 0,
            max: 100
        },

        riskLevel: {
            type: String,
            enum: ["LOW", "MEDIUM", "HIGH", "CRITICAL"],
            default: null
        },

        recommendation: {
            type: String,
            default: null,
            trim: true
        },

        recommendationType: {
            type: String,
            enum: ["PQC", "HYBRID", "REPLACE", "MONITOR", "NONE"],
            default: null
        },

        migrationPriority: {
            type: String,
            enum: ["IMMEDIATE", "HIGH", "PLANNED", "MONITOR"],
            default: null
        },

        status: {
            type: String,
            enum: [
                "DISCOVERED",
                "ASSESSMENT_PENDING",
                "MIGRATION_REQUIRED",
                "MIGRATION_PLANNED",
                "IN_PROGRESS",
                "COMPLETED",
                "MONITOR"
            ],
            default: "DISCOVERED"
        }
    },
    {
        timestamps: true
    }
);

const CryptoAsset = mongoose.model("CryptoAsset", cryptoAssetSchema);

module.exports = CryptoAsset;