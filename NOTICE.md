# Provenance

## Struct-Urb — CERTU / Cerema

Dépôt : https://github.com/CEREMA/territoires-ville.StructUrb
Licence : GNU General Public License v3.0
État : logiciel non maintenu, développé au CERTU en Visual Basic 6, initialement
diffusé sous licence propriétaire puis libéré sous GPL.

Éléments repris dans StructUrb+ :

| Élément | Origine dans le dépôt Cerema |
|---|---|
| Catalogue des 69 structures types, épaisseurs par classe de plate-forme et qualité de chantier | `Certu.str` |
| Matériaux de base et de fondation (modules, coefficients de gel) | `Certu.str` |
| Matériaux de couche de surface et compositions d'enrobés | `Certu.mts` |
| Trafic cumulé, nombre d'essieux équivalents | `ModuleMain.bas` — `CalculerTraficCum`, `CalculerEtAfficherNE` |
| Domaines de validité du trafic initial et du CAM | `ModuleMain.bas` — `DonnerMinMaxTraficIni`, `DonnerPrecMinMaxCAM` |
| Recherche du NE théorique et lecture des épaisseurs | `ModuleMain.bas` — `TrouverNEthEtInd`, `RechercherEpaisseur` |
| Indice de gel admissible et de référence | `ModuleMain.bas` — `CalculerIndiceGelAdm`, `CalculerIndiceGelRef`, `CalculerQng`, `CalculerQg` |
| 84 stations météo de référence | `ModuleMain.bas` — `RemplirLesStationsMeteo` |
| Épaisseur du lit de pose, constantes de types de voie et de structure | `ModuleMain.bas` |
| Textes d'aide des sept onglets de saisie | `OngletVoie.rtf`, `OngletTrafic.rtf`, `OngletCAM.rtf`, `OngletStructure.rtf`, `OngletPlateforme.rtf`, `OngletCouche de Surface.rtf`, `OngletGel.rtf` |
| Notice de chaque matériau (norme, classe, conditions d'emploi) | commentaires RTF de `Certu.str` et `Certu.mts` |
| Note de chaque structure type (minimum technologique, épaisseurs retenues) | commentaires RTF de `Certu.str` |

Deux écarts assumés sur ces textes, tracés dans `tools/aide.py` :

- les tableaux et abaques de l'aide d'origine étaient des **images incorporées au RTF** ;
  ils ne sont pas récupérables en texte, et les notices concernées portent une mention
  renvoyant au guide technique du CERTU ;
- la chaîne de test `TTTest`, restée dans la notice de l'enduit superficiel, est retirée
  à la construction. C'est la seule correction appliquée au contenu d'origine.

Les fichiers binaires du Cerema ne sont pas redistribués dans ce dépôt : ils sont
récupérés à la construction depuis le dépôt d'origine (voir README).

Ce que StructUrb+ n'a pas repris : le mécanisme de protection par licence
(`ccStruct.bas`, `Protection.bas`), l'interface Visual Basic et l'aide en ligne.

## Base carbone

Facteurs d'émission issus du classeur « Impact environnemental chaussée », établi à
partir des fiches **SEVE TP** (Fédération nationale des travaux publics) et de la base
**INIES**. Voir `data/base-carbone.json`, champ `_source`.

Ces facteurs sont des données d'entrée de l'outil, pas du code. Ils doivent être
tenus à jour par le service qui exploite le logiciel.

## Licence de l'ensemble

StructUrb+ étant une œuvre dérivée de Struct-Urb (GPL-3.0), il est distribué sous
**GNU General Public License v3.0**. Voir `LICENSE`.

Cela n'interdit pas l'usage commercial ni la vente de prestations autour du logiciel,
mais toute distribution binaire ou modifiée doit s'accompagner du code source sous la
même licence.
