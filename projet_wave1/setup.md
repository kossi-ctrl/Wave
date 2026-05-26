# 🛠️ WAVE — Developer Guide

## Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Git
- pip

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://scm.univ-tours.fr/22510981t/wave.git
cd wave/projet_wave1
```

### 2. Create virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # for development tools
```

### 4. Configure environment

```bash
cp .env.example .env
```

Edit `.env` with your settings:

```env
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1

# PostgreSQL
PGDATABASE=wave_kobe_db
PGUSER=wave_kobe
PGPASSWORD=your-password
PGHOST=localhost
PGPORT=5432

# Cloudinary (for media files)
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret

# Email
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_APP_PASSWORD=your-app-password
```

### 5. Create database

```bash
psql -U postgres
CREATE DATABASE wave_kobe_db;
CREATE USER wave_kobe WITH PASSWORD 'your-password';
GRANT ALL PRIVILEGES ON DATABASE wave_kobe_db TO wave_kobe;
\q
```

### 6. Run migrations

```bash
python manage.py migrate
```

### 7. Load data

```bash
python manage.py loaddata wave_data_fixed.json
```

### 8. Start development server

```bash
python manage.py runserver
```

Open **http://127.0.0.1:8000**

---

## 📁 Project Structure

```
wave/
├── projet_wave1/              # Django project config
│   ├── settings.py            # Settings (reads from .env)
│   ├── urls.py                # Main URL routing
│   ├── wsgi.py                # WSGI entry point
│   └── asgi.py                # ASGI entry point
├── kobe_wave/                 # Main application
│   ├── models.py              # Database models (Article, Image, Category)
│   ├── views.py               # View functions and class-based views
│   ├── api_views.py           # REST API endpoints
│   ├── urls.py                # App URL routing
│   ├── serializers.py         # DRF serializers
│   ├── admin.py               # Django admin configuration
│   ├── tests.py               # Unit tests
│   ├── migrations/            # Database migrations
│   ├── templates/             # HTML templates
│   │   └── kobe_wave/
│   │       ├── base.html      # Base template
│   │       ├── home.html      # Home page
│   │       ├── covers.html    # Covers library
│   │       ├── data.html      # Data visualizations
│   │       ├── timeline.html  # Timeline
│   │       └── contact.html   # Contact form
│   ├── static/                # Static files
│   │   └── kobe_wave/
│   │       ├── css/           # Stylesheets
│   │       ├── js/            # JavaScript files
│   │       └── img/           # Images
│   └── media/                 # Uploaded media files
│       └── wave_cover/        # Cover images
├── staticfiles/               # Collected static files (production)
├── requirements.txt           # Production dependencies
├── requirements-dev.txt       # Development dependencies
├── Procfile                   # Railway deployment command
├── .env.example               # Environment variables template
├── .gitlab-ci.yml             # CI/CD pipeline configuration
└── manage.py                  # Django management script
```

---

## 🗃️ Database Models

### Category
```python
class Category(models.Model):
    id_category = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
```

### Image (Cover)
```python
class Image(models.Model):
    id_image = models.AutoField(primary_key=True)
    filename = models.CharField(max_length=200, unique=True)
    year = models.IntegerField()
    month = models.IntegerField()
    hexadecimal = models.CharField(max_length=7)
    hue = models.IntegerField()
    sat = models.IntegerField()
    bri = models.IntegerField()
    # ... color data fields
```

### Article
```python
class Article(models.Model):
    id_articles = models.AutoField(primary_key=True)
    title = models.CharField(max_length=500)
    url = models.URLField(max_length=500)
    author = models.CharField(max_length=200)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL)
    created_at = models.DateTimeField()
```

---

## 🔗 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/articles/` | List articles (supports ?q=, ?category=, ?year=) |
| GET | `/api/categories/` | List all categories with article counts |
| GET | `/api/images/` | List all cover images |
| GET | `/api/stats/` | Global statistics |
| GET | `/api/covers/` | Cover data with Cloudinary URLs |
| GET | `/api/wordcloud/?category=` | Word frequency data |
| GET | `/api/cooccurrence/?top=30` | Word co-occurrence network |
| GET | `/api/heatmap/?mode=words` | Heatmap data (words/categories/authors) |
| GET | `/api/color-analysis/` | Color analysis scatter data |
| GET | `/api/cover-words/?year=&month=` | Words for a specific cover |
| GET | `/api/radial/` | Radial word-category data |

---

## 🧪 Running Tests

```bash
# Run all tests
python manage.py test kobe_wave

# Run with coverage
python3 -m coverage run manage.py test kobe_wave
python3 -m coverage report
python3 -m coverage xml
```

---

## 🚀 Deployment (Railway)

### Environment Variables on Railway

Set these in Railway → service Wave → Variables:

```
DEBUG=False
SECRET_KEY=your-production-secret-key
ALLOWED_HOSTS=wave-production-abb3.up.railway.app
PGDATABASE=railway
PGUSER=postgres
PGPASSWORD=your-railway-pg-password
PGHOST=postgres.railway.internal
PGPORT=5432
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_APP_PASSWORD=your-app-password
```

### Deploy

```bash
# Push to GitHub triggers automatic Railway deployment
git push github main
```

---

## 🔧 Development Tools

| Tool | Purpose |
|------|---------|
| `flake8` | Code style checking |
| `black` | Code formatting |
| `isort` | Import sorting |
| `coverage` | Test coverage |
| `bandit` | Security analysis |
| `safety` | Dependency vulnerability check |

Run all checks:
```bash
flake8 . --max-line-length=100
black .
isort .
bandit -r projet_wave1/
```

---

## 📝 Contributing

1. Create a branch: `git checkout -b feature/your-feature`
2. Make changes and commit: `git commit -m "feat: your feature"`
3. Push: `git push origin feature/your-feature`
4. Create a merge request on GitLab
