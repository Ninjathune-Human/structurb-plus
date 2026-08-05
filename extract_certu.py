#!/usr/bin/env python3
"""
Extraction des donnees binaires du logiciel Struct-Urb (CERTU / Cerema).

Lit Certu.str (catalogue des structures types + materiaux de base/fondation)
et Certu.mts (materiaux de couche de surface) et produit un JSON exploitable.

Format des fichiers : ecriture binaire VB6.
  - chaines  : Long (4 o) de longueur + octets CP1252
  - Integer  : 2 o signes    - Long : 4 o signes
  - Single   : 4 o IEEE754   - Byte : 1 o

Usage :  python tools/extract_certu.py vendor/structurb --out build/certu.json
"""
import argparse, json, os, struct

FIN_COMMENT = "###Fin commentaire###"


class Reader:
    def __init__(self, data):
        self.d, self.p = data, 0

    def raw(self, n):
        b = self.d[self.p:self.p + n]
        self.p += n
        return b

    def long(self):   return struct.unpack('<i', self.raw(4))[0]
    def int(self):    return struct.unpack('<h', self.raw(2))[0]
    def byte(self):   return struct.unpack('<B', self.raw(1))[0]
    def single(self): return struct.unpack('<f', self.raw(4))[0]

    def str(self):
        return self.raw(self.long()).decode('cp1252')

    def comment(self):
        """Le commentaire RTF est fragmente sur plusieurs chaines."""
        c = self.str()
        while True:
            nxt = self.str()
            if nxt == FIN_COMMENT:
                return c
            c += nxt

    def eof(self):
        return self.p >= len(self.d)


def parse_str(path):
    """Catalogue des structures. Voir ModuleMain.bas:OuvrirFichierStructures."""
    r = Reader(open(path, 'rb').read())
    entete = r.str()
    if not entete.startswith("Fichier de structures"):
        raise SystemExit("En-tete inattendu : %r" % entete)

    structures, materiaux = [], []
    while not r.eof():
        t = r.str()
        if t == "Structure":
            s = {
                'index': r.int(), 'abrege': r.str(),
                'couSurf': r.str(), 'couBase': r.str(), 'couFond': r.str(),
                'surfSansEp': r.int(), 'saisieComplete': r.int(),
                'vDes': r.int(), 'vDis': r.int(), 'vPL': r.int(), 'vBus': r.int(),
                'vParking': r.int(), 'gDis': r.int(), 'gPL': r.int(),
                'typeChaussee': r.byte(),
                'tauxRisque': r.int(), 'typeCAM': r.int(),
                'typeStructure': r.byte(),
                'neMin': r.long(), 'neMax': r.long(),
            }
            s['comment'] = r.comment()
            # 8 tableaux : PF1Q1 PF1Q2 PF2Q1 PF2Q2 PF2+Q1 PF2+Q2 PF3Q1 PF3Q2
            # 8 colonnes par ligne (Utilitaires.bas:DonnerColPF)
            tabs = []
            for _ in range(8):
                n = r.long()
                rows = []
                for _ in range(n // 8):
                    rows.append([r.int(), r.int(), r.int(), r.int(), r.int(),
                                 round(r.single(), 4), r.str(), r.str()])
                tabs.append(rows)
            s['tabs'] = tabs
            structures.append(s)

        elif t == "MatériauFondBase":
            m = {'nom': r.str(), 'abrege': r.str(), 'norme': r.str(), 'qual': r.str(),
                 'aGel': r.single(), 'bGel': r.single(),
                 'young': r.single(), 'poisson': r.single(),
                 'epsilon': r.single(), 'sigma': r.single()}
            m['comment'] = r.comment()
            materiaux.append(m)

        elif t.strip() == "":
            break
        else:
            raise SystemExit("Type inconnu dans le .str : %r" % t[:60])

    return structures, materiaux


def parse_mts(path):
    """Materiaux de surface. Voir ModuleMain.bas:OuvrirFichierMatSurface."""
    r = Reader(open(path, 'rb').read())
    entete = r.str()
    if entete != "Fichier de matériaux de surfaces":
        raise SystemExit("En-tete inattendu : %r" % entete)

    mats = []
    while not r.eof():
        t = r.str()
        if t in ("MatériauSimple", "Matériau"):
            m = {'type': t, 'nom': r.str(), 'abrege': r.str(),
                 'norme': r.str(), 'qual': r.str(),
                 'aGel': r.single(), 'bGel': r.single()}
            if t == "Matériau":
                m.update(young=r.single(), poisson=r.single(),
                         epsilon=r.single(), sigma=r.single())
            m['comment'] = r.comment()
            mats.append(m)

        elif t == "MatériauComposé":
            m = {'type': t, 'nom': r.str(), 'abrege': r.str()}
            nb = r.int()
            m['aGel'], m['bGel'] = r.single(), r.single()
            comps = []
            for _ in range(nb):
                row = [r.int()]                      # epaisseur totale preconisee
                for _ in range(3):                   # 3 couples (epaisseur, materiau)
                    e = r.int()
                    a = r.str()
                    row.append([e, a])
                comps.append(row)
            m['compositions'] = comps
            mats.append(m)

        elif t.strip() == "":
            break
        else:
            raise SystemExit("Type inconnu dans le .mts : %r" % t[:60])

    return mats


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('source', help="dossier contenant Certu.str et Certu.mts")
    ap.add_argument('--out', default='build/certu.json')
    a = ap.parse_args()

    structures, matbf = parse_str(os.path.join(a.source, 'Certu.str'))
    matsurf = parse_mts(os.path.join(a.source, 'Certu.mts'))

    os.makedirs(os.path.dirname(a.out) or '.', exist_ok=True)
    json.dump({'structures': structures, 'materiaux': matbf, 'matsurf': matsurf},
              open(a.out, 'w', encoding='utf-8'), ensure_ascii=False)

    print("%d structures, %d materiaux base/fondation, %d materiaux de surface -> %s"
          % (len(structures), len(matbf), len(matsurf), a.out))


if __name__ == '__main__':
    main()
