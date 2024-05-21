from unittest import TestCase
from unittest.mock import MagicMock
from src.key_bindings import key_bindings, ESCAPE
from src.mode import Mode


class KeyBindingsTest(TestCase):
    def setUp(self):
        self.app_state = MagicMock()
        self.app_state.mode = Mode.normal_mode()


    def check_all(self, string):
        for key_binding in key_bindings:
            if key_binding.check(string, self.app_state):
                break


    def test_switch_to_insert_mode(self):
        self.check_all('i')
        self.assertEqual(self.app_state.mode, Mode.insert_mode())


    def test_next_line(self):
        self.check_all('j')
        self.app_state.buffer.move_line.assert_called_once_with(1)


    def test_prev_line(self):
        self.check_all('k')
        self.app_state.buffer.move_line.assert_called_once_with(-1)


    def test_next_word(self):
        self.check_all('w')
        self.app_state.buffer.go_to_next_word.assert_called_once_with()


    def test_prev_word(self):
        self.check_all('b')
        self.app_state.buffer.go_to_prev_word.assert_called_once_with()


    def test_next_char(self):
        self.check_all('l')
        self.app_state.buffer.move_char.assert_called_once_with(1)


    def test_prev_char(self):
        self.check_all('h')
        self.app_state.buffer.move_char.assert_called_once_with(-1)


    def test_line_begin(self):
        self.check_all('0')
        self.app_state.buffer.go_to_line_begin.assert_called_once_with()


    def test_line_end(self):
        self.check_all('$')
        self.app_state.buffer.go_to_line_end.assert_called_once_with()


    def test_delete_line(self):
        self.check_all('dd')
        self.app_state.buffer.delete_line.assert_called_once_with()


    def test_delete_word(self):
        self.check_all('daw')
        self.app_state.buffer.delete_word.assert_called_once_with()


    def test_delete_char(self):
        self.check_all('i')
        self.check_all('\b')
        self.app_state.buffer.delete_char.assert_called_once_with()


    def test_search(self):
        self.check_all('/aba\n')
        self.assertEqual(self.app_state.search_string, 'aba')
        self.app_state.buffer.next_occurrence.assert_called_once_with('aba')
        self.app_state.buffer.next_occurrence.reset_mock()
        self.check_all('n')
        self.app_state.buffer.next_occurrence.assert_called_once_with('aba')


    def test_quit(self):
        self.check_all(':q\n')
        self.assertEqual(self.app_state.mode, Mode.quit_mode())


    def test_read_write(self):
        self.check_all(':e aba\n')
        self.assertEqual(self.app_state.file, 'aba')
        self.app_state.read.assert_called_once_with()
        self.check_all(':w c\n')
        self.assertEqual(self.app_state.file, 'c')
        self.app_state.write.assert_called_once_with()


    def test_cancel(self):
        self.check_all('i')
        self.assertEqual(self.app_state.mode, Mode.insert_mode())
        self.check_all(ESCAPE)
        self.check_all('a' + ESCAPE)
        self.assertEqual(self.app_state.mode, Mode.normal_mode())


    def test_insert(self):
        self.check_all('i')
        self.check_all('i')
        self.app_state.buffer.insert.assert_called_once_with('i')
        self.check_all('\n')
        self.app_state.buffer.insert_new_line.assert_called_once_with()
