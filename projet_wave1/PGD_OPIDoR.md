# PGD — format OPIDoR (version M1)

Projet : WAVE — corpus Wired (1993–2025)
Auteur : [Ton Nom]
Encadrant : [Nom de l'encadrant]
Date : 2026-06-04

---

## 1) Bref descriptif (champ court OPIDoR)
Scripts Python d’ingestion, nettoyage, validation et export du corpus WAVE (articles Wired 1993–2025). Données issues d’extractions automatisées ; publication d’un sous‑ensemble représentatif et des scripts ETL.

## 2) Descriptif détaillé (champ détaillé OPIDoR)
Le projet WAVE produit un corpus JSON d’articles extraits de Wired (1993–2025) et les scripts permettant l’ingestion, la normalisation, la validation (JSON Schema) et la génération d’exports (JSON/CSV). Le dépôt `projet_wave1` contient le code ETL, le schéma JSON, des lots de test et le corpus principal (`wave_data_fixed.json`). Pour des raisons de droits, seules les métadonnées et un sous‑ensemble seront publiés ; les images protégées ne seront publiées que si les droits le permettent.

## 3) Producteurs / créateurs
- Auteur principal : [Ton Nom], étudiant — responsable de la collecte et du nettoyage.
- Encadrant scientifique : [Nom de l'encadrant].
- Contact technique : [email étudiant] (remplacer).

## 4) Dates
- Période de collecte : 1993–2025 (données sources)
- Date d’extraction principale : [2026-xx-xx] (mettre la date exacte)
- Date de dépôt prévue : [à compléter]

## 5) Typologie / nature des données
- Typologie : corpus textuel structuré (métadonnées d’articles, index), métadonnées d’images.
- Format principal : JSON (UTF‑8). Exports CSV possibles.

## 6) Volume / taille
- Corpus principal : ~50,5 MB (`projet_wave1/wave_data_fixed.json`).
- Lots de test : ~1–1.5 MB chacun (`lot_*.json`).

## 7) Standards de métadonnées et schéma
- JSON Schema : fichier `projet_wave1/schema.json` (à ajouter si absent).
- Mapping recommandé vers Dublin Core pour la diffusion.
- Champs minimaux : `id`, `title`, `author`, `date`, `source_url`, `license`, `checksum`, `extraction_date`.

## 8) Conditions d’accès et diffusion
- Code ETL : dépôt GitHub/GitLab (public) sous licence `MIT` recommandée.
- Données publiées : sous‑ensemble sur Zenodo sous `CC BY 4.0` si les droits le permettent.
- Accès restreint pour données protégées : fournir métadonnées publiques mais ne pas diffuser les fichiers binaires protégés.

## 9) Modalités de partage
- Dépôt du code : GitHub/GitLab (lien à ajouter).
- Dépôt des données réduites : Zenodo (obtenir DOI lors du dépôt).
- Release Git pour versionnement du code ; release/asset ou Zenodo pour gros fichiers.

## 10) Sécurité et sauvegardes
- Hébergement des scripts et petits fichiers : dépôt distant (GitHub/GitLab privé durant dev).
- Sauvegardes : archive ZIP du dataset sur un disque externe et/ou serveur institutionnel.
- Vérification d’intégrité : conserver checksum SHA256 pour fichiers majeurs.

## 11) Propriété intellectuelle et licences
- Code : `MIT` (par défaut).
- Données publiées : `CC BY 4.0` (par défaut) — à confirmer.
- Pour contenus protégés (images, textes complets) : mentionner droits et limiter la diffusion.

## 12) Aspects éthiques / RGPD
- Aucun traitement de données sensibles prévu. Si des données personnelles apparaissent, anonymiser ou supprimer avant dépôt.
- Documenter toute extraction contenant données personnelles et la base légale.

## 13) Conservation et pérennité
- Dépôt final conseillé : Zenodo (dataset réduit) + archive institutionnelle.
- Formats pérennes : JSON/CSV + schéma JSON.
- Durée recommandée : 10 ans.

## 14) Disponibilité des livrables
- Code ETL complet (`projet_wave1/`)
- Dataset réduit (`wave_data_export.json` ou échantillon)
- JSON Schema (`schema.json`)
- README méthodologique et `METADATA.yaml`

## 15) Checklist pour dépôt OPIDoR
- [ ] Confirmer licences (code / données).
- [ ] Renseigner contacts et responsables.
- [ ] Générer `schema.json` et `METADATA.yaml`.
- [ ] Valider JSON contre le schéma.
- [ ] Préparer ZIP/manifest et déposer sur Zenodo → récupérer DOI.

---

Remarques :
- J’ai utilisé des licences par défaut (`MIT` pour code, `CC BY 4.0` pour données). Indique si tu veux d’autres licences.
- Remplace les placeholders `[Ton Nom]`, `[Nom de l'encadrant]`, `[email étudiant]`, et dates avant dépôt.

Fichier créé : [projet_wave1/PGD_OPIDoR.md](projet_wave1/PGD_OPIDoR.md)
