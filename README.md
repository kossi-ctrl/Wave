# 🌊 Wave

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.x-092E20?style=flat&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![GitLab CI](https://img.shields.io/badge/GitLab%20CI-passing-FC6D26?style=flat&logo=gitlab&logoColor=white)](/.gitlab-ci.yml)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](./LICENSE)

> > Application web Django pour analyser et visualiser les données du magazine Wired (articles, tendances, thèmes et auteurs).  


---

## 📋 Table des matières

- [🌊 Wave](#-wave)
  - [📋 Table des matières](#-table-des-matières)
  - [🔭 Aperçu](#-aperçu)
  - [✨ Fonctionnalités](#-fonctionnalités)
  - [🛠 Stack technique](#-stack-technique)
  - [📦 Prérequis](#-prérequis)
  - [🚀 Installation rapide](#-installation-rapide)
  - [⚙️ Configuration](#️-configuration)
  - [▶️ Lancer le projet](#️-lancer-le-projet)
  - [🧪 Tests](#-tests)
  - [📁 Structure du projet](#-structure-du-projet)
  - [📚 Documentation](#-documentation)
  - [🤝 Contribuer](#-contribuer)
  - [📄 Licence](#-licence)
  - [👥 Équipe Kobe](#-équipe-kobe)

---

## 🔭 Aperçu

Wave est une application web développée avec Django permettant d'explorer et d'analyser les contenus du magazine Wired à travers 
des visualisations interactives : graphes de connaissance, nuages 
de mots, diagrammes de tendances et analyse des auteurs et thèmes.

**Démo :** [https://wave.exemple.com](https://wave.exemple.com)  
**Documentation complète :** [docs/](./docs/)

---

## ✨ Fonctionnalités

- ✅ Visualisation des articles par catégories, par année et mois
- ✅ Visualisation des image spar année
- ✅ Evolution des thèmes technologiques par année
- ✅ Explorer les données par catégorie, année, auteur et mots-clés
- ✅ Analyse des couleurs 
- ✅ Liens entre mots co-occurents dans les titres
- ✅ Les Mots-Clés principaux par catégorie 
- ✅ Distribution mensuelle des articles
- ✅ Nuages des mots interactifs
- 🚧 [Fonctionnalité en cours]

---

## 🛠 Stack technique

| Couche        | Technologie              |
|---------------|--------------------------|
| Backend       | Python 3.11+, Django 4.x |
| Base de données | PostgreSQL 15+          |
| Frontend      | HTML5, CSS3, JS (Django Templates) |
| CI/CD         | GitLab CI                |
| Déploiement   | Docker + Docker Compose  |

---

## 📦 Prérequis

- Python **3.11+**
- pip / virtualenv
- PostgreSQL **15+**
- Git

---

## 🚀 Installation rapide

```bash
# 1. Cloner le dépôt
git clone https://scm.univ-tours.fr/22510981t/wave.git
cd wave

# 2. Créer l'environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Configurer les variables d'environnement
cp .env.example .env
# Éditer .env avec vos valeurs

# 5. Appliquer les migrations
python manage.py migrate

# 6. Créer un superutilisateur
python manage.py createsuperuser

# 7. Lancer le serveur
python manage.py runserver
```

L'application est accessible sur **http://localhost:8000**

---

## ⚙️ Configuration

Copiez `.env.example` en `.env` et renseignez les variables :

```env
# Django
SECRET_KEY=votre-clé-secrète
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Base de données
DATABASE_URL=postgresql://user:password@localhost:5432/wave_db

# Redis (optionnel)
REDIS_URL=redis://localhost:6379/0

# Email
EMAIL_HOST=smtp.exemple.com
EMAIL_PORT=587
EMAIL_HOST_USER=noreply@exemple.com
EMAIL_HOST_PASSWORD=mot-de-passe
```

---

## ▶️ Lancer le projet

**Développement :**
```bash
python manage.py runserver
```

**Avec Docker :**
```bash
# 1. Cloner le dépôt
git clone https://scm.univ-tours.fr/22510981t/wave.git
cd wave

# 2. Lancer les conteneurs
docker compose up -d

# 3. Appliquer les migrations
docker compose exec web python manage.py migrate

# 4. Importer les données
docker compose exec -T db psql -U wave_kobe -d wave_kobe_db < backup_data.sql
```

L'application est accessible sur **http://localhost:8000**

**Production :**
```bash
gunicorn wave.wsgi:application --bind 0.0.0.0:8000
```

---

## 🧪 Tests

```bash
# Tous les tests
python manage.py test

# Avec couverture
pip install coverage
coverage run manage.py test
coverage report
coverage html  # rapport HTML dans htmlcov/

# Tests d'une application spécifique
python manage.py test projet_wave.tests
```

---

## 📁 Structure du projet

```
wave/
├── .gitlab/                    # Templates GitLab (issues, MR)
│   ├── issue_templates/
│   └── merge_request_templates/
├── docs/                       # Documentation complète
│   ├── uml/                    # Diagrammes UML
│   ├── dev/                    # Guide développeur
│   └── user/                   # Guide utilisateur
├── projet_wave/                # Application Django principale
│   ├── migrations/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   ├── admin.py
│   └── tests.py
├── templates/                  # Templates HTML
├── static/                     # Fichiers statiques
├── manage.py
├── requirements.txt
├── requirements-dev.txt
├── .env.example
├── .gitlab-ci.yml
├── docker-compose.yml
└── README.md
```

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [UML & Architecture](./docs/uml/architecture.md) | Diagrammes UML, architecture système |
| [Guide développeur](./docs/dev/setup.md) | Setup, conventions, API |
| [Guide utilisateur](./docs/user/guide.md) | Manuel d'utilisation |
| [CONTRIBUTING](./CONTRIBUTING.md) | Comment contribuer |
| [CHANGELOG](./CHANGELOG.md) | Historique des versions |

---

## 🤝 Contribuer

Les contributions sont les bienvenues ! Consultez [CONTRIBUTING.md](./CONTRIBUTING.md) pour les directives.

---

## 📄 Licence

Ce projet est sous licence **MIT** — voir le fichier [LICENSE](./LICENSE) pour plus de détails.

---

## 👥 Équipe Kobe

- [kossi Zangbe](https://scm.univ-tours.fr/22510981t)
- [Orphée Bonardeau](https://scm.univ-tours.fr/22205925t)
- [Elise Matta]

*Maintenu par l'équipe Kobe — dernière mise à jour : avril 2026*
