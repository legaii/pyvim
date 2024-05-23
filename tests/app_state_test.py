from unittest import TestCase
from unittest.mock import MagicMock
from src.app_state import AppState


class AppStateTest(TestCase):
    def test_read_write(self):
        app_state = AppState('a')
        app_state.buffer = MagicMock()
        app_state.read()
        app_state.write()
        app_state.buffer.read_from.assert_called_once_with('a')
        app_state.buffer.write_to.assert_called_once_with('a')
