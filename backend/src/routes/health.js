// Health check route
const express = require("express");
const mongoose = require("mongoose");

const router = express.Router();

// Mongoose readyState: 0=disconnected, 1=connected, 2=connecting, 3=disconnecting
const DB_STATES = {
  0: "disconnected",
  1: "connected",
  2: "connecting",
  3: "disconnecting",
};

router.get("/", (req, res) => {
  const dbState = mongoose.connection.readyState;

  res.status(200).json({
    status: "ok",
    timestamp: new Date().toISOString(),
    database: DB_STATES[dbState] || "unknown",
  });
});

module.exports = router;
