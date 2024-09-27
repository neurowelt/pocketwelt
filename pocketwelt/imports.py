import importlib
from importlib.util import find_spec
import os
from types import ModuleType
from typing import Any, Dict, List

from pocketwelt.paths import get_all_attributes, build_all_paths


def is_package_available(name: str) -> bool:
    """
    Use to check for installation of a package. Finding path of the package
    does not import it, thus we can notify the user if some packages are missing.

    Args:
        name (str): Name of the package to check.
    """
    return find_spec(name) is not None


class LazyModule(ModuleType):
    """
    Module for lazy importing.

    Heavily based on:
        * https://github.com/optuna/optuna/blob/master/optuna/integration/__init__.py
        * https://github.com/huggingface/diffusers/blob/main/src/diffusers/utils/import_utils.py
    """

    def __init__(
        self, module_name: str, module_file: str, import_structure: Dict[str, List[str]]
    ):
        """
        Initialize a LazyModule instance.

        Args:
            module_name (str): Name of the module.
            module_file (str): File path of the module.
            import_structure (Dict[str, List[str]]): A dictionary representing the import structure.
        """
        super().__init__(module_name)
        self.__file__ = module_file
        self.__all__ = get_all_attributes(import_structure)
        self.__path__ = [os.path.dirname(module_file)]

        # Attributes for lazy importing based on structure
        self._import_structure = import_structure
        self._modules = set(import_structure.keys())
        self._objects_to_modules = build_all_paths(import_structure)

    def __getattr__(self, name: str) -> Any:
        """
        Retrieve module when requested from the namespace.

        Args:
            name (str): The name of the attribute to retrieve.

        Raises:
            AttributeError: If the attribute does not exist in the module.

        Returns:
            Any: The requested module or attribute.

        """
        if name in self._modules:
            value = self._get_module(name)
        elif name in self._objects_to_modules.keys():
            # Get the module and then create the whole import path
            _modules = self._objects_to_modules[name]
            module = self._get_module(".".join(_modules))
            value = getattr(module, name)
        else:
            raise AttributeError(f"module {self.__name__} has no attribute {name}")

        setattr(self, name, value)

        return value

    def _get_module(self, module_name: str):
        """
        Import the given module.

        Args:
            module_name (str): The name of the module to import.

        Raises:
            RuntimeError: If the module cannot be imported.

        Returns:
            module: The imported module.
        """
        try:
            return importlib.import_module("." + module_name, self.__name__)
        except Exception as e:
            raise RuntimeError(
                f"Failed to import {self.__name__}.{module_name} because of the following error:\n\n{e}"
            ) from e

    def __reduce__(self):
        """
        This method is used to ensure that the LazyModule objectcan be pickled and unpickled correctly.
        """
        return (self.__class__, (self.__name__, self.__file__, self._import_structure))
