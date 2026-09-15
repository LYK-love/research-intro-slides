"""Browser-level regression checks, using unittest as the test runner."""
from pathlib import Path
import tempfile
import unittest
from playwright.sync_api import sync_playwright

DECK = Path(__file__).resolve().parents[1] / 'src' / 'index.html'


class PresentationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch()

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.playwright.stop()

    def setUp(self):
        self.context = self.browser.new_context(viewport={'width': 1280, 'height': 720})
        self.page = self.context.new_page()
        self.errors = []
        self.page.on('pageerror', lambda error: self.errors.append(str(error)))
        self.page.goto(DECK.as_uri())
        self.page.evaluate('document.fonts.ready')

    def tearDown(self):
        self.context.close()
        self.assertEqual(self.errors, [])

    def test_keyboard_navigation_and_bounds(self):
        self.assertEqual(self.page.locator('.slide').count(), 6)
        for key, expected in [('ArrowRight', 1), ('Space', 2), ('Home', 0),
                              ('ArrowLeft', 0), ('End', 5), ('PageDown', 5),
                              ('PageUp', 4)]:
            self.page.keyboard.press(key)
            self.assertEqual(self.page.evaluate('presentation.currentSlide'), expected)
            self.assertEqual(self.page.locator('.slide:not([inert])').count(), 1)

    def test_offline_layout_on_desktop_and_phone(self):
        self.context.set_offline(True)
        self.page.reload()
        self.page.evaluate('document.fonts.ready')
        self.assertTrue(self.page.evaluate("document.fonts.check('200 40px Jost')"))
        for width, height in [(1280, 720), (390, 844)]:
            self.page.set_viewport_size({'width': width, 'height': height})
            for i in range(6):
                self.page.evaluate('(i) => presentation.showSlide(i)', i)
                rect = self.page.locator('.deck-stage').bounding_box()
                self.assertAlmostEqual(rect['width'] / rect['height'], 16 / 9, places=3)
                bad = self.page.evaluate('''() => {
                    const slide = document.querySelector('.slide.active');
                    const bounds = slide.getBoundingClientRect();
                    return [...slide.querySelectorAll('[data-edit]')].filter(el => {
                        const r = el.getBoundingClientRect();
                        return r.left < bounds.left - 1 || r.right > bounds.right + 1 ||
                            r.bottom > bounds.bottom + 1 ||
                            (getComputedStyle(el).display !== 'inline' &&
                             el.scrollWidth > el.clientWidth + 2);
                    }).map(el => el.textContent);
                }''')
                self.assertEqual(bad, [])

    def test_edit_persistence_and_portable_export(self):
        self.page.keyboard.press('e')
        text = self.page.locator('.slide.active [data-edit]').first
        text.fill('Edited title')
        self.page.reload()
        self.assertEqual(text.inner_text(), 'Edited title')
        with self.page.expect_download() as download:
            self.page.keyboard.press('Control+s')
        with tempfile.TemporaryDirectory() as tmp:
            exported = Path(tmp) / 'export.html'
            download.value.save_as(exported)
            self.page.goto(exported.as_uri())
            self.assertEqual(self.page.locator('.slide.active [data-edit]').first.inner_text(), 'Edited title')
            self.assertFalse(self.page.locator('body').evaluate("el => el.classList.contains('editing')"))
            self.page.keyboard.press('ArrowRight')
            self.assertEqual(self.page.evaluate('presentation.currentSlide'), 1)


if __name__ == '__main__':
    unittest.main()
