import importlib.util
import tempfile
import unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location('check_site', Path(__file__).resolve().parents[1] / 'tools/check_site.py')
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
BASE = '<html lang="pt-BR"><head><title>Teste</title><meta name="viewport" content="width=device-width"></head><body><h1 id="home">Teste</h1>{}</body></html>'


class SiteChecks(unittest.TestCase):
    def evaluate(self, content):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'index.html').write_text(content, encoding='utf-8')
            return MODULE.check(root)[0]

    def test_valid_page_and_existing_anchor(self):
        self.assertEqual(self.evaluate(BASE.format('<a href="#home">Início</a>')), [])

    def test_missing_asset_is_reported(self):
        self.assertTrue(any('arquivo ausente' in e for e in self.evaluate(BASE.format('<img src="missing.svg">'))))

    def test_missing_anchor_is_reported(self):
        self.assertTrue(any('âncora ausente' in e for e in self.evaluate(BASE.format('<a href="#missing">Ir</a>'))))

    def test_external_link_is_not_requested(self):
        self.assertEqual(self.evaluate(BASE.format('<a href="https://example.invalid">Externo</a>')), [])

    def test_missing_metadata_is_reported(self):
        errors = self.evaluate('<html><body><h1>Teste</h1></body></html>')
        self.assertEqual(len(errors), 3)

    def test_directory_traversal_is_rejected(self):
        self.assertTrue(any('fora da raiz' in e for e in self.evaluate(BASE.format('<a href="../outside">Ir</a>'))))

    def test_directory_index_and_cross_page_anchor(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'links').mkdir()
            (root / 'index.html').write_text(BASE.format('<a href="links/#home">Links</a>'))
            (root / 'links/index.html').write_text(BASE.format(''))
            errors, count = MODULE.check(root)
            self.assertEqual(errors, [])
            self.assertEqual(count, 2)

    def test_github_pages_project_prefix(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'assets').mkdir()
            (root / 'assets/style.css').write_text('body {}')
            (root / '404.html').write_text(BASE.format('<link rel="stylesheet" href="/voltta-system-site/assets/style.css"><a href="/voltta-system-site/">Início</a>'))
            (root / 'index.html').write_text(BASE.format(''))
            self.assertEqual(MODULE.check(root)[0], [])


if __name__ == '__main__':
    unittest.main()
