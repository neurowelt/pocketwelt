import sys
from typing import TYPE_CHECKING

from pocketwelt.imports import LazyModule

__all__ = [
    "compress_file",
    "decompress_file",
    "fetch_module",
    "hash_file",
    "load_pickle",
    "save_pickle",
    "get_parent_path",
    "run_process",
    "build_all_paths",
    "build_top_paths",
    "get_all_attributes",
    "list_all_paths"
]

_import_structure = {
    "files": [
        "compress_file",
        "decompress_file"
    ],
    "modules": ["fetch_module"],
    "objects": [
        "hash_file",
        "load_pickle",
        "save_pickle"
    ],
    "paths": [
        "get_parent_path",
        "build_all_paths",
        "build_top_paths",
        "get_all_attributes",
        "list_all_paths"
    ],
    "processes": ["run_process"]
}


if TYPE_CHECKING:
    
    from pocketwelt.files import (
        compress_file,
        decompress_file
    )
    from pocketwelt.modules import fetch_module
    from pocketwelt.objects import (
        hash_file,
        load_pickle,
        save_pickle
    )
    from pocketwelt.paths import (
        build_all_paths,
        build_top_paths,
        get_all_attributes,
        get_parent_path,
        list_all_paths
    )
    from pocketwelt.processes import run_process

else:

    sys.modules[__name__] = LazyModule(
        module_name=__name__,
        module_file=globals()["__file__"],
        import_structure=_import_structure
    )
    