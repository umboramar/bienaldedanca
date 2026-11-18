#!/usr/bin/env python3
"""Update only the embedded catalogue in the Bienal site; preserve all other views."""
import base64
import hashlib
import io
import json
from pathlib import Path

import fitz
from PIL import Image

PDF = Path('catalogo.pdf')
HTML = Path('index.html')
EXPECTED_SHA = '8af4d9167bb1f9f0369955821171e0ec3ba0314c9b2c677f7972e05cb1bc2894'

def main():
    binary = PDF.read_bytes()
    assert hashlib.sha256(binary).hexdigest() == EXPECTED_SHA, 'PDF mismatch'
    original = HTML.read_text('utf-8')
    assert original.count('id="page-data"') == 1 and "if(id==='catalogo')" in original
    assert '1hFytsu1lK3QkKcZUWrH7uzW41BCECvLa' in original
    doc = fitz.open(stream=binary, filetype='pdf')
    assert len(doc) == 11, f'Wrong page count: {len(doc)}'
    pages = ['<div class="catalog-viewport" aria-label="Catálogo completo da Bienal">']
    for index, page in enumerate(doc):
        pix = page.get_pixmap(matrix=fitz.Matrix(1, 1), colorspace=fitz.csRGB, alpha=False)
        pic = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
        out = io.BytesIO()
        pic.save(out, 'WEBP', quality=82, method=3)
        encoded = base64.b64encode(out.getvalue()).decode('ascii')
        n = index + 1
        loading = 'eager' if n == 1 else 'lazy'
        pages.append(
            f'<section class="catalog-page" data-catalog-page="{n}" aria-label="Catálogo, página {n}">'
            f'<img loading="{loading}" decoding="async" width="{pix.width}" height="{pix.height}" '
            f'alt="Catálogo da X Bienal Internacional de Dança do Ceará — página {n}" '
            f'src="data:image/webp;base64,{encoded}">'
        )
        if n == 11:
            pages.append('<span class="catalog-ficha-anchor" id="catalog-ficha" aria-hidden="true"></span>')
        pages.append('</section>')
        print(f'Page {n}/11: {pix.width}x{pix.height}, {len(out.getvalue())} bytes', flush=True)
        del pix, pic
    pages.append('</div>')
    tag = '<script id="page-data" type="application/json">'
    start = original.index(tag) + len(tag)
    end = original.index('</script>', start)
    raw = original[start:end]
    assert raw.count(',"catalogo":') == 1
    head, sep, tail = raw.rpartition(',"catalogo":')
    assert tail.endswith('}') and 'data-catalog-page="11"' in json.loads(tail[:-1])
    newval = json.dumps(''.join(pages), ensure_ascii=True).replace('<', r'\u003c').replace('>', r'\u003e').replace('&', r'\u0026')
    updated = original[:start] + head + sep + newval + '}' + original[end:]
    parsed = json.loads(updated[start:updated.index('</script>', start)])
    original_parsed = json.loads(raw)
    assert len(parsed) == 7 and parsed['catalogo'].count('class="catalog-page"') == 11
    assert all(parsed[k] == original_parsed[k] for k in parsed if k != 'catalogo')
    assert updated[updated.index('</script>', start):] == original[end:]
    HTML.write_text(updated, 'utf-8')
    print(f'Updated index.html: {len(original)} -> {len(updated)} characters')

if __name__ == '__main__':
    main()
