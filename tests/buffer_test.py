from unittest import TestCase
from unittest.mock import MagicMock, call
from tempfile import NamedTemporaryFile
from src.buffer import Buffer


class BufferTest(TestCase):
    def setUp(self):
        self.buffer = Buffer()
        self.buffer.content = [' a_a   !3a_', 'a_aba,', ' word1  word2   word3    ']


    def test_read_write(self):
        tmp_file = NamedTemporaryFile()
        with open(tmp_file.name, 'w') as file:
            file.write(' a b c \ncba\n')

        self.buffer.read_from('abacaba')
        self.buffer.read_from(tmp_file.name)
        self.buffer.write_to(tmp_file.name)
        self.assertEqual(self.buffer.content, [' a b c ', 'cba', ''])

        with open(tmp_file.name, 'r') as file:
            self.assertEqual(file.read(), ' a b c \ncba\n')


    def test_moving(self):
        get_pos = lambda: (self.buffer.current_line, self.buffer.current_char)
        self.assertEqual(get_pos(), (0, 0))
        self.buffer.move_line(-10)
        self.assertEqual(get_pos(), (0, 0))
        self.buffer.move_line(10)
        self.assertEqual(get_pos(), (2, len(self.buffer.content[-1])))
        self.buffer.move_line(-1)
        self.assertEqual(get_pos(), (1, 6))
        self.buffer.move_line(-1)
        self.assertEqual(get_pos(), (0, 6))
        self.buffer.move_char(-5)
        self.assertEqual(get_pos(), (0, 1))
        self.buffer.move_char(-5)
        self.assertEqual(get_pos(), (0, 0))

        self.buffer.go_to_next_word()
        self.assertEqual(get_pos(), (0, 1))
        self.buffer.go_to_next_word()
        self.assertEqual(get_pos(), (0, 7))
        self.buffer.go_to_next_word()
        self.assertEqual(get_pos(), (1, 0))
        self.buffer.go_to_next_word()
        self.assertEqual(get_pos(), (2, 1))

        for _ in range(10):
            self.buffer.go_to_next_word()
        self.assertEqual(get_pos(), (2, len(self.buffer.content[-1])))

        self.buffer.go_to_prev_word()
        self.buffer.go_to_prev_word()
        self.buffer.go_to_prev_word()
        self.assertEqual(get_pos(), (2, 5))
        self.buffer.go_to_prev_word()
        self.assertEqual(get_pos(), (1, 5))
        self.buffer.go_to_next_word()
        self.assertEqual(get_pos(), (2, 1))

        for _ in range(10):
            self.buffer.go_to_prev_word()
        self.assertEqual(get_pos(), (0, 0))

        self.buffer.go_to_line_end()
        self.assertEqual(get_pos(), (0, len(self.buffer.content[0])))
        self.buffer.go_to_next_word()
        self.assertEqual(get_pos(), (1, 0))
        self.buffer.go_to_line_begin()
        self.assertEqual(get_pos(), (1, 0))
        self.buffer.go_to_prev_word()
        self.buffer.go_to_line_begin()
        self.assertEqual(get_pos(), (0, 0))


    def test_insert(self):
        self.buffer.insert('a')
        self.assertTrue(self.buffer.content[0].startswith('a a_a'))
        self.buffer.insert_new_line()
        self.assertTrue(self.buffer.content[1].startswith(' a_a'))
        self.buffer.go_to_prev_word()
        self.buffer.go_to_prev_word()
        self.assertEqual(self.buffer.content[0][self.buffer.current_char], 'a')


    def test_delete(self):
        self.buffer.move_char(1)
        self.buffer.delete_char()
        self.assertTrue(self.buffer.content[0].startswith('a_a'))
        self.buffer.move_line(1)
        self.buffer.delete_char()
        self.assertEqual(len(self.buffer.content), 2)
        self.assertEqual(self.buffer.content[0][-1], ',')

        self.buffer.delete_word()
        self.assertEqual(self.buffer.content[0], 'a_a   ')
        self.assertEqual(self.buffer.current_char, 6)
        self.buffer.delete_word()
        self.assertEqual(self.buffer.content[0], 'a_a   ')
        self.assertEqual(self.buffer.current_char, 6)
        self.buffer.go_to_prev_word()
        self.buffer.delete_word()
        self.assertEqual(self.buffer.content[0], '')
        self.assertEqual(self.buffer.current_char, 0)

        self.buffer.delete_line()
        self.assertEqual(len(self.buffer.content), 1)
        self.assertTrue(self.buffer.content[0].startswith(' word1'))
        self.buffer.delete_line()
        self.assertEqual(len(self.buffer.content), 1)
        self.assertEqual(self.buffer.content[0], '')


    def test_search(self):
        get_pos = lambda: (self.buffer.current_line, self.buffer.current_char)
        self.buffer.next_occurrence('a_a')
        self.assertEqual(get_pos(), (0, 1))
        self.buffer.next_occurrence('a_a')
        self.assertEqual(get_pos(), (1, 0))
        self.buffer.next_occurrence('a_a')
        self.assertEqual(get_pos(), (0, 1))


    def test_draw(self):
        self.buffer.content.insert(1, '')
        window_mock = MagicMock()
        self.buffer.draw(window_mock, 8, 3)
        window_mock.addstr.assert_has_calls([
            call(0, 0, ' a_'),
            call(1, 0, 'a  '),
            call(2, 0, ' !3'),
            call(3, 0, 'a_ '),
            call(4, 0, '   '),
            call(5, 0, 'a_a'),
            call(6, 0, 'ba,'),
            call(7, 0, ' wo'),
        ])
