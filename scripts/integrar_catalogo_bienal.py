#!/usr/bin/env python3
"""Integra a pagina de catalogo ao HTML existente, preservando todas as pranchas."""
from pathlib import Path
import json

PDF_ID = '1Tdqje4TkPe0elWxxHsoxrh1Z2JhCafNM'
PDF_PREVIEW = f'https://drive.google.com/file/d/{PDF_ID}/preview'
PDF_DOWNLOAD = f'https://drive.google.com/uc?export=download&id={PDF_ID}'
PDF_VIEW = f'https://drive.google.com/file/d/{PDF_ID}/view'

STYLE = r'''
/* Catálogo 2026: nova seção visual no mesmo HTML da Bienal */
.catalogo-page{min-height:100vh;background:#000;color:#fff;line-height:1.4}
.catalogo-header{display:flex;align-items:flex-start;justify-content:space-between;flex-wrap:wrap;gap:24px;padding:42px clamp(20px,5vw,86px);border-bottom:1px solid #343434}
.catalogo-brand{color:#ff5708;text-decoration:none;font-size:clamp(15px,1.1vw,21px);font-weight:800;line-height:1.05;letter-spacing:-.04em}
.catalogo-nav{display:flex;flex-wrap:wrap;gap:12px clamp(12px,1.5vw,27px);align-items:center}
.catalogo-nav a{color:#fff;text-decoration:none;text-transform:uppercase;font-size:clamp(11px,.75vw,14px);font-weight:700;letter-spacing:.01em}
.catalogo-nav a:hover,.catalogo-nav a:focus-visible,.catalogo-nav [aria-current="page"]{color:#ff5708}
.catalogo-inner{padding:clamp(32px,5vw,88px) clamp(20px,5vw,86px) 90px}
.catalogo-eyebrow{margin:0 0 18px;font-size:clamp(13px,1vw,19px);text-transform:uppercase;letter-spacing:.12em;color:#eee}
.catalogo-title{font-family:Arial,Helvetica,sans-serif;font-weight:800;font-stretch:condensed;text-transform:uppercase;color:#ff5708;font-size:clamp(56px,10.7vw,205px);letter-spacing:-.09em;line-height:.95;margin:0 0 28px}
.catalogo-actions{display:flex;align-items:center;gap:18px 28px;flex-wrap:wrap;margin:0 0 42px}
.catalogo-download{display:inline-flex;align-items:center;gap:22px;padding:18px 23px;color:#000!important;background:#ff5708;border:2px solid #ff5708;text-decoration:none;text-transform:uppercase;font-size:clamp(13px,1vw,17px);font-weight:800;letter-spacing:.01em;transition:background .18s,color .18s}
.catalogo-download:hover,.catalogo-download:focus-visible{color:#ff5708!important;background:transparent}
.catalogo-download-arrow{font-size:27px;line-height:.5;font-weight:400}
.catalogo-meta{font-size:14px;text-transform:uppercase;letter-spacing:.08em;color:#b9b9b9}
.catalogo-reader{width:100%;background:#161616;border:1px solid #484848;position:relative}
.catalogo-reader iframe{display:block;width:100%;height:75vh;min-height:550px;border:0;background:#fff}
.catalogo-below{display:flex;justify-content:space-between;gap:12px 24px;flex-wrap:wrap;padding:19px 0 0;font-size:13px;color:#bcbcbc}
.catalogo-below a,.catalogo-footer a{color:#ff5708;text-decoration:underline;text-underline-offset:4px;font-weight:700}
.catalogo-footer{padding:28px clamp(20px,5vw,86px);border-top:1px solid #343434;color:#bbb;font-size:12px;display:flex;justify-content:space-between;align-items:center;gap:16px;flex-wrap:wrap}
@media(max-width:800px){.catalogo-header{padding:22px 20px;gap:18px}.catalogo-nav{gap:12px 18px}.catalogo-inner{padding:38px 20px 58px}.catalogo-title{font-size:clamp(51px,12vw,90px);letter-spacing:-.065em}.catalogo-reader iframe{height:66vh;min-height:410px}.catalogo-meta{font-size:11px}.catalogo-download{padding:16px 20px}}
@media(max-width:430px){.catalogo-nav{gap:10px 16px}.catalogo-nav a{font-size:10px}.catalogo-title{font-size:clamp(47px,12vw,60px)}.catalogo-download{width:100%;justify-content:space-between}.catalogo-reader iframe{min-height:350px;height:62vh}}
'''

