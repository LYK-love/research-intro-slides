"""Checks for source composition independent of the browser."""
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import deck


class BuildTests(unittest.TestCase):
    def test_offline_asset_embedding(self):
        result = deck.render()
        self.assertNotIn('{{', result)
        self.assertEqual(result.count('data:font/ttf;base64,'), 4)
        self.assertNotIn('../assets/fonts/', result)
        self.assertIn('class InlineEditor', result)
        self.assertIn('class SlidePresentation', result)

    def test_manifest_controls_order_and_numbering(self):
        # A tiny isolated source tree verifies additions/removals without changing real slides.
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp)
            for directory in ['slides', 'styles', 'scripts']:
                (source / directory).mkdir()
            (source / 'deck.json').write_text(json.dumps({
                'title': 'A & B', 'slides': ['second.html', 'first.html']}))
            (source / 'index.html').write_text('{{TITLE}}{{STYLES}}{{SLIDES}}{{SCRIPTS}}')
            for name in ['first', 'second']:
                (source / 'slides' / f'{name}.html').write_text(
                    f'{name}<span data-slide-number></span>')
            (source / 'styles/deck.css').write_text('')
            for name in ['editor', 'presentation']:
                (source / 'scripts' / f'{name}.js').write_text('')
            with patch.object(deck, 'SRC', source):
                result = deck.render()
            self.assertIn('A &amp; B', result)
            self.assertLess(result.index('second'), result.index('first'))
            self.assertIn('01 / 02', result)
            self.assertIn('02 / 02', result)
