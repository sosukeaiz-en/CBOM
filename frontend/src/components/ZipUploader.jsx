import React, { useState } from "react";

export default function ZipUploader({ onScanCreated }) {
  const [file, setFile] = useState(null);
  const [scanName, setScanName] = useState("");
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState(null);
  const [dragActive, setDragActive] = useState(false);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const droppedFile = e.dataTransfer.files[0];
      validateAndSetFile(droppedFile);
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      validateAndSetFile(e.target.files[0]);
    }
  };

  const validateAndSetFile = (selectedFile) => {
    setError(null);
    if (!selectedFile.name.endsWith(".zip")) {
      setError("Please select a valid .zip archive containing source code.");
      setFile(null);
      return;
    }
    setFile(selectedFile);
    if (!scanName) {
      setScanName(selectedFile.name.replace(/\.zip$/i, ""));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      setError("Please select a ZIP file to upload.");
      return;
    }

    setIsUploading(true);
    setError(null);

    const formData = new FormData();
    formData.append("zipFile", file);
    formData.append("name", scanName);

    try {
      const response = await fetch("http://localhost:5000/api/scans/upload", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Failed to upload and process ZIP file.");
      }

      setFile(null);
      setScanName("");
      if (onScanCreated) {
        onScanCreated(data.scan);
      }
    } catch (err) {
      setError(err.message || "An unexpected error occurred during upload.");
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="bg-gray-800 border border-gray-700 rounded-xl p-6 shadow-xl mb-8">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-lg font-semibold text-white flex items-center gap-2">
            <svg
              className="w-5 h-5 text-indigo-400"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"
              />
            </svg>
            Upload Source Code Archive (Phase 3)
          </h3>
          <p className="text-xs text-gray-400 mt-1">
            Upload a .zip source repository to extract and prepare for CBOM cryptographic scanning.
          </p>
        </div>
        <span className="px-2.5 py-1 bg-indigo-900/60 text-indigo-300 text-xs rounded-full font-medium border border-indigo-700/50">
          Max 50 MB
        </span>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        {/* Scan Project Name Input */}
        <div>
          <label className="block text-xs font-medium text-gray-300 mb-1">
            Scan Project Name (Optional)
          </label>
          <input
            type="text"
            value={scanName}
            onChange={(e) => setScanName(e.target.value)}
            placeholder="e.g. My-Nodejs-Service-v1"
            className="w-full bg-gray-900 border border-gray-700 rounded-lg px-3.5 py-2 text-sm text-white focus:outline-none focus:border-indigo-500 transition-colors"
          />
        </div>

        {/* Drag & Drop Zone */}
        <div
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
          className={`border-2 border-dashed rounded-xl p-8 text-center transition-colors ${
            dragActive
              ? "border-indigo-500 bg-indigo-950/20"
              : "border-gray-700 bg-gray-900/50 hover:border-gray-600"
          }`}
        >
          <input
            type="file"
            accept=".zip"
            id="zip-file-input"
            onChange={handleFileChange}
            className="hidden"
          />

          {!file ? (
            <label htmlFor="zip-file-input" className="cursor-pointer flex flex-col items-center">
              <div className="w-12 h-12 rounded-full bg-gray-800 border border-gray-700 flex items-center justify-center mb-3 text-indigo-400">
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
                  />
                </svg>
              </div>
              <p className="text-sm font-medium text-gray-200">
                Click to browse or drag & drop source ZIP here
              </p>
              <p className="text-xs text-gray-500 mt-1">
                Supports Node.js, Python, Java, Go repository archives (.zip)
              </p>
            </label>
          ) : (
            <div className="flex items-center justify-between bg-gray-800 p-4 rounded-lg border border-gray-700">
              <div className="flex items-center gap-3 text-left">
                <div className="p-2 bg-indigo-900/40 border border-indigo-700/40 rounded text-indigo-400">
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth="2"
                      d="M5 8h14M5 8a2 2 0 01-2-2V5a2 2 0 012-2h14a2 2 0 012 2v1a2 2 0 01-2 2M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4"
                    />
                  </svg>
                </div>
                <div>
                  <p className="text-sm font-medium text-white">{file.name}</p>
                  <p className="text-xs text-gray-400">
                    {(file.size / (1024 * 1024)).toFixed(2)} MB
                  </p>
                </div>
              </div>
              <button
                type="button"
                onClick={() => setFile(null)}
                className="text-gray-400 hover:text-red-400 text-xs px-2 py-1 rounded transition-colors"
              >
                Remove
              </button>
            </div>
          )}
        </div>

        {/* Error message display */}
        {error && (
          <div className="p-3 rounded-lg bg-red-950/60 border border-red-800 text-red-300 text-xs flex items-center gap-2">
            <svg className="w-4 h-4 shrink-0 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            {error}
          </div>
        )}

        {/* Submit button */}
        <div className="flex justify-end">
          <button
            type="submit"
            disabled={!file || isUploading}
            className={`px-5 py-2.5 rounded-lg text-sm font-medium transition-colors flex items-center gap-2 ${
              !file || isUploading
                ? "bg-gray-700 text-gray-400 cursor-not-allowed"
                : "bg-indigo-600 hover:bg-indigo-500 text-white shadow-lg shadow-indigo-600/30"
            }`}
          >
            {isUploading ? (
              <>
                <svg className="animate-spin w-4 h-4 text-white" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                </svg>
                Extracting & Validating...
              </>
            ) : (
              <>
                Upload & Create Scan
              </>
            )}
          </button>
        </div>
      </form>
    </div>
  );
}
