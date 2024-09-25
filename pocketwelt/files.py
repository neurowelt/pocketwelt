import gzip
import pickle
import shutil
from typing import Any


def compress_file(file_path: str, compressed_file_path: str) -> None:
    """
    Compress file using GZIP.

    Args:
        file_path (str): The path to the file to be compressed.
        compressed_file_path (str): The path where the compressed file will be saved.
    """
    with open(file_path, 'rb') as f_in:
        with open(compressed_file_path, 'wb') as f_out:
            with gzip.GzipFile(file_path, 'wb', fileobj=f_out) as f_out:
                shutil.copyfileobj(f_in, f_out)

def decompress_file(compressed_file_path: str) -> Any:
    """
    Decompress a GZIP-compressed file and return its contents.

    Args:
        compressed_file_path (str): The path to the compressed file.

    Returns:
        Any: The decompressed and deserialized content of the file.
            We first read the content and then try unpickling. If that fails
            we simply decode the content from bytes.
    """
    with gzip.open(compressed_file_path, 'rb') as f_in:
        content = f_in.read()
        try:
            return pickle.loads(content)
        except pickle.UnpicklingError:
            return content.decode('utf-8')