// Phase 4 - Post-Quantum Cryptography Recommendations
// Provides PQC and hybrid migration recommendations
// based on detected cryptographic algorithms.

const recommendationDatabase = {
  RSA: {
    replacement: "ML-KEM",
    hybrid: "RSA + ML-KEM",
    category: "Key Encapsulation",
    reason:
      "RSA is vulnerable to Shor's algorithm. ML-KEM provides a post-quantum key encapsulation mechanism.",
    priority: "CRITICAL",
  },

  RSA2048: {
    replacement: "ML-KEM-768",
    hybrid: "RSA-2048 + ML-KEM-768",
    category: "Key Encapsulation",
    reason:
      "RSA-2048 is vulnerable to quantum factorization attacks and should be migrated to a post-quantum key establishment mechanism.",
    priority: "CRITICAL",
  },

  RSA3072: {
    replacement: "ML-KEM-768",
    hybrid: "RSA-3072 + ML-KEM-768",
    category: "Key Encapsulation",
    reason:
      "RSA-3072 remains vulnerable to sufficiently powerful quantum computers.",
    priority: "CRITICAL",
  },

  RSA4096: {
    replacement: "ML-KEM-1024",
    hybrid: "RSA-4096 + ML-KEM-1024",
    category: "Key Encapsulation",
    reason:
      "RSA-4096 is vulnerable to Shor's algorithm and should be migrated to PQC.",
    priority: "CRITICAL",
  },

  ECC: {
    replacement: "ML-KEM / ML-DSA",
    hybrid: "ECC + PQC",
    category: "Key Exchange / Digital Signature",
    reason:
      "Elliptic-curve cryptography is vulnerable to Shor's algorithm.",
    priority: "CRITICAL",
  },

  ECDSA: {
    replacement: "ML-DSA",
    hybrid: "ECDSA + ML-DSA",
    category: "Digital Signature",
    reason:
      "ECDSA signatures are vulnerable to quantum attacks. ML-DSA provides a post-quantum signature alternative.",
    priority: "CRITICAL",
  },

  ECDH: {
    replacement: "ML-KEM",
    hybrid: "ECDH + ML-KEM",
    category: "Key Exchange",
    reason:
      "ECDH is vulnerable to quantum attacks. ML-KEM provides a post-quantum key establishment mechanism.",
    priority: "CRITICAL",
  },

  DH: {
    replacement: "ML-KEM",
    hybrid: "DH + ML-KEM",
    category: "Key Exchange",
    reason:
      "Diffie-Hellman is vulnerable to Shor's algorithm.",
    priority: "CRITICAL",
  },

  DSA: {
    replacement: "ML-DSA",
    hybrid: "DSA + ML-DSA",
    category: "Digital Signature",
    reason:
      "DSA is vulnerable to quantum attacks and should be migrated to a post-quantum signature scheme.",
    priority: "CRITICAL",
  },

  AES128: {
    replacement: "AES-256",
    hybrid: "AES-256",
    category: "Symmetric Encryption",
    reason:
      "Grover's algorithm reduces the effective security of AES-128. AES-256 provides a stronger quantum security margin.",
    priority: "MEDIUM",
  },

  AES192: {
    replacement: "AES-256",
    hybrid: "AES-256",
    category: "Symmetric Encryption",
    reason:
      "AES-256 provides a larger security margin against quantum search attacks.",
    priority: "LOW",
  },

  AES256: {
    replacement: "AES-256",
    hybrid: "AES-256",
    category: "Symmetric Encryption",
    reason:
      "AES-256 is considered suitable for continued use with respect to known quantum search attacks.",
    priority: "LOW",
  },

  SHA1: {
    replacement: "SHA-256 or SHA-384",
    hybrid: "SHA-256",
    category: "Hash Function",
    reason:
      "SHA-1 is cryptographically weak and should be replaced regardless of quantum considerations.",
    priority: "HIGH",
  },

  SHA256: {
    replacement: "SHA-256",
    hybrid: "SHA-256",
    category: "Hash Function",
    reason:
      "SHA-256 provides a strong security margin against known quantum search attacks.",
    priority: "LOW",
  },

  SHA384: {
    replacement: "SHA-384",
    hybrid: "SHA-384",
    category: "Hash Function",
    reason:
      "SHA-384 provides strong resistance against known quantum search attacks.",
    priority: "LOW",
  },

  SHA512: {
    replacement: "SHA-512",
    hybrid: "SHA-512",
    category: "Hash Function",
    reason:
      "SHA-512 provides strong resistance against known quantum search attacks.",
    priority: "LOW",
  },
};


