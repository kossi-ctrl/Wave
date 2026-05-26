# 🛠 Guide Développeur — Wave

> Documentation technique pour les développeurs contribuant au projet Wave.

---

## Table des matières

- [1. Environnement de développement](#1-environnement-de-développement)
- [2. Architecture du code](#2-architecture-du-code)
- [3. Conventions de code](#3-conventions-de-code)
- [4. Base de données](#4-base-de-données)
- [5. Tests](#5-tests)
- [6. API interne](#6-api-interne)
- [7. Pipeline CI/CD](#7-pipeline-cicd)
- [8. Débogage](#8-débogage)

---

## 1. Environnement de développement

### Prérequis

| Outil | Version minimale | Lien |
|-------|-----------------|------|
| Python | 3.11 | [python.org](https://python.org) |
| PostgreSQL | 15 | [postgresql.org](https://postgresql.org) |
| Git | 2.40 | [git-scm.com](https://git-scm.com) |
| Docker (optionnel) | 24 | [docker.com](https://docker.com) |

### Installation pas à pas

```bash
# Cloner le projet
git clone https://scm.univ-tours.fr/22510981t/wave.git
cd wave

# Créer et activer le virtualenv
python3 -m venv venv
source env/bin/activate

# Dépendances de développement
pip install -r requirements-dev.txt


# Variables d'environnement
cp .env.example .env
# Éditer .env

# Créer la base de données
createdb wave_kobe_db
python manage.py migrate

# Charger des données de test
python manage.py loaddata fixtures/dev_data.json

# Superutilisateur local
python manage.py createsuperuser

# Lancer le serveur
python manage.py runserver
```

### Variables d'environnement (`.env`)

| Variable | Obligatoire | Description | Exemple |
|----------|-------------|-------------|---------|
| `SECRET_KEY` | ✅ | Clé secrète Django | `django-insecure-xxx` |
| `DEBUG` | ✅ | Mode debug | `True` |
| `ALLOWED_HOSTS` | ✅ | Hôtes autorisés | `localhost,127.0.0.1` |
| `DATABASE_URL` | ✅ | URL PostgreSQL | `postgresql://user:pwd@localhost/wave` |
| `REDIS_URL` | ❌ | URL Redis | `redis://localhost:6379/0` |
| `EMAIL_HOST` | ❌ | Serveur SMTP | `smtp.mailtrap.io` |
| `SENTRY_DSN` | ❌ | Monitoring Sentry | `https://xxx@sentry.io/xxx` |

### Docker Compose (développement)

```bash
# Démarrer tous les services
docker-compose up -d

# Voir les logs
docker-compose logs -f web

# Lancer les migrations dans le conteneur
docker-compose exec web python manage.py migrate

# Arrêter
docker-compose down
```

---

## 2. Architecture du code

### Structure Django

```
projet_wave/
├── __init__.py
├── admin.py          # Configuration Django Admin
├── apps.py           # Configuration de l'app
├── forms.py          # Formulaires Django
├── managers.py       # Custom ORM Managers
├── middleware.py     # Middlewares personnalisés
├── migrations/       # Migrations DB (auto-générées)
├── models.py         # Modèles de données
├── permissions.py    # Permissions personnalisées
├── serializers.py    # Sérialiseurs (DRF si utilisé)
├── services.py       # Logique métier
├── signals.py        # Django Signals
├── tests/
│   ├── test_models.py
│   ├── test_views.py
│   ├── test_forms.py
│   └── test_services.py
├── urls.py           # Routes de l'application
└── views.py          # Vues Django
```

### Séparation des responsabilités

- **`models.py`** : Définition des données + méthodes simples sur les instances
- **`services.py`** : Logique métier complexe, réutilisable entre les vues
- **`views.py`** : Orchestration requête/réponse uniquement
- **`forms.py`** : Validation des entrées utilisateur
- **`admin.py`** : Interface d'administration

> ⚠️ **Règle d'or :** Les vues ne contiennent pas de logique métier. Tout passe par les services.

---

## 3. Conventions de code

### Style Python — PEP 8 + Black

```bash
# Formater le code
black .

# Vérifier le style
flake8 .

# Trier les imports
isort .
```

### Configuration `.flake8`

```ini
[flake8]
max-line-length = 88
extend-ignore = E203, W503
exclude = migrations/, venv/, .git/
```

### Nommage

| Type | Convention | Exemple |
|------|-----------|---------|
| Classes | PascalCase | `WaveDetailView` |
| Fonctions/méthodes | snake_case | `get_published_waves()` |
| Variables | snake_case | `user_profile` |
| Constantes | UPPER_SNAKE | `MAX_WAVE_LENGTH` |
| URLs | kebab-case | `/waves/my-wave/` |
| Templates | snake_case | `wave_detail.html` |

### Commits — Conventional Commits

Format : `type(scope): description`

```
feat(waves): ajouter la fonctionnalité de tags
fix(auth): corriger la redirection après login
docs(readme): mettre à jour les instructions d'installation
test(waves): ajouter tests unitaires WaveService
refactor(models): simplifier la méthode get_status
chore(deps): mettre à jour Django 4.2 → 4.3
```

Types : `feat`, `fix`, `docs`, `test`, `refactor`, `chore`, `perf`, `style`

### Branches Git

```
main          → production stable
develop       → intégration continue
feature/xxx   → nouvelle fonctionnalité
fix/xxx       → correction de bug
hotfix/xxx    → correctif urgent sur main
release/x.x.x → préparation d'une version
```

---

## 4. Base de données

### Migrations

```bash
# Créer une migration
python manage.py makemigrations

# Appliquer les migrations
python manage.py migrate

# Voir le SQL généré
python manage.py sqlmigrate projet_wave 0001

# Vérifier l'état
python manage.py showmigrations
```

### Règles sur les migrations

- ✅ Toujours commiter les migrations avec le code associé
- ✅ Une migration = un changement atomique
- ❌ Ne jamais modifier une migration déjà mergée sur `main`
- ❌ Ne jamais supprimer de migrations

### Fixtures de développement

```bash
# Exporter des données existantes
python manage.py dumpdata projet_wave --indent 2 > fixtures/dev_data.json

# Charger les fixtures
python manage.py loaddata fixtures/dev_data.json
```

---

## 5. Tests

### Lancer les tests

```bash
# Tous les tests
python manage.py test

# App spécifique
python manage.py test projet_wave

# Test spécifique
python manage.py test projet_wave.tests.test_models.WaveModelTest

# Avec coverage
coverage run --source='.' manage.py test
coverage report --fail-under=80
coverage html
```

### Structure d'un test

```python
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from projet_wave.models import Wave
from projet_wave.services import WaveService

User = get_user_model()

class WaveModelTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        """Données partagées pour tous les tests de la classe."""
        cls.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="SecurePass123!"
        )
    
    def test_wave_creation(self):
        """Un Wave créé doit avoir un statut 'draft' par défaut."""
        wave = Wave.objects.create(
            title="Test Wave",
            content="Contenu de test",
            author=self.user
        )
        self.assertEqual(wave.status, "draft")
        self.assertIsNotNone(wave.slug)
    
    def test_wave_publish(self):
        """La méthode publish() doit changer le statut en 'published'."""
        wave = Wave.objects.create(
            title="Wave à publier",
            content="Contenu",
            author=self.user
        )
        wave.publish()
        self.assertEqual(wave.status, "published")
        self.assertIsNotNone(wave.published_at)
```

### Objectifs de couverture

| Module | Couverture minimale |
|--------|-------------------|
| `models.py` | 90% |
| `services.py` | 85% |
| `views.py` | 75% |
| `forms.py` | 80% |

---

## 6. API interne

### Endpoints principaux

| Méthode | URL | Vue | Description |
|---------|-----|-----|-------------|
| GET | `/` | `HomeView` | Page d'accueil |
| GET/POST | `/login/` | `LoginView` | Authentification |
| GET | `/logout/` | `LogoutView` | Déconnexion |
| GET | `/dashboard/` | `DashboardView` | Tableau de bord |
| GET | `/waves/` | `WaveListView` | Liste des waves |
| GET/POST | `/waves/create/` | `WaveCreateView` | Créer un wave |
| GET | `/waves/<slug>/` | `WaveDetailView` | Détail d'un wave |
| GET/POST | `/waves/<slug>/edit/` | `WaveUpdateView` | Modifier un wave |
| POST | `/waves/<slug>/delete/` | `WaveDeleteView` | Supprimer un wave |
| GET/POST | `/profile/` | `ProfileView` | Profil utilisateur |

### Exemple de Vue (CBV)

```python
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import WaveForm
from .services import WaveService

class WaveCreateView(LoginRequiredMixin, CreateView):
    form_class = WaveForm
    template_name = "waves/wave_form.html"
    success_url = reverse_lazy("wave-list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        WaveService.notify_followers(self.object)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Créer un Wave"
        return context
```

---

## 7. Pipeline CI/CD

Voir [`.gitlab-ci.yml`](../../.gitlab-ci.yml) pour la configuration complète.

**Stages :**
1. `lint` — Vérification du style (Black, Flake8, isort)
2. `test` — Tests unitaires + couverture
3. `security` — Audit de sécurité (Bandit, Safety)
4. `build` — Construction de l'image Docker
5. `deploy-staging` — Déploiement staging (branche `develop`)
6. `deploy-prod` — Déploiement production (branche `main`, manuel)

---

## 8. Débogage

### Django Debug Toolbar

```python
# Installé en dev uniquement
pip install django-debug-toolbar

# Accès : http://localhost:8000 (panneau latéral)
```

### Shell Django

```bash
# Shell interactif avec contexte Django
python manage.py shell

# Exemple
>>> from projet_wave.models import Wave
>>> Wave.objects.filter(status='published').count()
```

### Logs

```python
import logging
logger = logging.getLogger(__name__)

# Utilisation
logger.debug("Message de debug")
logger.info("Information importante")
logger.warning("Avertissement")
logger.error("Erreur", exc_info=True)
```

### Problèmes fréquents

| Problème | Solution |
|----------|----------|
| `ModuleNotFoundError` | Vérifier que le venv est activé |
| `OperationalError: no such table` | Lancer `python manage.py migrate` |
| `ImproperlyConfigured: SECRET_KEY` | Vérifier le fichier `.env` |
| `CORS error` | Vérifier `CORS_ALLOWED_ORIGINS` dans settings |
| Migration conflict | `python manage.py migrate --merge` |

---

*Dernière mise à jour : avril 2026*
