import os


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