MARKUP = f'''
<section class="catalogo-page" aria-labelledby="titulo-catalogo">
  <header class="catalogo-header">
    <a class="catalogo-brand" href="#inicio" aria-label="Voltar à página inicial da Bienal">X BIENAL<br>INTERNACIONAL<br>DE DANÇA DO CEARÁ</a>
    <nav class="catalogo-nav" aria-label="Navegação da Bienal">
      <a href="#a-bienal">A BIENAL</a>
      <a href="#programacao">PROGRAMAÇÃO</a>
      <a href="#formacoes">FORMAÇÕES</a>
      <a href="#catalogo" aria-current="page">CATÁLOGO</a>
      <a href="#a-casa-movimenta">A CASA MOVIMENTA</a>
      <a href="#informacoes">INFORMAÇÕES</a>
    </nav>
  </header>
  <div class="catalogo-inner">
    <p class="catalogo-eyebrow">DE PAR EM PAR · 2026</p>
    <h1 class="catalogo-title" id="titulo-catalogo">CATÁLOGO</h1>
    <div class="catalogo-actions">
      <a class="catalogo-download" href="{PDF_DOWNLOAD.replace('&', '&amp;')}" target="_blank" rel="noopener noreferrer" aria-label="Baixar o catálogo da Bienal em PDF">BAIXAR CATÁLOGO (PDF) <span class="catalogo-download-arrow" aria-hidden="true">↓</span></a>
      <span class="catalogo-meta">EDIÇÃO 2026 · PDF COMPLETO</span>
    </div>
    <div class="catalogo-reader">
      <iframe src="{PDF_PREVIEW}" title="Leitura do catálogo 2026 da X Bienal Internacional de Dança do Ceará" loading="eager" allow="fullscreen"></iframe>
    </div>
    <div class="catalogo-below">
      <span>Leia o catálogo acima ou baixe a publicação completa.</span>
      <a href="{PDF_VIEW}" target="_blank" rel="noopener noreferrer">ABRIR PDF EM NOVA ABA ↗</a>
    </div>
  </div>
  <footer class="catalogo-footer"><span>X BIENAL INTERNACIONAL DE DANÇA DO CEARÁ · DE PAR EM PAR</span><a href="#inicio">VOLTAR AO INÍCIO ↑</a></footer>
</section>
'''


def integrate(text: str) -> str:
    if "id=\"titulo-catalogo\"" in text or "views.catalogo=" in text:
        print('Catálogo já integrado: nenhuma modificação necessária')
        return text
    assert text.count('</style>') == 1, 'Não achei o fim do CSS original'
    assert text.count("const views=JSON.parse($('#page-data').textContent);") == 1, 'Estrutura de páginas inesperada'
    assert text.count("'informacoes':'Informações'};") == 1, 'Mapa de títulos inesperado'
    assert text.count("function enhance(root,id){const sv=") == 1, 'Estrutura de navegação inesperada'
    assert text.count("openExternal('catalogo')") == 3, 'Foram encontrados acessos diferentes ao catálogo'

    text = text.replace('</style>', STYLE + '\n</style>', 1)
    init = "const views=JSON.parse($('#page-data').textContent);"
    text = text.replace(init, init + '\nviews.catalogo=' + json.dumps(MARKUP,ensure_ascii=False) + ';', 1)
    text = text.replace("'informacoes':'Informações'};", "'informacoes':'Informações','catalogo':'Catálogo'};", 1)
    text = text.replace("function enhance(root,id){const sv=", "function enhance(root,id){if(id==='catalogo')return;const sv=", 1)
    text = text.replace("openExternal('catalogo')", "go('catalogo')")
    before = "['A Bienal — História e manifesto','a-bienal'],"
    if before in text:
        text = text.replace(before,"['Catálogo 2026 — PDF','catalogo']," + before, 1)
    assert "views.catalogo=" in text
    assert "go('catalogo')" in text
    assert "https://drive.google.com/file/d/"+PDF_ID+"/preview" in text
    return text


if __name__ == '__main__':
    p = Path('index.html')
    original = p.read_text(encoding='utf-8')
    modified = integrate(original)
    if original != modified:
        p.write_text(modified,encoding='utf-8')
        print('Catálogo integrado ao index.html. Tamanho:',len(modified),'caracteres')
