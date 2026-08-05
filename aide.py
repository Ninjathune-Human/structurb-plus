#!/usr/bin/env python3
"""
Conversion des textes explicatifs du logiciel Struct-Urb en HTML.

Deux gisements :
  - les 7 fichiers OngletXxx.rtf : aide generale de chaque onglet de saisie ;
  - les commentaires RTF stockes dans Certu.str et Certu.mts : notice de
    chaque materiau et note de chaque structure type.

Les tableaux et abaques de l'aide d'origine etaient des images incorporees au
RTF : ils ne sont pas recuperables en texte et sont signales comme tels.
"""
import html
import re

try:
    from striprtf.striprtf import rtf_to_text
except ImportError:                                     # pragma: no cover
    raise SystemExit("Dependance manquante : pip install striprtf")

# Onglets du logiciel d'origine -> etape correspondante dans StructUrb+
ONGLETS = {
    'voie':      ('OngletVoie',             "Type de voie"),
    'trafic':    ('OngletTrafic',           "Trafic"),
    'cam':       ('OngletCAM',              "Coefficient d'agressivité moyen"),
    'structure': ('OngletStructure',        "Structure type"),
    'plateforme': ('OngletPlateforme',      "Plate-forme support"),
    'surface':   ('OngletCouche de Surface', "Couche de surface"),
    'gel':       ('OngletGel',              "Vérification au gel"),
}

# Les textes d'origine comportent des scories de developpement.
CORRECTIONS = [
    (" TTTest", ""),          # chaine de test laissee dans la notice de l'ES
]


def _nettoyer(t):
    t = t.replace('\x00', '')
    for avant, apres in CORRECTIONS:
        t = t.replace(avant, apres)
    t = t.replace('\u2019', "'").replace('\xa0', ' ')
    t = re.sub(r'[ \t]+\n', '\n', t)
    t = re.sub(r'\n{3,}', '\n\n', t)
    return t.strip()


def _est_titre(ligne, avant_vide, apres_vide):
    """Ligne courte isolee entre deux blancs : intertitre de l'aide d'origine."""
    return avant_vide and apres_vide and 0 < len(ligne.split()) <= 6


def to_html(texte):
    """Texte brut -> HTML simple : paragraphes, listes a puces, intertitres."""
    texte = _nettoyer(texte)
    if not texte:
        return ''
    lignes = texte.split('\n')
    out, liste = [], []

    def vider_liste():
        if liste:
            out.append('<ul>' + ''.join('<li>%s</li>' % x for x in liste) + '</ul>')
            liste.clear()

    for i, brute in enumerate(lignes):
        l = brute.strip().lstrip('\t')
        if not l:
            vider_liste()
            continue
        if l.startswith('·'):
            liste.append(html.escape(l.lstrip('·').strip()))
            continue
        vider_liste()
        avant = (i == 0) or not lignes[i - 1].strip()
        apres = (i == len(lignes) - 1) or not lignes[i + 1].strip()
        if _est_titre(l, avant, apres):
            out.append('<h4>%s</h4>' % html.escape(l))
        else:
            out.append('<p>%s</p>' % html.escape(l))
    vider_liste()
    return ''.join(out)


def rtf_html(brut):
    """Commentaire RTF issu des binaires -> HTML."""
    if not brut:
        return ''
    if brut.lstrip().startswith('{\\rtf'):
        brut = rtf_to_text(brut, errors='ignore')
    return to_html(brut)


def charger_onglets(dossier):
    """Lit les OngletXxx.rtf et renvoie {cle: {titre, html}}."""
    import os
    aide = {}
    for cle, (fichier, titre) in ONGLETS.items():
        chemin = os.path.join(dossier, fichier + '.rtf')
        if not os.path.exists(chemin):
            print("aide manquante : %s" % fichier)
            continue
        brut = open(chemin, encoding='cp1252', errors='replace').read()
        h = to_html(rtf_to_text(brut, errors='ignore'))
        if '\\pict' in brut:
            h += ('<p class="perdu">L\u2019aide d\u2019origine comportait ici des tableaux '
                  'et abaques sous forme d\u2019images, non repris dans cette version. '
                  'Se reporter au guide technique du CERTU.</p>')
        aide[cle] = {'t': titre, 'h': h}
    return aide
