from unittest import TestCase
from unittest.mock import MagicMock
from curses import A_BOLD
from src.app_ui import AppUI


class AppUITest(TestCase):
    def test_app_ui(self):
        key_binding1 = MagicMock()
        key_binding1.check.return_value = False
        key_binding2 = MagicMock()
        key_binding2.check.return_value = True
        key_binding3 = MagicMock()
        key_binding3.check.return_value = True

        app_ui = AppUI(MagicMock(), 4, 5, '', [key_binding1, key_binding2, key_binding3])
        app_ui.window.getkey.return_value = 'a'
        app_ui.state = MagicMock()
        app_ui.state.mode.__ne__.side_effect=[True, False]
        app_ui.state.mode.draw.return_value = 'b'
        app_ui.run()
        app_ui.state.buffer.draw.assert_called_once_with(app_ui.window, 3, 5)
        app_ui.window.addstr.assert_called_once_with(3, 0, '    b', A_BOLD)
