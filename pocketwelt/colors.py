from enum import Enum
from typing import List, Union


_ANSI_COLORS = {
    "black": 30,
    "red": 31,
    "green": 32,
    "yellow": 33,
    "blue": 34,
    "magenta": 35,
    "cyan": 36,
    "white": 37,
    "reset": 39,
    "bright_black": 90,
    "bright_red": 91,
    "bright_green": 92,
    "bright_yellow": 93,
    "bright_blue": 94,
    "bright_magenta": 95,
    "bright_cyan": 96,
    "bright_white": 97,
}  # source: https://github.com/pallets/click/termui.py

class RGBColor(tuple, Enum):
    RED = (255, 0, 0)
    CRIMSON = (220, 20, 60)
    DEEP_PINK = (255, 20, 147)
    ORANGE_RED = (255, 69, 0)
    ORANGE = (255, 165, 0)
    GREEN = (0, 128, 0)
    LIME = (0, 255, 0)
    TEAL = (0, 128, 128)
    AQUAMARINE = (102, 205, 170)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GOLDEN = (218, 165, 32)
    CYAN = (0, 255, 255)
    YELLOW = (255, 255, 0)

class click:
    """
    This class was made to simulate [`click`](https://github.com/pallets/click)
    package coloring functionality.

    My goal was to keep the package fully built-in, so if you do not have this
    package installed, there will be no problem with using the `style()` method.

    However, if it is installed, do not worry - this class is only used in `logs.ColorFormatter`
    and is imported only when real `click` is not installed.
    """
    @classmethod
    def style(cls, text: str, fg: Union[int, RGBColor, str], **style_kwargs) -> str:
        """
        Style a text with ANSI color codes.

        Args:
            text (str): The text to be styled.
            fg (Union[int, RGBColor, str]): The foreground color. Can be an integer,
                `RGBColor`, or a string representing the color.
            **style_kwargs: Options from the original `click.style` method.

        Returns:
            str: The styled text with ANSI color codes.
        """
        bits: List[str] = [text]
        if isinstance(fg, int):
            bits.insert(0, f"{38};5;{fg:d}")
        elif isinstance(fg, (tuple, list)):
            r, g, b = fg
            bits.insert(0, f"{38};2;{r:d};{g:d};{b:d}")
        else:
            bits.insert(0, str(_ANSI_COLORS[fg]))
            
        return "".join(bits)
    