import copy
import logging
import os
from contextlib import redirect_stdout
from datetime import datetime
from io import StringIO
from typing import Any, Callable, Literal, Optional, Union

from pocketwelt.colors import RGBColor

try:
    import click
except ImportError:
    print(
        "Package called `click` has not been found."
        "Importing replacement class from `pocketwelt.colors`"
    )
    from pocketwelt.colors import click


DATETIME_FMT = "%Y-%m-%d %H:%M:%S"
LOG_FMT = "%(asctime)s  %(levelname)-8s %(filename)s:%(lineno)d >>  %(message)s"


class ColorFormatter(logging.Formatter):
    """
    Custom colored formatter converting logRecord to text.

    Adapted from:
        * https://github.com/encode/uvicorn/blob/master/uvicorn/logging.py
    """

    level_name_colors = {
        logging.DEBUG: lambda msg: click.style(str(msg), fg=RGBColor.TEAL),
        logging.INFO: lambda msg: click.style(str(msg), fg=RGBColor.GREEN),
        logging.WARNING: lambda msg: click.style(str(msg), fg=RGBColor.YELLOW),
        logging.ERROR: lambda msg: click.style(str(msg), fg=RGBColor.CRIMSON),
        logging.CRITICAL: lambda msg: click.style(str(msg), fg=RGBColor.RED),
    }

    def __init__(
        self,
        fmt: Optional[str] = LOG_FMT,
        datefmt: Optional[str] = DATETIME_FMT,
        style: Literal["%", "{", "$"] = "%",
        use_colors: bool = True,
    ) -> None:
        """
        Initialize the ColorFormatter.

        Args:
            fmt (Optional[str], optional): The format string. Defaults to `None`.
            datefmt (Optional[str], optional): The date format string. Defaults to `None`.
            style (Literal["%", "{", "$"], optional): The style of the format string. Defaults to '%'.
            use_colors (bool, optional): Whether to use colors in the output. Defaults to `False`.
        """
        self.use_colors = use_colors
        super().__init__(fmt=fmt, datefmt=datefmt, style=style)

    def color_message(self, level_no: int, msg: str) -> str:
        """
        Color the log message based on the log level.

        Args:
            level_no (int): The log level number.
            msg (str): The log message.

        Returns:
            str: The colored log message.
        """
        coloring_func = self.level_name_colors.get(
            level_no, lambda msg: click.style(str(msg), fg=RGBColor.GREEN)
        )

        return coloring_func(msg)

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the specified record.

        Args:
            record (logging.LogRecord): The log record to be formatted.

        Returns:
            str: The formatted log record as a string, possibly with color applied.
        """
        s = super().format(record)
        if self.use_colors:
            s = self.color_message(record.levelno, s)

        return s


class CustomLogger(logging.Logger):
    """
    Custom Logger class accepting formatter objects and adding file logging option.
    """

    def __init__(
        self,
        name: str,
        level: Union[str, int],
        formatter: Optional[logging.Formatter] = None,
        log_directory: Optional[str] = None,
        use_colors: bool = True,
        **fmt_kwargs: Any,
    ) -> None:
        """
        Initialize the custom logger class which accepts `ColorFormatter` and log file to
        dump your logs to.

        Args:
            name (str): The name of the logger.
            level (Union[str, int]): The logging level for this logger.
            formatter (logging.Formatter, optional): Formatter to set for stream and file handlers.
                Defaults to `None` (use default formatters).
            log_directory (str, optional): The directory to store log files.
                If provided, log files will be created. Defaults to `None`.
            use_colors (bool): Whether to use colored logs. Defaults to `True`.
            **fmt_kwargs: Formatting keywords: `fmt` and `datefmt` for the formatter.
        """
        super().__init__(name, level)

        # Prepare formatter
        formatter = formatter or ColorFormatter(
            use_colors=use_colors,
            fmt=fmt_kwargs.get("fmt", LOG_FMT),
            datefmt=fmt_kwargs.get("datefmt", DATETIME_FMT),
        )
        handler = logging.StreamHandler()
        handler.setLevel(level)
        handler.setFormatter(formatter)
        self.addHandler(handler)

        # Create file logging
        if log_directory is not None:
            os.makedirs(log_directory, exist_ok=True)
            log_name = (
                "log"
                + f"_{name.lower()}_"
                + datetime.now().strftime("%Y-%m-%d_%H%M")
                + ".txt"
            )
            log_path = os.path.join(log_directory, log_name)
            handler = logging.FileHandler(log_path, mode="a")
            handler.setLevel(level)

            # Create non-colored formatter for file logs
            if hasattr(formatter, "use_colors"):
                file_formatter = copy.copy(formatter)
                setattr(file_formatter, "use_colors", False)
            handler.setFormatter(file_formatter)
            self.addHandler(handler)


def stdout_to_logger(logger: logging.Logger, func: Callable, *args) -> str:
    """
    Redirect stdout to a logger and execute a function. Method can be used when you
    are not sure were given `print()` statements are located in huge codebases, so
    you can wrap any method in this and force logs via your logging system.

    Args:
        logger (logging.Logger): Your own logger to use for logging the stdout output.
        func (Callable): The function to execute with stdout redirection.
        *args: Variable length argument list to pass to the function.

    Returns:
        Any: The return value of the executed function.
    """
    f = StringIO()
    with redirect_stdout(f):
        res = func(*args)

    o = f.getvalue()
    for line in o.splitlines():
        logger.info(line)

    return res
