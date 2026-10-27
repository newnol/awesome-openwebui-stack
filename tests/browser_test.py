"""Browser regression tests: python -m unittest discover -s tests -p 'browser_test.py'."""
import functools
import json
import os
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import threading
import unittest
from playwright.sync_api import sync_playwright, expect

ROOT = Path(__file__).resolve().parents[1]


class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/project/'):
            self.path = self.path[len('/project'):]
        super().do_GET()

    def log_message(self, *_args):
        pass


class CatalogBrowserTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Handler, directory=str(ROOT)))
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base = f'http://127.0.0.1:{cls.server.server_port}'
        cls.pw = sync_playwright().start()
        cls.browser = cls.pw.chromium.launch(executable_path=os.environ.get('CHROMIUM_EXECUTABLE'))
        (ROOT / 'test-results').mkdir(exist_ok=True)

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.pw.stop()
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def setUp(self):
        self.context = self.browser.new_context(viewport={'width': 1440, 'height': 1000})
        self.page = self.context.new_page()
        self.errors = []
        self.page.on('pageerror', lambda error: self.errors.append(str(error)))

    def tearDown(self):
        self.context.close()
        self.assertEqual(self.errors, [])

    def open(self, suffix='/'):
        self.page.goto(self.base + suffix)
        expect(self.page.locator('#results article')).to_have_count(7)

    def test_desktop_and_mobile(self):
        self.open('/project/')
        self.page.screenshot(path=str(ROOT / 'test-results/desktop.png'), full_page=True)
        self.page.set_viewport_size({'width': 390, 'height': 844})
        self.page.screenshot(path=str(ROOT / 'test-results/mobile.png'), full_page=True)
        self.assertTrue(self.page.evaluate('document.documentElement.scrollWidth <= innerWidth'))
        self.page.locator('#theme').click()
        expect(self.page.locator('html')).to_have_attribute('data-theme', 'dark')
        self.page.screenshot(path=str(ROOT / 'test-results/mobile-dark.png'), full_page=True)
        self.page.reload()
        expect(self.page.locator('html')).to_have_attribute('data-theme', 'dark')

    def test_filters_and_empty_state(self):
        self.open()
        self.page.locator('#q').fill('SHEETPROOF')
        expect(self.page.locator('#results article')).to_have_count(2)
        self.page.locator('#type').select_option('tool')
        expect(self.page.locator('#results article')).to_have_count(1)
        self.page.locator('#q').fill('does-not-exist')
        expect(self.page.locator('#empty')).to_be_visible()
        self.page.locator('#empty-reset').click()
        expect(self.page.locator('#results article')).to_have_count(7)
        self.page.locator('#unavailable').check()
        expect(self.page.locator('#results article')).to_have_count(12)
        self.page.locator('#status').select_option('unavailable')
        expect(self.page.locator('#results article')).to_have_count(5)

    def test_comparison_and_shared_url(self):
        self.open()
        for name in ['LiteLLM', 'Ollama', 'Open Terminal']:
            self.page.get_by_role('checkbox', name=f'Compare {name}', exact=True).check()
        fourth = self.page.get_by_role('checkbox', name='Compare SheetProof', exact=True)
        fourth.click()
        expect(fourth).not_to_be_checked()
        self.assertIn('compare=', self.page.url)
        self.page.reload()
        expect(self.page.locator('#compare-button')).to_have_text('Compare (3/3)')
        self.page.locator('#compare-button').click()
        expect(self.page.get_by_role('dialog')).to_be_visible()
        expect(self.page.locator('#comparison thead th')).to_have_count(4)
        self.page.keyboard.press('Escape')
        expect(self.page.get_by_role('dialog')).not_to_be_visible()
        self.page.locator('#clear-compare').click()
        expect(self.page.locator('#compare-button')).to_be_disabled()

    def test_keyboard_history_and_legacy_route(self):
        self.open()
        self.page.keyboard.press('/')
        expect(self.page.locator('#q')).to_be_focused()
        self.page.locator('#type').select_option('integration')
        self.page.locator('#category').select_option('research')
        expect(self.page.locator('#results article')).to_have_count(1)
        self.page.go_back()
        expect(self.page.locator('#results article')).to_have_count(4)
        self.page.route('**/guide.html', lambda route: route.fulfill(body='<h1>Guide route</h1>', content_type='text/html'))
        self.page.goto(self.base + '/#/catalog/tools')
        self.page.wait_for_url('**/guide.html#/catalog/tools')

    def test_load_failure_has_markdown_fallback(self):
        self.page.route('**/data/catalog.json', lambda route: route.fulfill(status=503, body='Unavailable'))
        self.page.goto(self.base)
        expect(self.page.locator('#load-error')).to_be_visible()
        expect(self.page.locator('#load-error a')).to_have_attribute('href', 'https://github.com/newnol/awesome-openwebui-stack/blob/main/catalog/README.md')

    def test_untrusted_text_is_not_html(self):
        data = json.loads((ROOT / 'data/catalog.json').read_text())
        entry = next(e for e in data if e['id'] == 'ollama')
        entry['name'] = '<img src=x onerror=alert(1)>'
        self.page.route('**/data/catalog.json', lambda route: route.fulfill(json=data))
        self.open()
        expect(self.page.locator('#ollama h3')).to_have_text(entry['name'])
        expect(self.page.locator('#results img')).to_have_count(0)

    def test_no_javascript_fallback(self):
        context = self.browser.new_context(java_script_enabled=False)
        page = context.new_page()
        page.goto(self.base)
        expect(page.locator('noscript a')).to_be_visible()
        context.close()

    def test_blocked_storage_and_malformed_query(self):
        self.context.add_init_script("Object.defineProperty(window, 'localStorage', { get() { throw new Error('blocked'); } });")
        self.open('/?type=invalid&status=__proto__&compare=missing')
        expect(self.page.locator('#compare-button')).to_have_text('Compare (0/3)')
        self.page.locator('#theme').click()
        expect(self.page.locator('html')).to_have_attribute('data-theme', 'dark')


if __name__ == '__main__':
    unittest.main()
