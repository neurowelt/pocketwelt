import os

from PIL import Image

from pocketwelt import b64_decode, b64_encode


def test_b64_encodings() -> None:
    """
    Test encoding and decoding in base64.
    """
    # Bytes
    encoded_obj = b64_encode(b"binary data", "application/octet-stream")
    decoded_obj = b64_decode(encoded_obj)
    assert decoded_obj.getvalue() == b"binary data"  # type: ignore

    # String
    encoded_obj = b64_encode("string data", "text")
    decoded_obj = b64_decode(encoded_obj)
    assert decoded_obj.getvalue().decode("utf-8") == "string data"  # type: ignore

    # Image
    image = Image.open("tests/test_image.png")
    encoded_obj = b64_encode("tests/test_image.png", "png")
    decoded_obj = b64_decode(encoded_obj)
    decoded_image = Image.open(decoded_obj)
    assert decoded_image == image

    # File
    with open("tests/test.md", "w") as f:
        f.write("# Content")
    encoded_obj = b64_encode("tests/test.md", "md")
    decoded_obj = b64_decode(encoded_obj, filepath="tests/test2.md")
    with open("tests/test2.md", "r") as f:
        assert f.read() == "# Content"
    os.remove("tests/test.md")
    os.remove("tests/test2.md")
