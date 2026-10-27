import hashlib
import tempfile
import os

from verification import verify_file


def test_verification():
    content = b"Hello CNS Project"

    with tempfile.NamedTemporaryFile(delete=False) as file:
        file.write(content)
        file_path = file.name

    try:
        original_hash = hashlib.sha256(content).hexdigest()

        result, current_hash = verify_file(
            file_path, original_hash
        )

        assert result is True
        print("Original file verification passed!")

        with open(file_path, "wb") as file:
            file.write(b"Modified CNS Project")

        result, current_hash = verify_file(
            file_path, original_hash
        )

        assert result is False
        print("Modified file detection passed!")

    finally:
        os.remove(file_path)


if __name__ == "__main__":
    test_verification()