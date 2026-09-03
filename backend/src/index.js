// QuantumShield Backend -- Entry Point
require("dotenv").config();

const express = require("express");
const cors = require("cors");
const connectDB = require("./config/db");
const healthRouter = require("./routes/health");
const scanRouter = require("./routes/scanRoutes");

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors());
app.use(express.json());

// Routes
app.use("/api/health", healthRouter);
app.use("/api/scans", scanRouter);

// Root route
app.get("/", (req, res) => {
  res.json({ message: "QuantumShield API is running." });
});

// Connect to database then start the server
connectDB()
  .then(() => {
    app.listen(PORT, () => {
      console.log(`Server running on http://localhost:${PORT}`);
    });
  })
  .catch((err) => {
    console.error("Database connection failed:", err.message);
    process.exit(1);
  });
