// QuantumShield Backend -- Entry Point

require("dotenv").config({
  path: require("path").resolve(__dirname, "../.env"),
});

const express = require("express");
const cors = require("cors");
const connectDB = require("./config/db");
const healthRouter = require("./routes/health");
const phase4Routes = require("./routes/phase4");

const app = express();
const PORT = process.env.PORT || 5000;

console.log("MONGO_URI loaded:", !!process.env.MONGO_URI);

app.use(cors());
app.use(express.json());

app.use("/api/health", healthRouter);
app.use("/api/phase4", phase4Routes);

app.get("/", (req, res) => {
  res.json({
    message: "QuantumShield API is running.",
  });
});

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