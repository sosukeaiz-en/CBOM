const mongoose = require("mongoose");

const scanSchema = new mongoose.Schema(
  {
    name: {
      type: String,
      required: true,
      trim: true,
    },
    originalFileName: {
      type: String,
      required: true,
    },
    zipSize: {
      type: Number,
      default: 0,
    },
    status: {
      type: String,
      enum: ["pending", "uploading", "extracted", "scanning", "completed", "failed"],
      default: "pending",
    },
    extractedPath: {
      type: String,
      default: "",
    },
    totalFiles: {
      type: Number,
      default: 0,
    },
    supportedFiles: {
      type: [String],
      default: [],
    },
    errorMessage: {
      type: String,
      default: null,
    },
  },
  {
    timestamps: true,
  }
);

module.exports = mongoose.model("Scan", scanSchema);
