const mongoose = require("mongoose");

const scanSchema = new mongoose.Schema(
    {
        projectName: {
            type: String,
            required: true,
            trim: true
        },

        originalFileName: {
            type: String,
            required: true,
            trim: true
        },

        artifactType: {
            type: String,
            enum: ["SOURCE_CODE", "LIBRARY", "BINARY", "CONTAINER"],
            default: "SOURCE_CODE"
        },

        status: {
            type: String,
            enum: ["PENDING", "SCANNING", "COMPLETED", "FAILED"],
            default: "PENDING"
        },

        startedAt: {
            type: Date,
            default: null
        },

        completedAt: {
            type: Date,
            default: null
        },

        assetsFound: {
            type: Number,
            default: 0,
            min: 0
        },

        criticalAssets: {
            type: Number,
            default: 0,
            min: 0
        },

        error: {
            type: String,
            default: null,
            trim: true
        }
    },
    {
        timestamps: true
    }
);

const Scan = mongoose.model("Scan", scanSchema);

module.exports = Scan;