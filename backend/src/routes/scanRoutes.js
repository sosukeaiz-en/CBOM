const express = require("express");
const router = express.Router();
const upload = require("../middleware/uploadMiddleware");
const scanController = require("../controllers/scanController");

// POST /api/scans/upload - Upload source code ZIP
router.post("/upload", upload.single("zipFile"), scanController.createScan);

// GET /api/scans - List all scans
router.get("/", scanController.getScans);

// GET /api/scans/:id - Get scan status/details
router.get("/:id", scanController.getScanById);

// DELETE /api/scans/:id - Delete scan
router.delete("/:id", scanController.deleteScan);

module.exports = router;
