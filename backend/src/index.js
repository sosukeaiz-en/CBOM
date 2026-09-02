// QuantumShield Backend — Express Server
const express = require("express");

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(express.json());

// Root route
app.get("/", (req, res) => {
  res.json({ message: "QuantumShield API is running 🚀" });
});

// Start server
app.listen(PORT, () => {
  console.log(`✅ Server running on http://localhost:${PORT}`);
});
