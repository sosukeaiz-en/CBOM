// QuantumShield Backend -- Entry Point
require("dotenv").config();

const express = require("express");
const connectDB = require("./config/db");
const healthRouter = require("./routes/health");

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(express.json());

// Routes
app.use("/api/health", healthRouter);

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
