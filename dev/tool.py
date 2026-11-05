#!/usr/bin/env python3
"""Herramienta para editar Mis Hábitos sin romper el empaquetado.

index.html es un "bundle": la app vive como un string JSON dentro de
<script type="__bundler/template">. Este script lo saca a archivos editables y lo vuelve a armar.

  python3 dev/tool.py unpack   -> dev/work/template.html, dev/work/widget.js, dev/work/sync.js
  (editar esos archivos)
  python3 dev/tool.py pack     -> reescribe index.html (verifica JS con node si está instalado)
  python3 dev/tool.py check    -> unpack+pack en memoria y confirma que index.html queda idéntico
"""
import json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX = os.path.join(ROOT, 'index.html')
WORK = os.path.join(ROOT, 'dev', 'work')
TPL_RE = re.compile(r'(<script type="__bundler/template">\s*)(.*?)(\s*</script>)', re.S)
W_START = '<script>\n(function(){\n"use strict";\nif (window.__mePlanBoot)'
S_START = '<script>\n(function(){\n"use strict";\nif (window.__meSyncBoot)'
END = '\n</script>\n'
W_MARK, S_MARK = '<!--@@WIDGET_JS@@-->', '<!--@@SYNC_JS@@-->'

def read_index():
    src = open(INDEX, encoding='utf-8').read()
    m = TPL_RE.search(src)
    if not m: sys.exit('No encuentro el template en index.html')
    return src, m, json.loads(m.group(2))

def split(tpl):
    w0 = tpl.index(W_START); w1 = tpl.index(END, w0)
    s0 = tpl.index(S_START); s1 = tpl.index(END, s0)
    assert w1 < s0, 'orden inesperado de scripts'
    widget = tpl[w0 + len('<script>\n'):w1]
    sync = tpl[s0 + len('<script>\n'):s1]
    base = tpl[:w0] + '<script>\n' + W_MARK + END + tpl[w1 + len(END):s0] + '<script>\n' + S_MARK + END + tpl[s1 + len(END):]
    return base, widget, sync

def join(base, widget, sync):
    assert base.count(W_MARK) == 1 and base.count(S_MARK) == 1, 'faltan los marcadores en template.html'
    return base.replace(W_MARK, widget).replace(S_MARK, sync)

def encode(tpl):
    enc = json.dumps(tpl, ensure_ascii=False).replace('</', '<\\u002F')
    assert json.loads(enc) == tpl
    return enc

def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'check'
    src, m, tpl = read_index()
    if cmd == 'unpack':
        base, widget, sync = split(tpl)
        os.makedirs(WORK, exist_ok=True)
        for name, txt in (('template.html', base), ('widget.js', widget), ('sync.js', sync)):
            open(os.path.join(WORK, name), 'w', encoding='utf-8').write(txt)
        print('Listo: editá dev/work/template.html, widget.js y sync.js; después: python3 dev/tool.py pack')
    elif cmd == 'pack':
        rd = lambda n: open(os.path.join(WORK, n), encoding='utf-8').read()
        widget, sync = rd('widget.js'), rd('sync.js')
        try:
            for n in ('widget.js', 'sync.js'):
                subprocess.run(['node', '--check', os.path.join(WORK, n)], check=True)
        except FileNotFoundError:
            print('(node no está instalado: no verifiqué la sintaxis JS)')
        new = join(rd('template.html'), widget, sync)
        out = src[:m.start(2)] + encode(new) + src[m.end(2):]
        open(INDEX, 'w', encoding='utf-8').write(out)
        print('index.html actualizado (%d bytes)' % len(out))
    elif cmd == 'check':
        base, widget, sync = split(tpl)
        same = src[:m.start(2)] + encode(join(base, widget, sync)) + src[m.end(2):] == src
        print('ida y vuelta idéntica:', same)
        sys.exit(0 if same else 1)
    else:
        sys.exit(__doc__)

if __name__ == '__main__':
    main()
