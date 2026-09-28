"""既有用例：覆盖 `fold` 已经可用的那一层（小写化 + 去首尾空白）。

这些断言是**冻结**的基线，一条都不许删或改。
"""

import unittest

from textfold import fold


class LowercaseTests(unittest.TestCase):
    def test_ascii_lower(self):
        self.assertEqual(fold("Hello"), "hello")

    def test_mixed_case(self):
        self.assertEqual(fold("MiXeD CaSe"), "mixed case")

    def test_already_lower(self):
        self.assertEqual(fold("already"), "already")

    def test_digits_and_punctuation(self):
        self.assertEqual(fold("Item-1!"), "item-1!")


class StripTests(unittest.TestCase):
    def test_strip_spaces(self):
        self.assertEqual(fold("  hi  "), "hi")

    def test_strip_tabs_and_newlines(self):
        self.assertEqual(fold("\t\nhi\n\t"), "hi")

    def test_strip_then_lower(self):
        self.assertEqual(fold("  HeLLo  "), "hello")

    def test_internal_space_kept(self):
        self.assertEqual(fold("  a b  "), "a b")


class BoundaryTests(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(fold(""), "")

    def test_only_whitespace(self):
        self.assertEqual(fold("   \t\n "), "")

    def test_cjk_passthrough(self):
        self.assertEqual(fold("中文字"), "中文字")

    def test_emoji_passthrough(self):
        self.assertEqual(fold("ok🌊"), "ok🌊")


if __name__ == "__main__":
    unittest.main()
