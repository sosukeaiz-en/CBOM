import React from "react";

export default function ScanList({ scans, onDeleteScan, isLoading }) {
  if (isLoading) {
    return (
      <div className="bg-gray-800 border border-gray-700 rounded-xl p-6 text-center text-gray-400 text-sm">
        Loading scan history...
      </div>
    );
  }

  if (!scans || scans.length === 0) {
    return (
      <div className="bg-gray-800 border border-gray-700 rounded-xl p-8 text-center">
        <div className="w-12 h-12 rounded-full bg-gray-900 border border-gray-700 flex items-center justify-center mx-auto mb-3 text-gray-500">
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
        </div>
        <p className="text-sm font-medium text-gray-300">No Scans Found</p>
        <p className="text-xs text-gray-500 mt-1">Upload a source repository ZIP above to create your first scan.</p>
      </div>
    );
  }

  const getStatusBadge = (status) => {
    switch (status) {
      case "extracted":
        return <span className="px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-900/60 text-green-300 border border-green-700/50">Extracted & Ready</span>;
      case "uploading":
        return <span className="px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-900/60 text-yellow-300 border border-yellow-700/50 animate-pulse">Uploading</span>;
      case "scanning":
        return <span className="px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-900/60 text-blue-300 border border-blue-700/50 animate-pulse">Scanning</span>;
      case "completed":
        return <span className="px-2.5 py-0.5 rounded-full text-xs font-medium bg-emerald-900/60 text-emerald-300 border border-emerald-700/50">Completed</span>;
      case "failed":
        return <span className="px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-900/60 text-red-300 border border-red-700/50">Failed</span>;
      default:
        return <span className="px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-700 text-gray-300">{status}</span>;
    }
  };

  return (
    <div className="bg-gray-800 border border-gray-700 rounded-xl overflow-hidden shadow-xl">
      <div className="px-6 py-4 border-b border-gray-700 flex items-center justify-between">
        <h3 className="text-sm font-semibold text-white tracking-wide uppercase">
          Scanned Repositories ({scans.length})
        </h3>
      </div>

      <div className="divide-y divide-gray-700/60">
        {scans.map((scan) => (
          <div key={scan._id} className="p-5 hover:bg-gray-750/50 transition-colors flex items-center justify-between">
            <div className="space-y-1">
              <div className="flex items-center gap-3">
                <span className="font-semibold text-white text-sm">{scan.name}</span>
                {getStatusBadge(scan.status)}
              </div>
              <p className="text-xs text-gray-400">
                Original file: <span className="text-gray-300">{scan.originalFileName}</span> ({(scan.zipSize / (1024 * 1024)).toFixed(2)} MB)
              </p>
              <div className="flex items-center gap-4 text-xs text-gray-500 pt-1">
                <span>📁 Total Files: <strong className="text-gray-300">{scan.totalFiles}</strong></span>
                <span>⚡ Code Files: <strong className="text-indigo-400">{scan.supportedFiles ? scan.supportedFiles.length : 0}</strong></span>
                <span>📅 Created: {new Date(scan.createdAt).toLocaleString()}</span>
              </div>
              {scan.errorMessage && (
                <p className="text-xs text-red-400 mt-1">Error: {scan.errorMessage}</p>
              )}
            </div>

            <div className="flex items-center gap-3">
              <button
                onClick={() => onDeleteScan(scan._id)}
                className="text-xs text-gray-400 hover:text-red-400 bg-gray-900 border border-gray-700 hover:border-red-950 px-3 py-1.5 rounded-lg transition-colors"
              >
                Delete
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
