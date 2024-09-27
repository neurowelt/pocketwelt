# `imports`

This module contains `LazyModule` class for lazy importing of modules and a simple package availability check.

It is not intended for regular importing, as it works as the `__init__.py` namespace resident - it can be assigned to `sys.modules[__name__]` in order to perform lazy loading of modules by passing just the import structure instead of imported models.

For example implementation, check out [the `__init__.py` script of this package](https://github.com/neurowelt/pocketwelt/blob/main/pocketwelt/__init__.py)!

## `LazyModule`

```{eval-rst}
.. autoclass:: pocketwelt.imports.LazyModule
    :members:
    :undoc-members:
    :show-inheritance:
```

## `is_package_available`

```{eval-rst}
.. autofunction:: pocketwelt.imports.is_package_available
```
