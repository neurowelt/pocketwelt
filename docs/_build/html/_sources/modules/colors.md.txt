# `colors`

This module contains a very much simplified implementation of [`click`](https://github.com/pallets/click) module to allow for string coloring.

It is not intended to be used as standalone, but as part of the [`ColorFormatter`](./logs.md#colorformatter) class. Unless you need to color your strings somewhere else!

This module also provides structures with RGB and string named colors

## `click`

```{eval-rst}
.. autoclass:: pocketwelt.colors.click
    :members:
    :undoc-members:
    :show-inheritance:
```

## `_ANSI_COLORS`

Dictionary with human-readable color names and their ANSI codes:

```python
from pocketwelt.colors import _ANSI_COLORS
```

## `RGBColor`

Enumerator with color names and their corresponding RGB color tuples:

```python
from pocketwelt.colors import RGBColor

# Extract tuple (255, 0 , 0)
red = RGBColor.RED
```
