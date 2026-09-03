COMPATIBILITY_MATRIX = {
    "ML-KEM-768": {
        "hybrid_mode_supported": True,
        "hybrid_pair": "ECDH-P256 + ML-KEM-768",
        "tls13_draft_supported": True,
        "x509_extension_supported": True
    },
    "ML-DSA-65": {
        "hybrid_mode_supported": True,
        "hybrid_pair": "ECDSA-P256 + ML-DSA-65",
        "tls13_draft_supported": True,
        "x509_extension_supported": True
    },
    "SLH-DSA-SHA2-128f": {
        "hybrid_mode_supported": False,
        "hybrid_pair": "N/A",
        "tls13_draft_supported": False,
        "x509_extension_supported": True
    }
}
