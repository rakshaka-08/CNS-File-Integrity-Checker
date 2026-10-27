from hashing import calculate_sha256


def verify_file(file_path, original_hash):
    current_hash = calculate_sha256(file_path)

    if current_hash == original_hash.strip().lower():
        return True, current_hash

    return False, current_hash