import os

from pocketwelt import compress_file, decompress_file


def test_file_compression() -> None:
    """
    Test compressing and decompressing a file.
    """
    with open("tests/file.txt", "w") as f:
        f.write("content")
    zip_path = "tests/archive.zip"
    compress_file("tests/file.txt", zip_path)
    contents = decompress_file(zip_path)

    assert contents == "content"

    os.remove("tests/file.txt")
    os.remove(zip_path)
