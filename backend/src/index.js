// QuantumShield Backend -- Entry Point
const express = require("express");

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

// Start server
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
