"""Compose editable slide sources into an offline HTML deck; serve live previews."""
import argparse
import base64
import html
import json
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'src'
DIST = ROOT / 'dist'


def render():
    config = json.loads((SRC / 'deck.json').read_text())
    slides = []
    for index, filename in enumerate(config['slides'], 1):
        slide = (SRC / 'slides' / filename).read_text()
        slide = slide.replace('<span data-slide-number></span>',
                              f'<span data-slide-number>{index:02} / {len(config["slides"]):02}</span>')
        slides.append(slide)
    css = (SRC / 'styles/deck.css').read_text()

    def embed_font(match):
        asset = (SRC / 'styles' / match[1]).resolve()
        data = base64.b64encode(asset.read_bytes()).decode()
        return f'url(data:font/ttf;base64,{data})'

    css = re.sub(r'url\([\"\']?([^\)\"\']+\.ttf)[\"\']?\)', embed_font, css)
    scripts = '\n'.join((SRC / 'scripts' / filename).read_text()
                        for filename in ['editor.js', 'presentation.js'])
    result = (SRC / 'index.html').read_text()
    for key, value in {'TITLE': html.escape(config['title']), 'SLIDES': '\n'.join(slides),
                       'STYLES': f'<style>\n{css}</style>',
                       'SCRIPTS': f'<script>\n{scripts}</script>'}.items():
        result = result.replace('{{' + key + '}}', value)
    return result


def build():
    DIST.mkdir(exist_ok=True)
    target = DIST / 'index.html'
    target.write_text(render())
    return target


class PreviewHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.split('?', 1)[0] in ['/', '/index.html']:
            try:
                content = render().encode()
            except Exception as error:
                self.send_error(500, str(error))
                return
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Cache-Control', 'no-store')
            self.end_headers()
            self.wfile.write(content)
        else:
            super().do_GET()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['build', 'dev'])
    parser.add_argument('--port', type=int, default=8000)
    args = parser.parse_args()
    if args.command == 'build':
        print(build().relative_to(ROOT))
    else:
        server = ThreadingHTTPServer(('127.0.0.1', args.port),
                                     partial(PreviewHandler, directory=str(SRC)))
        print(f'Preview: http://localhost:{args.port} — save sources and refresh.', flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            server.server_close()


if __name__ == '__main__':
    main()
