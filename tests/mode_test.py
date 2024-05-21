from unittest import TestCase
from src.mode import Mode


class ModeTest(TestCase):
    def test_draw(self):
        self.assertEqual(Mode.normal_mode().draw(), '')
        self.assertEqual(Mode.insert_mode().draw(), '-- INSERT --')
        self.assertEqual(Mode.quit_mode().draw(), '')


    def test_constants(self):
        self.assertEqual(Mode.normal_mode(), Mode(0))
        self.assertEqual(Mode.insert_mode(), Mode(1))
        self.assertEqual(Mode.quit_mode(), Mode(2))
