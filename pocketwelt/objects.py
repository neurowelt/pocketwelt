import os
import pickle
from typing import Any


def save_pickle(obj: Any, path: str, replace: bool = False) -> None:
    """
    Save an object to a file using pickle serialization.

    Args:
        obj (Any): Python object to be saved.
        path (str): File path where the object will be saved.
        replace (bool, optional): If `True`, overwrites the file if it already exists.
            Defaults to `False`.

    Raises:
        FileExistsError: If the file already exists and `replace` is `False`.
        ValueError: If given path does not containt .pkl extension.
    """
    if os.path.exists(path) and not replace:
        print(f'{path} already exists - either use `replace=True` or rename/move the file.')
    if not path.endswith('.pkl'):
        raise ValueError('Only pickle (.pkl) files are supported!')
    dir = os.path.dirname(path)
    if dir != '':
        os.makedirs(dir)
    with open(path, 'wb') as f:
        pickle.dump(obj, f)

def load_pickle(path: str) -> Any:
    """
    Load an object from a file using pickle deserialization.

    Args:
        path (str): The file path from which to load the object.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        ValueError: If given path does not containt .pkl extension.

    Returns:
        Any: Deserialized Python object loaded from the file.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f'{path} does not exist!')
    if not path.endswith('.pkl'):
        raise ValueError('Only pickle (.pkl) files are supported!')
    
    return pickle.load(open(path, 'rb'))