/**
 * Normalize an algorithm name.
 */
function normalizeAlgorithm(algorithm) {
  if (!algorithm) {
    return "";
  }

  return algorithm
    .toString()
    .toUpperCase()
    .replace(/[-_\s]/g, "");
}


/**
 * Get a PQC recommendation for an algorithm.
 *
 * @param {string} algorithm - Cryptographic algorithm
 * @returns {object} Recommendation
 */
function getRecommendation(algorithm) {
  const normalizedAlgorithm = normalizeAlgorithm(algorithm);

  // Exact match
  if (recommendationDatabase[normalizedAlgorithm]) {
    return {
      algorithm,
      normalizedAlgorithm,
      ...recommendationDatabase[normalizedAlgorithm],
    };
  }

  // RSA variants
  if (normalizedAlgorithm.startsWith("RSA")) {
    return {
      algorithm,
      normalizedAlgorithm,
      ...recommendationDatabase.RSA,
    };
  }

  // ECC variants
  if (normalizedAlgorithm.includes("ECDSA")) {
    return {
      algorithm,
      normalizedAlgorithm,
      ...recommendationDatabase.ECDSA,
    };
  }

  if (normalizedAlgorithm.includes("ECDH")) {
    return {
      algorithm,
      normalizedAlgorithm,
      ...recommendationDatabase.ECDH,
    };
  }

  if (
    normalizedAlgorithm === "ECC" ||
    normalizedAlgorithm.includes("SECP") ||
    normalizedAlgorithm.includes("CURVE25519")
  ) {
    return {
      algorithm,
      normalizedAlgorithm,
      ...recommendationDatabase.ECC,
    };
  }

  // AES variants
  if (normalizedAlgorithm.includes("AES")) {
    if (normalizedAlgorithm.includes("256")) {
      return {
        algorithm,
        normalizedAlgorithm,
        ...recommendationDatabase.AES256,
      };
    }

    if (normalizedAlgorithm.includes("192")) {
      return {
        algorithm,
        normalizedAlgorithm,
        ...recommendationDatabase.AES192,
      };
    }

    return {
      algorithm,
      normalizedAlgorithm,
      ...recommendationDatabase.AES128,
    };
  }

  // SHA variants
  if (normalizedAlgorithm.includes("SHA512")) {
    return {
      algorithm,
      normalizedAlgorithm,
      ...recommendationDatabase.SHA512,
    };
  }

  if (normalizedAlgorithm.includes("SHA384")) {
    return {
      algorithm,
      normalizedAlgorithm,
      ...recommendationDatabase.SHA384,
    };
  }

  if (normalizedAlgorithm.includes("SHA256")) {
    return {
      algorithm,
      normalizedAlgorithm,
      ...recommendationDatabase.SHA256,
    };
  }

  if (normalizedAlgorithm.includes("SHA1")) {
    return {
      algorithm,
      normalizedAlgorithm,
      ...recommendationDatabase.SHA1,
    };
  }

  // Unknown algorithm
  return {
    algorithm,
    normalizedAlgorithm,
    replacement: "UNKNOWN",
    hybrid: "UNKNOWN",
    category: "UNKNOWN",
    reason:
      "No post-quantum recommendation is currently available for this algorithm.",
    priority: "UNKNOWN",
  };
}


module.exports = {
  getRecommendation,
  normalizeAlgorithm,
  recommendationDatabase,
};