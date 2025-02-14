import importlib
from typing import Optional

from pocketwelt.processes import run_process


def fetch_module(package: str, alias: Optional[str] = None, skip_install: bool = True) -> None:
    """
    Try importing a package and install it if it's not available.

    Args:
        package (str): Name of the package to import and potentially install.
        alias (str): Alias for module used in code (e.g. `np` is an alias for `numpy`).
        skip_install (bool): If `True`, skip the installation of the package. Defaults to `True`.

    Raises:
        ImportError: If the package cannot be imported after installation attempt.

    Note:
        This function modifies the global namespace by adding the imported module.

    Example:
        >>> fetch_module('numpy', skip_install=False)
        # If numpy is not installed, it will be installed and then imported.
        # If numpy is already installed, it will just be imported.
    """
    try:
        importlib.import_module(package)
    except (ImportError, ModuleNotFoundError):
        if not skip_install:
            run_process(f"python -m pip install {package}")
        else:
            raise ImportError(f"Package {package} is not installed!")
    finally:
        globals()[alias or package] = importlib.import_module(package)
