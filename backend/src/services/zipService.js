const AdmZip = require("adm-zip");
const path = require("path");
const fs = require("fs");

/**
 * Supported file extensions for crypto scanning
 */
const SUPPORTED_EXTENSIONS = new Set([
  ".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs",
  ".json", ".py", ".java", ".go", ".c", ".cpp",
  ".cs", ".php", ".rb", ".rs", ".env", ".yml", ".yaml"
]);

/**
 * Safely extracts a ZIP archive into destination folder with Zip-Slip protection
 * @param {string} zipFilePath - Path to temporary zip file
 * @param {string} scanId - Unique scan identifier
 * @returns {Promise<{ extractedDir: string, totalFiles: number, supportedFiles: string[] }>}
 */
async function extractZipSafely(zipFilePath, scanId) {
  const baseExtractedDir = path.join(__dirname, "../../uploads/extracted");
  const targetDir = path.join(baseExtractedDir, scanId);

  // Ensure target extraction directory exists
  if (!fs.existsSync(targetDir)) {
    fs.mkdirSync(targetDir, { recursive: true });
  }

  const zip = new AdmZip(zipFilePath);
  const zipEntries = zip.getEntries();

  let totalFiles = 0;
  const supportedFiles = [];

  const resolvedTargetDir = path.resolve(targetDir);

  for (const entry of zipEntries) {
    if (entry.isDirectory) continue;

    // Zip-Slip Path Traversal Protection
    const entryName = entry.entryName;
    const destPath = path.resolve(targetDir, entryName);

    // Verify that the entry destination stays within the target directory
    if (!destPath.startsWith(resolvedTargetDir + path.sep) && destPath !== resolvedTargetDir) {
      throw new Error(`Security Violation: Zip entry "${entryName}" contains illegal path traversal (Zip Slip vulnerability detected).`);
    }

    // Extract file safely
    zip.extractEntryTo(entry, targetDir, true, true);
    totalFiles++;

    const ext = path.extname(entryName).toLowerCase();
    if (SUPPORTED_EXTENSIONS.has(ext)) {
      supportedFiles.push(entryName);
    }
  }

  // Cleanup temp ZIP file after extraction
  try {
    if (fs.existsSync(zipFilePath)) {
      fs.unlinkSync(zipFilePath);
    }
  } catch (cleanupErr) {
    console.warn("Could not delete temp zip file:", cleanupErr.message);
  }

  return {
    extractedDir: targetDir,
    totalFiles,
    supportedFiles,
  };
}

module.exports = {
  extractZipSafely,
  SUPPORTED_EXTENSIONS,
};
