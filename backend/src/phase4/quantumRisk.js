// Phase 4 - Quantum Risk Analysis
// Classifies cryptographic algorithms based on their vulnerability
// to quantum computing attacks.

const quantumRiskDatabase = {
  // Public-key algorithms broken by Shor's algorithm
  RSA: {
    quantumVulnerable: true,
    risk: "CRITICAL",
    attack: "Shor's Algorithm",
    reason: "RSA can be broken by a sufficiently powerful quantum computer.",
  },

  RSA2048: {
    quantumVulnerable: true,
    risk: "CRITICAL",
    attack: "Shor's Algorithm",
    reason: "RSA-2048 is vulnerable to quantum factorization attacks.",
  },

  RSA3072: {
    quantumVulnerable: true,
    risk: "CRITICAL",
    attack: "Shor's Algorithm",
    reason: "RSA-3072 is vulnerable to quantum factorization attacks.",
  },

  RSA4096: {
    quantumVulnerable: true,
    risk: "CRITICAL",
    attack: "Shor's Algorithm",
    reason: "RSA-4096 is vulnerable to quantum factorization attacks.",
  },

  ECC: {
    quantumVulnerable: true,
    risk: "CRITICAL",
    attack: "Shor's Algorithm",
    reason: "Elliptic-curve cryptography is vulnerable to quantum attacks.",
  },

  ECDSA: {
    quantumVulnerable: true,
    risk: "CRITICAL",
    attack: "Shor's Algorithm",
    reason: "ECDSA signatures can be broken by sufficiently powerful quantum computers.",
  },

  ECDH: {
    quantumVulnerable: true,
    risk: "CRITICAL",
    attack: "Shor's Algorithm",
    reason: "ECDH key exchange is vulnerable to quantum attacks.",
  },

  DH: {
    quantumVulnerable: true,
    risk: "CRITICAL",
    attack: "Shor's Algorithm",
    reason: "Diffie-Hellman key exchange is vulnerable to quantum attacks.",
  },

  DSA: {
    quantumVulnerable: true,
    risk: "CRITICAL",
    attack: "Shor's Algorithm",
    reason: "DSA is vulnerable to quantum attacks.",
  },

  // Symmetric algorithms are affected by Grover's algorithm,
  // but are not completely broken in the same way as RSA/ECC.
  AES128: {
    quantumVulnerable: false,
    risk: "MEDIUM",
    attack: "Grover's Algorithm",
    reason: "Quantum search reduces the effective security of AES-128.",
  },

  AES192: {
    quantumVulnerable: false,
    risk: "LOW",
    attack: "Grover's Algorithm",
    reason: "AES-192 retains significant security against quantum search.",
  },

  AES256: {
    quantumVulnerable: false,
    risk: "LOW",
    attack: "Grover's Algorithm",
    reason: "AES-256 provides strong resistance against known quantum search attacks.",
  },

  SHA1: {
    quantumVulnerable: false,
    risk: "HIGH",
    attack: "Grover's Algorithm",
    reason: "SHA-1 is already cryptographically weak and quantum search further reduces its security margin.",
  },

  SHA256: {
    quantumVulnerable: false,
    risk: "LOW",
    attack: "Grover's Algorithm",
    reason: "SHA-256 retains substantial security against quantum search.",
  },

  SHA384: {
    quantumVulnerable: false,
    risk: "LOW",
    attack: "Grover's Algorithm",
    reason: "SHA-384 provides strong resistance against known quantum search attacks.",
  },

  SHA512: {
    quantumVulnerable: false,
    risk: "LOW",
    attack: "Grover's Algorithm",
    reason: "SHA-512 provides strong resistance against known quantum search attacks.",
  },
};

/**
 * Normalize an algorithm name so different representations
 * can be matched against the risk database.
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
 * Analyze the quantum risk of a cryptographic algorithm.
 *
 * @param {string} algorithm - Cryptographic algorithm name
 * @returns {object} Quantum risk assessment
 */
function assessQuantumRisk(algorithm) {
  const normalizedAlgorithm = normalizeAlgorithm(algorithm);

  // Direct match
  if (quantumRiskDatabase[normalizedAlgorithm]) {
    return {
      algorithm,
      normalizedAlgorithm,
      ...quantumRiskDatabase[normalizedAlgorithm],
    };
  }

  // Handle common algorithm variants
  if (normalizedAlgorithm.startsWith("RSA")) {
    return {
      algorithm,
      normalizedAlgorithm,
      ...quantumRiskDatabase.RSA,
    };
  }

  if (
    normalizedAlgorithm.includes("ECDSA") ||
    normalizedAlgorithm.includes("ECDH")
  ) {
    return {
      algorithm,
      normalizedAlgorithm,
      ...quantumRiskDatabase.ECC,
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
      ...quantumRiskDatabase.ECC,
    };
  }

  if (normalizedAlgorithm.includes("AES")) {
    if (normalizedAlgorithm.includes("256")) {
      return {
        algorithm,
        normalizedAlgorithm,
        ...quantumRiskDatabase.AES256,
      };
    }

    if (normalizedAlgorithm.includes("192")) {
      return {
        algorithm,
        normalizedAlgorithm,
        ...quantumRiskDatabase.AES192,
      };
    }

    return {
      algorithm,
      normalizedAlgorithm,
      ...quantumRiskDatabase.AES128,
    };
  }

  if (normalizedAlgorithm.includes("SHA512")) {
    return {
      algorithm,
      normalizedAlgorithm,
      ...quantumRiskDatabase.SHA512,
    };
  }

  if (normalizedAlgorithm.includes("SHA384")) {
    return {
      algorithm,
      normalizedAlgorithm,
      ...quantumRiskDatabase.SHA384,
    };
  }

  if (normalizedAlgorithm.includes("SHA256")) {
    return {
      algorithm,
      normalizedAlgorithm,
      ...quantumRiskDatabase.SHA256,
    };
  }

  if (normalizedAlgorithm.includes("SHA1")) {
    return {
      algorithm,
      normalizedAlgorithm,
      ...quantumRiskDatabase.SHA1,
    };
  }

  // Unknown algorithm
  return {
    algorithm,
    normalizedAlgorithm,
    quantumVulnerable: "UNKNOWN",
    risk: "UNKNOWN",
    attack: "Unknown",
    reason: "No quantum risk profile is currently available for this algorithm.",
  };
}

module.exports = {
  assessQuantumRisk,
  normalizeAlgorithm,
  quantumRiskDatabase,
};