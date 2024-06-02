from enum import Enum
from questionary import Style
from typing import Callable

import colorama
init(autoreset=True)

class Theme(Enum):
    DARK = 'dark'
    LIGHT = 'light'
    YELLOW = 'yellow'

class ColorName(Enum):
    RED = ('red', 'lightred_ex')
    GREEN = ('green', 'lightgreen_ex')
    YELLOW = ('yellow', 'lightyellow_ex')
    BLUE = ('blue', 'lightblue_ex')
    CYAN = ('cyan', 'lightcyan_ex')
    WHITE = ('white', 'lightwhite_ex')

THEME_STYLES = {
    Theme.DARK: Style.from_dict({
        'question': '#FFFFFF bold',
        'answer': '#FF910A bold',
        'pointer': '#FF4500 bold',
        'highlighted': '#63CD91 bold',
        'instruction': '#FFFF00 bold'
    }),
    Theme.LIGHT: Style.from_dict({
        'question': '#000000 bold',
        'answer': '#FFB74D bold',
        'pointer': '#FF7043 bold',
        'highlighted': '#AED581 bold',
        'instruction': '#757575 bold'
    }),
    Theme.YELLOW: Style.from_dict({
        'question': '#000000 bold',
        'answer': '#FFB74D bold',
        'pointer': '#FF7043 bold',
    })
}

class ThemeStyle:
    def __init__(self, theme: Theme):
        self.theme = theme

    def get_style(self):
        return THEME_STYLES[self.theme]

class StyleConfig:
    def __init__(self, theme: Theme = Theme.DARK):
        self.theme_style = ThemeStyle(theme)
        self.theme = theme

    def get_style(self):
        return self.theme_style.get_style()

    def get_color(self, color_name: ColorName):
        foreground, _ = color_name.value
        return getattr(colorama.Fore, foreground) if self.theme is Theme.DARK else getattr(colorama.Fore, foreground.upper())

    def set_theme(self, theme: Theme):
        self.theme = theme
        self.theme_style.theme = theme

def get_color_function(color_name: ColorName, bold: bool = False):
    color = StyleConfig().get_color(color_name)
    style = colorama.Style.BRIGHT if bold else ""
    reset = colorama.Style.RESET_ALL

    def color_func(text):
        return f'{color}{style}{text}{reset}'

    return color_func

style_config = StyleConfig()

# Dynamically generate color functions
color_red = get_color_function(ColorName.RED)
color_red_bold = get_color_function(ColorName.RED, True)
color_green = get_color_function(ColorName.GREEN)
color_green_bold = get_color_function(ColorName.GREEN, True)
color_yellow = get_color_function(ColorName.YELLOW)
color_yellow_bold = get_color_function(ColorName.YELLOW, True)
color_blue = get_color_function(ColorName.BLUE)
color_blue_bold = get_color_function(ColorName.BLUE, True)
color_cyan = get_color_function(ColorName.CYAN)
color_cyan_bold = get_color_function(ColorName.CYAN, True)
color_white = get_color_function(ColorName.WHITE)
color_white_bold = get_color_function(ColorName.WHITE, True)
