import os
from typing import List


def get_parent_path(path: str, level: int = 1, absolute: bool = True) -> str:
    """
    Find parent of a given path.

    Args:
        path (str): Path to get parent of.
        level (int, optional): How distant parent to look for. Defaults to 1.
        absolute (str): Return the absolute path to the parent. Defaults to `True`.

    Returns:
        str: Parent path of the given path.
    """
    assert level >= 0, "`level` must be at least 0."
    
    if absolute:
        path = os.path.abspath(path)
    if level > 0:
        return get_parent_path(os.path.dirname(path), level-1, False)
    
    return path

def list_all_paths(directory: str) -> List[str]:
    """
    List all paths from the given directory.

    Args:
        directory (str): Path to the directory.

    Returns:
        List[str]: List of all paths in the directory.
    """
    paths = []
    for root, dirs, files in os.walk(directory):
        for name in dirs + files:
            paths.append(os.path.join(root, name))
            
    return paths
