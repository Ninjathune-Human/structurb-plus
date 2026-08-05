#!/usr/bin/env python3
"""
Injecte le bundle de donnees dans le gabarit et produit l'application autonome.

  src/app.template.html + src/data.js  ->  index.html

index.html n'a aucune dependance : il s'ouvre par double-clic et fonctionne
hors ligne. C'est aussi le fichier servi par GitHub Pages.

Usage : python tools/build.py
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TPL = os.path.join(ROOT, 'src', 'app.template.html')
DATA = os.path.join(ROOT, 'src', 'data.js')
OUT = os.path.join(ROOT, 'index.html')
MARK = '/*__DATA__*/'


def main():
    tpl = open(TPL, encoding='utf-8').read()
    if MARK not in tpl:
        raise SystemExit("Marqueur %s absent du gabarit." % MARK)
    html = tpl.replace(MARK, open(DATA, encoding='utf-8').read())
    open(OUT, 'w', encoding='utf-8').write(html)
    print("index.html : %d Ko" % (len(html.encode('utf-8')) // 1024))


if __name__ == '__main__':
    main()
