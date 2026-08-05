#!/usr/bin/env python3
"""
Assemble le bundle de donnees consomme par l'application.

Entrees  : build/certu.json          (sortie de tools/extract_certu.py)
           data/base-carbone.json    (facteurs d'emission, editable)
           vendor/structurb/ModuleMain.bas  (stations meteo de reference)
Sortie   : src/data.js

Usage : python tools/build_data.py
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CERTU = os.path.join(ROOT, 'build', 'certu.json')
CARBONE = os.path.join(ROOT, 'data', 'base-carbone.json')
BAS = os.path.join(ROOT, 'vendor', 'structurb', 'ModuleMain.bas')
OUT = os.path.join(ROOT, 'src', 'data.js')


def f(x):
    x = round(float(x), 4)
    return int(x) if x == int(x) else x


def stations():
    """RemplirLesStationsMeteo : 84 stations codees en dur dans le source VB."""
    txt = open(BAS, encoding='cp1252').read()
    rows = re.findall(
        r'RemplirUneStation\w+ uneForm, "([^"]+)", "?(\d+)"?, (-?\d+), (-?\d+), (-?\d+), (-?\d+)',
        txt)
    if len(rows) != 84:
        print("attention : %d stations extraites au lieu de 84" % len(rows), file=sys.stderr)
    return [{'nom': n, 'dpt': d, 'alt': int(a), 'HRE': int(e), 'HRNE': int(ne), 'HC': int(c)}
            for n, d, a, e, ne, c in rows]


def main():
    certu = json.load(open(CERTU, encoding='utf-8'))
    carb = json.load(open(CARBONE, encoding='utf-8'))

    # --- structures : lignes d'epaisseurs compactees "epS,eb1,eb2,ef1,ef2,qm,minTec,maxPra"
    structs = []
    for s in certu['structures']:
        tabs = []
        for t in s['tabs']:
            tabs.append(";".join(
                "%d,%d,%d,%d,%d,%s,%d,%d" % (
                    r[0], r[1], r[2], r[3], r[4], f(r[5]),
                    1 if r[6].strip().lower() == 'oui' else 0,
                    1 if r[7].strip().lower() == 'oui' else 0)
                for r in t))
        structs.append({
            'i': s['index'], 'n': s['abrege'].strip(),
            's': s['couSurf'].strip(), 'b': s['couBase'].strip(), 'f': s['couFond'].strip(),
            'se': s['surfSansEp'], 'ts': s['typeStructure'], 'tc': s['typeChaussee'],
            'cam': s['typeCAM'], 'r': s['tauxRisque'],
            'ne': [s['neMin'], s['neMax']],
            'v': [s['vDes'], s['vDis'], s['vPL'], s['vBus'],
                  s['vParking'], s['gDis'], s['gPL']],
            't': tabs})

    # --- materiaux de base et de fondation
    matbf = {m['abrege'].strip(): {
        'nom': m['nom'].strip(), 'E': f(m['young']), 'nu': f(m['poisson']),
        'eps': f(m['epsilon']), 'sig': f(m['sigma']),
        'a': f(m['aGel']), 'b': f(m['bGel']), 'q': m['qual'].strip()}
        for m in certu['materiaux']}

    # --- materiaux de surface ; " Enrobés " (giratoires) est stocke sous "Enrobés*"
    matsurf = {}
    for m in certu['matsurf']:
        k = m['abrege'].strip()
        e = {'nom': m['nom'].strip(), 'a': f(m['aGel']), 'b': f(m['bGel'])}
        if m['type'] == 'MatériauComposé':
            e['comp'] = [[c[0]] + [[c[i][0], c[i][1].strip()] for i in (1, 2, 3) if c[i][0] > 0]
                         for c in m['compositions']]
        else:
            e['E'] = f(m.get('young', 0))
        if m['abrege'] == ' Enrobés ':
            k = 'Enrobés*'
        matsurf[k] = e

    data = {
        'structures': structs,
        'matbf': matbf,
        'matsurf': matsurf,
        'stations': stations(),
        'carbone': carb['produits'],
        'deblais': carb['deblais'],
        'pfco2': carb['plateforme_kgco2_m2'],
        'map': carb['correspondances'],
    }

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    js = "const D=" + json.dumps(data, ensure_ascii=False, separators=(',', ':')) + ";"
    open(OUT, 'w', encoding='utf-8').write(js)
    print("src/data.js : %d structures, %d produits, %d Ko"
          % (len(structs), len(carb['produits']), len(js) // 1024))


if __name__ == '__main__':
    main()
