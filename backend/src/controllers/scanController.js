const Scan = require("../models/Scan");
const { extractZipSafely } = require("../services/zipService");
const fs = require("fs");

/**
 * Handles ZIP file upload and initiates scan creation & extraction
 */
exports.createScan = async (req, res) => {
  if (!req.file) {
    return res.status(400).json({ error: "No ZIP file uploaded. Please upload a .zip archive." });
  }

  const { originalname, path: zipFilePath, size } = req.file;
  const scanName = req.body.name || originalname.replace(/\.zip$/i, "");

  let scanRecord = null;

  try {
    // 1. Create Scan record in DB
    scanRecord = new Scan({
      name: scanName,
      originalFileName: originalname,
      zipSize: size,
      status: "uploading",
    });
    await scanRecord.save();

    // 2. Safely extract ZIP archive
    const { extractedDir, totalFiles, supportedFiles } = await extractZipSafely(
      zipFilePath,
      scanRecord._id.toString()
    );

    // 3. Update Scan record with extraction details
    scanRecord.status = "extracted";
    scanRecord.extractedPath = extractedDir;
    scanRecord.totalFiles = totalFiles;
    scanRecord.supportedFiles = supportedFiles;
    await scanRecord.save();

    return res.status(201).json({
      message: "ZIP uploaded and extracted successfully.",
      scan: scanRecord,
    });
  } catch (error) {
    console.error("Scan Creation / Extraction Error:", error);

    // Cleanup temp uploaded file if it still exists
    if (fs.existsSync(zipFilePath)) {
      try {
        fs.unlinkSync(zipFilePath);
      } catch (e) {
        // ignore
      }
    }

    if (scanRecord) {
      scanRecord.status = "failed";
      scanRecord.errorMessage = error.message;
      await scanRecord.save();
    }

    return res.status(500).json({
      error: error.message || "Failed to process uploaded ZIP file.",
      scanId: scanRecord ? scanRecord._id : null,
    });
  }
};

/**
 * Gets list of all scans
 */
exports.getScans = async (req, res) => {
  try {
    const scans = await Scan.find().sort({ createdAt: -1 });
    return res.json({ scans });
  } catch (error) {
    return res.status(500).json({ error: "Failed to fetch scans." });
  }
};

/**
 * Gets details of a specific scan
 */
exports.getScanById = async (req, res) => {
  try {
    const scan = await Scan.findById(req.params.id);
    if (!scan) {
      return res.status(404).json({ error: "Scan not found." });
    }
    return res.json({ scan });
  } catch (error) {
    return res.status(500).json({ error: "Failed to fetch scan details." });
  }
};

/**
 * Deletes a scan record and removes extracted files from disk
 */
exports.deleteScan = async (req, res) => {
  try {
    const scan = await Scan.findById(req.params.id);
    if (!scan) {
      return res.status(404).json({ error: "Scan not found." });
    }

    // Clean up extracted files
    if (scan.extractedPath && fs.existsSync(scan.extractedPath)) {
      fs.rmSync(scan.extractedPath, { recursive: true, force: true });
    }

    await Scan.findByIdAndDelete(req.params.id);
    return res.json({ message: "Scan deleted successfully." });
  } catch (error) {
    return res.status(500).json({ error: "Failed to delete scan." });
  }
};
