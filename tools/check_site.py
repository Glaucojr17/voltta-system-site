#!/usr/bin/env python3
"""Check local HTML links/assets and basic page metadata, without network access."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import argparse
import sys


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.refs = []
        self.lang = False
        self.viewport = False
        self.in_title = False
        self.title = ''
        self.h1_count = 0
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get('id'):
            self.ids.add(attrs['id'])
        if tag == 'html':
            self.lang = bool(attrs.get('lang'))
        if tag == 'meta' and attrs.get('name') == 'viewport':
            self.viewport = bool(attrs.get('content'))
        if tag == 'title':
            self.in_title = True
        if tag == 'h1':
            self.h1_count += 1
        for key in ('href', 'src'):
            if attrs.get(key):
                self.refs.append(attrs[key])

    def handle_endtag(self, tag):
        if tag == 'title':
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title += data


def check(root, base_path='/voltta-system-site/'):
    root = Path(root).resolve()
    if not base_path.startswith('/') or not base_path.endswith('/'):
        raise ValueError('base_path deve começar e terminar com /')
    errors = []
    pages = {path.resolve(): Page(path.read_text(encoding='utf-8'))
             for path in root.rglob('*.html')
             if not any(p.startswith('.') or p in ('node_modules', 'tests') for p in path.relative_to(root).parts)}
    if not pages:
        return ['Nenhuma página HTML encontrada.'], 0
    for path, page in pages.items():
        label = str(path.relative_to(root))
        for ok, name in [(page.lang, 'lang'), (page.viewport, 'viewport'), (page.title.strip(), 'title'),
                         (page.h1_count == 1, 'exatamente um h1')]:
            if not ok:
                errors.append(f'{label}: falta {name}')
        for ref in page.refs:
            parts = urlsplit(ref)
            if parts.scheme or parts.netloc:
                continue
            if not parts.path:
                target = path
            elif parts.path.startswith('/'):
                absolute_path = unquote(parts.path)
                if absolute_path.startswith(base_path):
                    absolute_path = absolute_path[len(base_path):]
                target = root / absolute_path.lstrip('/')
            else:
                target = path.parent / unquote(parts.path)
            target = target.resolve()
            if not target.is_relative_to(root):
                errors.append(f'{label}: referência fora da raiz: {ref}')
                continue
            if target.is_dir():
                target = target / 'index.html'
            if not target.is_file():
                errors.append(f'{label}: arquivo ausente: {ref}')
            elif parts.fragment and target.suffix == '.html':
                target_page = pages.get(target)
                if target_page and unquote(parts.fragment) not in target_page.ids:
                    errors.append(f'{label}: âncora ausente: {ref}')
    return errors, len(pages)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', nargs='?', default=Path(__file__).resolve().parents[1], type=Path)
    parser.add_argument('--base-path', default='/voltta-system-site/', help='prefixo usado no GitHub Pages de projeto')
    args = parser.parse_args()
    errors, count = check(args.root, args.base_path)
    if errors:
        print('\n'.join(errors), file=sys.stderr)
        return 1
    print(f'OK: {count} páginas verificadas; referências locais e metadados válidos.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
