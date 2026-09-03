import hashlib


def hash_file_sha256(file_path: str) -> str:
    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()


def hash_bytes_sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()
