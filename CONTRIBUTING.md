# 🤝 Guide de contribution — Wave

Merci de votre intérêt pour contribuer à Wave ! Ce guide vous explique comment participer efficacement.

---

## Code of Conduct

Ce projet adhère à un code de conduite basé sur le respect mutuel. Tout comportement irrespectueux entraînera une exclusion du projet.

---

## Comment contribuer ?

### 1. Signaler un bug

Avant de créer une issue, vérifiez qu'elle n'existe pas déjà dans [les issues ouvertes](https://scm.univ-tours.fr/22510981t/wave/-/issues).

Utilisez le template **Bug Report** et incluez :
- Description claire et concise du bug
- Étapes pour reproduire le problème
- Comportement attendu vs observé
- Captures d'écran si pertinent
- Environnement (OS, navigateur, version Python/Django)

### 2. Proposer une fonctionnalité

Utilisez le template **Feature Request** et décrivez :
- Le problème que la fonctionnalité résoudrait
- La solution envisagée
- Les alternatives considérées

### 3. Soumettre du code

#### Workflow Git

```
1. Créer une branche depuis main
2. Implémentez votre changement
3. Écrivez / mettez à jour les tests
4. Vérifiez que tous les tests passent
5. Ouvrez une Merge Request vers develop
```

#### Checklist avant de soumettre une MR

- [ ] Le code respecte les conventions (Black, Flake8, isort)
- [ ] Des tests ont été ajoutés / mis à jour
- [ ] La couverture de tests ne diminue pas
- [ ] La documentation a été mise à jour si nécessaire
- [ ] Le CHANGELOG.md a été mis à jour
- [ ] Le titre de la MR suit le format Conventional Commits

#### Processus de review

- Toute MR nécessite **au moins 1 approbation**
- Les pipelines CI doivent passer ✅
- Les conflits doivent être résolus avant merge

---

## Standards de code

Voir [docs/dev/setup.md](./docs/dev/setup.md#3-conventions-de-code) pour les détails complets.

```bash
# Avant chaque commit
black .
isort .
flake8 .
python manage.py test
```

---

## Setup de développement

Voir [docs/dev/setup.md](./docs/dev/setup.md) pour les instructions complètes.

---

*Merci pour votre contribution ! 🌊*
