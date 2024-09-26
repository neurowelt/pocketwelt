import base64
import os
from io import BytesIO, StringIO
from typing import Any, Optional, Union


MIME_HEADERS = {
    "png": "image/png",
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "html": "text/html",
    "glb": "text/plain",
    "text": "text/plain",
    "wav": "audio/wav",
    "mp3": "audio/mpeg",
    "webm": "audio/webm",
    "mp4": "video/mp4",
    "mkv": "video/x-matroska",
    "avi": "video/x-msvideo",
    "zip": "application/zip",
    "md": "text/markdown",
    "pdf": "application/pdf",
}


def b64_encode(obj: Any, type_or_header: str) -> str:
    """
    Encode an object to a base64 string with a MIME header.

    Args:
        obj (Any): The object to encode. Can be a string (file path or content),
            `BytesIO`, `StringIO`, `bytes`, or any other object that can be
            converted to bytes. If `obj` does not support casting to bytes, will
            raise its own exception.
        type_or_header (str): Either a key from `MIME_HEADERS` or a full MIME header.

    Raises:
        ValueError: If the provided `type_or_header` is not supported or invalid.

    Returns:
        str: A string in the format "data:<mime_header>;base64,<encoded_data>".

    Examples:
        >>> b64_encode("hello.txt", "text")
        'data:text/plain;base64,aGVsbG8udHh0'

        >>> b64_encode(b"binary data", "application/octet-stream")
        'data:application/octet-stream;base64,YmluYXJ5IGRhdGE='
    """
    # First extract proper header
    if "/" not in type_or_header and type_or_header not in MIME_HEADERS:
        raise ValueError(
            f"{type_or_header} not supported. Either pass proper header"
            " or use provided headers (see `encodings.MIME_HEADERS`)."
        )
    mime_header = (
        type_or_header if "/" in type_or_header else MIME_HEADERS.get(type_or_header)
    )

    # For strings either enocde file content or text
    if isinstance(obj, str):
        if os.path.exists(obj):
            with open(obj, "rb") as file:
                enc_obj = base64.b64encode(file.read())
        else:
            enc_obj = base64.b64encode(obj.encode("utf-8"))

    # For buffers encode their value
    elif isinstance(obj, (BytesIO, StringIO)):
        obj.seek(0)  # make sure we read from the start
        if isinstance(obj, BytesIO):
            enc_obj = base64.b64encode(obj.getvalue())
        else:
            enc_obj = base64.b64encode(obj.getvalue().encode("utf-8"))
        obj.seek(0)  # return to starting position

    # For bytes simply encode them
    elif isinstance(obj, bytes):
        enc_obj = base64.b64encode(obj)

    # Anything else try casting to bytes and encoding
    else:
        enc_obj = base64.b64encode(bytes(obj))

    return f"data:{mime_header};base64,{enc_obj.decode('utf-8')}"


def b64_decode(encoded_obj: str, filepath: Optional[str] = None) -> Union[str, BytesIO]:
    """
    Decode a base64 encoded string.

    Args:
        encoded_obj (str): The base64 encoded string to decode.
        filepath (str, optional): The path to save the decoded content as a file.
            If `None`, the decoded content is returned as a `BytesIO` object. Defaults to `None`.

    Raises:
        FileExistsError: If the specified file path already exists.

    Returns:
        Union[str, BytesIO]: If `fileobj` is a valid path, returns the absolute path of the
            created file as a string. If `fileobj` is `None`, returns a `BytesIO` object containing
            the decoded content.

    Examples:
        >>> decoded = b64_decode("data:text/plain;base64,aGVsbG8=")
        >>> decoded.getvalue()
        b'hello'

        >>> file_path = b64_decode("data:text/plain;base64,aGVsbG8=", "output.txt")
        >>> with open(file_path, "r") as f:
        ...     print(f.read())
        hello
    """

    # Decode object
    decoded_obj = base64.b64decode(encoded_obj.split(",")[-1])

    # If not string, dump to binary buffer
    if filepath is None:
        return BytesIO(decoded_obj)

    # If string, treat as path
    if isinstance(filepath, str):
        if os.path.exists(filepath):
            raise FileExistsError(f"{filepath} is taken - interrupting decoding.")
        _dir = os.path.dirname(filepath)
        if _dir != "":
            os.makedirs(_dir, exist_ok=True)
        with open(filepath, "wb") as f:
            f.write(decoded_obj)
        return os.path.abspath(filepath)
