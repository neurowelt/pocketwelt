# `logs`

This module contains two classed designed for enhanced logging experience: `ColorFormatter` and `CustomLogger`.

## `ColorFormatter`

```{eval-rst}
.. autoclass:: pocketwelt.logs.ColorFormatter
    :members:
    :undoc-members:
    :show-inheritance:
```

## `CustomLogger`

```{eval-rst}
.. autoclass:: pocketwelt.logs.CustomLogger
    :members:
    :undoc-members:
    :show-inheritance:
```

## `stdout_to_logger`

```{eval-rst}
.. autofunction:: pocketwelt.logs.stdout_to_logger
```

## `getCustomLogger`

```{eval-rst}
.. autofunction:: pocketwelt.logs.getCustomLogger
```

## `DATETIME_FMT`

Default datetime format:

```python
DATETIME_FMT = "%Y-%m-%d %H:%M:%S"
```

## `LOG_FMT`

Default logs format:

```python
LOG_FMT = "%(asctime)s  %(levelname)-8s %(filename)s:%(lineno)d >>  %(message)s"
```