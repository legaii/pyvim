import curses
import sys

from .app_ui import AppUI
from .key_bindings import key_bindings


def main(window):
    curses.use_default_colors()
    window.clear()
    window.move(0, 0)
    AppUI(window, curses.LINES, curses.COLS - 1, key_bindings).run()


if __name__ == '__main__':
    if len(sys.argv) != 1:
        print('No file provided', file=sys.stderr)
        print('Syntax: pyvim file', file=sys.stderr)
        exit(1)
    curses.wrapper(main)
