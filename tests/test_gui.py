"""Unit tests for desktop GUI workbench module."""

from __future__ import annotations

import unittest
from igprompts.cli import build_parser
from igprompts.gui import THEMES, TK_AVAILABLE, detect_system_theme


class TestGUI(unittest.TestCase):
    def test_gui_subcommand_registered(self):
        parser = build_parser()
        args = parser.parse_args(["gui"])
        self.assertEqual(args.command, "gui")

    def test_tkinter_module_presence(self):
        self.assertIsInstance(TK_AVAILABLE, bool)

    def test_theme_definitions(self):
        self.assertIn("dark", THEMES)
        self.assertIn("light", THEMES)
        required_keys = ["bg", "panel", "fg", "accent", "console_bg"]
        for key in required_keys:
            self.assertIn(key, THEMES["dark"])
            self.assertIn(key, THEMES["light"])

    def test_detect_system_theme_returns_valid_value(self):
        theme = detect_system_theme()
        self.assertIn(theme, ["dark", "light"])


if __name__ == "__main__":
    unittest.main()
