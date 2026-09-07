![StructUrb+](docs/banner.png)

# StructUrb+

Dimensionnement de chaussée urbaine et bilan carbone à 50 ans, dans le navigateur.

Reprise du moteur de calcul de **Struct-Urb** (CERTU / Cerema, Visual Basic 6, GPL-3.0,
non maintenu) et du catalogue des structures types de chaussées urbaines, avec un
module d'analyse du cycle de vie ajouté.

**[→ Ouvrir l'application](https://VOTRE-ORG.github.io/structurb-plus/)**

---

## Ce que fait le logiciel

- **Trafic** — trafic PL cumulé et nombre d'essieux équivalents à partir du trafic
  initial, de la durée de service, de la croissance annuelle et du CAM, avec contrôle
  des domaines de validité par type de voie.
- **Épaisseurs** — lecture des 69 structures types du catalogue pour les 4 classes de
  plate-forme et les 2 qualités de mise en œuvre, avec signalement du minimum
  technologique et du dépassement du maximum pratique.
- **Gel/dégel** — indice de gel admissible de la structure comparé à l'indice
  atmosphérique de référence corrigé, sur les 84 stations météo du logiciel d'origine.
- **Carbone** — émissions à la pose et sur 50 ans, renouvellements des matériaux
  compris, déblais et création de plate-forme inclus, avec choix du produit pour chaque
  couche. Contribution de chaque matériau lisible sur la barre, et rappel du poste
  structure seule hors déblais et plate-forme.
- **Comparaison** — deux solutions côte à côte sur une règle graduée commune, écart de
  terrassement et écart d'émissions chiffrés.
- **Documentation intégrée** — les textes explicatifs du logiciel d'origine sont repris :
  une notice dépliante à chaque étape de saisie, une note par structure type, et une
  fiche par matériau (norme, classe, module, conditions d'emploi) accessible en cliquant
  son nom sur la coupe ou dans les tableaux.

Étude enregistrable en JSON, feuille de résultats imprimable avec cartouche.

## Installation

Aucune. `index.html` est autonome : téléchargez-le et ouvrez-le. Il fonctionne hors
ligne, sans serveur ni installation, et peut être posé sur un partage réseau.

## Reconstruire depuis les sources

Les fichiers de données binaires du Cerema ne sont pas versionnés ici. Récupérez-les
et relancez la chaîne de construction :

## Conventions de calcul à connaître

- Le **nombre de renouvellements** vaut 50 / durée de vie de référence. Un enrobé à
  20 ans est donc compté 2,5 fois sur la période.
- Le poste **déblais** est facturé à la tonne. La masse volumique est déduite de la
  composition de la structure, avec les valeurs du classeur — 2,35 pour les enrobés,
  2,10 pour la GNT, 1,80 pour le sable — ce qui donne 2,0 à 2,3 t/m³ selon la
  structure. Elle reste modifiable quand la nature des matériaux en place est connue.
  Le classeur d'origine utilisait implicitement 1,0 t/m³, en traitant des mètres cubes
  comme des tonnes ; les études enregistrées avec cette valeur sont converties à
  l'ouverture.
- L'**enduit superficiel** n'a pas d'épaisseur structurelle au catalogue ; 1,5 cm sont
  retenus par défaut pour le calcul carbone, signalés par `~` sur la coupe.
- Le catalogue CERTU date de 1998. Il ne couvre ni les forts taux d'agrégats d'enrobés
  ni les matériaux biosourcés.
- Les **tableaux et abaques** de l'aide d'origine (classification de gélivité, abaques
  de déflexion) étaient des images incorporées au RTF : ils ne sont pas repris et les
  notices concernées le signalent.

## Provenance et licence

Voir [NOTICE.md](NOTICE.md) pour le détail des sources reprises.

Ce logiciel dérive de Struct-Urb, publié par le Cerema sous **GNU GPL v3**. Il est donc
lui-même distribué sous GPL-3.0 : toute redistribution, modifiée ou non, doit rester
sous cette licence et fournir le code source.
