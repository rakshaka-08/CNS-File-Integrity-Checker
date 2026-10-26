import hashlib
import tempfile
import os

from hashing import calculate_sha256


def test_hash_generation():
    content = b"Hello CNS Project"

    with tempfile.NamedTemporaryFile(delete=False) as file:
        file.write(content)
        file_path = file.name

    try:
        actual_hash = calculate_sha256(file_path)
        expected_hash = hashlib.sha256(content).hexdigest()

        assert actual_hash == expected_hash
        print("Test passed!")

    finally:
        os.remove(file_path)


if __name__ == "__main__":
    test_hash_generation()