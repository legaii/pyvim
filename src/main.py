import curses
import sys

from .app_ui import AppUI
from .key_bindings import key_bindings


def main(window: curses.window):
    """Функция, настраивающая базовые параметры curses.window и передающая управление окном AppUI"""
    curses.use_default_colors()
    window.keypad(True)
    window.clear()
    window.move(0, 0)
    AppUI(window, curses.LINES, curses.COLS - 1, sys.argv[1], key_bindings).run()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('No file provided', file=sys.stderr)
        print('Syntax: python3 -m src.main FILE', file=sys.stderr)
        exit(1)
    curses.wrapper(main)
