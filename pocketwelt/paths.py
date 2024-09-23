import os
from typing import Any, Dict, List, Optional


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

def build_all_paths(structure: Dict[str, Any], current_path: Optional[list] = None,
                    result: Optional[dict] = None) -> Dict[str, Any]:
    """
    Recursively build a dictionary of all paths from a nested dictionary.

    Args:
        structure (Dict[str, Any]): The nested dictionary structure to process.
        current_path (Optional[list], optional): The current path being processed. 
            Defaults to `None`.
        result (Optional[dict], optional): The dictionary to store the results.
            Defaults to `None`.

    Returns:
        Dict[str, Any]: A dictionary containing all paths from the nested dictionary.
    """
    if result is None:
        result = dict()
    if current_path is None:
        current_path = list()

    for key, value in structure.items():
        if isinstance(value, dict):
            build_all_paths(value, current_path + [key], result)
        else:
            result[key] = current_path
            for item in value:
                result[item] = current_path + [key]

    return result

def build_top_paths(structure: Dict[str, Any], current_path: Optional[str] = None) -> List[str]:
    """
    Recursively build a list of all possible paths for a given nested dictionary.

    Args:
        structure (Dict[str, Any]): The nested dictionary structure to process.
        current_path (Optional[str], optional): The current path being processed.
            Defaults to `None`.

    Returns:
        List[str]: A list of all possible paths from the nested dictionary.
    """
    paths = []
    for key, value in structure.items():
        if isinstance(value, dict):
            for sub_path in build_top_paths(value, key):
                paths.append(f"{sub_path}")
        else:
            for item in value:
                paths.append(
                    f"{key}.{item}"
                    if current_path is None
                    else f"{current_path}.{key}.{item}"
                )

    return paths

def get_all_attributes(structure: Dict[str, Any], attrs: Optional[List[str]] = None) -> List[str]:
    """
    Recursively retrieve all names that exist in the nested dictionary.

    Args:
        structure (Dict[str, Any]): The nested dictionary structure to process.
        attrs (Optional[List[str]], optional): The list to store the attribute names.
            Defaults to `None`.

    Returns:
        List[str]: A list of all unique attribute names in the nested dictionary.
    """
    if attrs is None:
        attrs = []

    for key, value in structure.items():
        attrs.append(key)
        if isinstance(value, dict):
            get_all_attributes(value, attrs)
        elif isinstance(value, list):
            for item in value:
                attrs.append(item)

    return list(set(attrs))
