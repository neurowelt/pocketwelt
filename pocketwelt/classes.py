from typing import Optional, Tuple


def replace_parents(
    cls: type,
    remove_parents: Optional[Tuple[type, ...]] = None,
    place_parents: Optional[Tuple[type, ...]] = None,
) -> type:
    """
    Modify the class to replace parents with new ones. Also allows to just remove or add new parents.

    Args:
        cls (type): Class to modify.

    Returns:
        type: Modified class.
    """
    # Remove specified parents
    clss = list(
        cls.__mro__
    )  # list all classes this class is built from (itself and parents)
    for _cls in clss:
        if remove_parents and _cls.__name__ in remove_parents:  # remove specified parents
            clss.remove(_cls)
    
    # Create new class with different parents
    new_parents = tuple(clss)
    if place_parents:
        new_parents = place_parents + new_parents
    cls = type(cls.__name__, new_parents, dict(cls.__dict__))

    return cls
