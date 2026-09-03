class PatchGenerator:
    def generate_patch(self, file_path: str, old_alg: str, new_alg: str) -> str:
        diff_text = (
            f"--- a/{file_path}\n"
            f"+++ b/{file_path}\n"
            f"@@ -1,5 +1,5 @@\n"
            f"- # Legacy algorithm: {old_alg}\n"
            f"- use_crypto_algorithm('{old_alg}')\n"
            f"+ # Upgraded PQC algorithm: {new_alg}\n"
            f"+ use_crypto_algorithm('{new_alg}')\n"
        )
        return diff_text
