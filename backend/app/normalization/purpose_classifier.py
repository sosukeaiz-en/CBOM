from app.models.enums import AlgPurpose


class PurposeClassifier:
    def classify(self, algorithm: str, matched_construct: str) -> AlgPurpose:
        alg_upper = algorithm.upper()
        construct_upper = matched_construct.upper()

        if any(kw in alg_upper or kw in construct_upper for kw in ["RSA_PUBLIC_ENCRYPT", "RSA_PRIVATE_DECRYPT", "ECDH", "KEY_EXCHANGE", "KEY_ESTABLISHMENT"]):
            return AlgPurpose.KEY_ESTABLISHMENT
        if any(kw in alg_upper or kw in construct_upper for kw in ["SIGN", "VERIFY", "ECDSA", "RSASSA"]):
            return AlgPurpose.SIGNATURE
        if any(kw in alg_upper or kw in construct_upper for kw in ["AES", "3DES", "DES", "CHACHA", "ENCRYPT"]):
            return AlgPurpose.ENCRYPTION
        if any(kw in alg_upper or kw in construct_upper for kw in ["SHA256", "SHA384", "SHA512", "SHA-2", "SHA1", "MD5", "HASH"]):
            return AlgPurpose.HASHING
        if "MAC" in alg_upper or "HMAC" in construct_upper:
            return AlgPurpose.MAC
        return AlgPurpose.AUTHENTICATION
