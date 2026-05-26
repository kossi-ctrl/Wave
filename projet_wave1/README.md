# 🌊 WAVE — Wired Archive of Visual Explorations

> A Django web application for visualizing and exploring data from the Kobe Wave music journal.

[![Python](https://img.shields.io/badge/Python-3.13-blue)](https://python.org)
[![Django](https://img.shields.io/badge/Django-5.2.4-green)](https://djangoproject.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)](https://postgresql.org)
[![Railway](https://img.shields.io/badge/Hosted%20on-Railway-purple)](https://railway.app)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

---

## 🌐 Live Demo

**[https://wave-production-abb3.up.railway.app](https://wave-production-abb3.up.railway.app)**

---

## 📖 About

WAVE is an academic web application developed at the **Centre d'Études Supérieures de la Renaissance (CESR)**, Université de Tours. It allows researchers to analyze and visualize data from the **Kobe Wave** music journal, covering publications from **1993 to 2025**.

### Key Features

- 📊 **Interactive visualizations** — word clouds, heatmaps, co-occurrence networks, radial charts
- 🖼️ **Covers Library** — browse every cover from 1993 to 2025 with color analysis
- 📰 **Article Explorer** — search and filter 193,379 articles by category, author, year
- 🎨 **Color Analysis** — analyze dominant colors of magazine covers
- 🔗 **REST API** — programmatic access to all data

---

## 👥 Authors

| Name | Role |
|------|------|
| **Zangbé Kossi** | Developer |
| **Orphée Bonnardeau** | Developer |

**Supervisor**: Federico Biggio — Université de Tours, CESR

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| Backend | Django 5.2.4 |
| API | Django REST Framework |
| Database | PostgreSQL 15 |
| Web Server | Gunicorn |
| Hosting | Railway |
| Media Storage | Cloudinary |
| Frontend | Bootstrap 5, ECharts |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Git

### Installation

```bash
# Clone the repository
git clone https://scm.univ-tours.fr/22510981t/wave.git
cd wave/projet_wave1

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Run migrations
python manage.py migrate

# Load data
python manage.py loaddata wave_data_fixed.json

# Start development server
python manage.py runserver
```

Open **http://127.0.0.1:8000** in your browser.

---

## 📁 Project Structure

```
wave/
├── projet_wave1/          # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── kobe_wave/             # Main application
│   ├── models.py          # Database models
│   ├── views.py           # View functions
│   ├── api_views.py       # REST API endpoints
│   ├── urls.py            # URL routing
│   ├── serializers.py     # API serializers
│   ├── templates/         # HTML templates
│   └── static/            # CSS, JS, images
├── requirements.txt       # Python dependencies
├── Procfile               # Railway deployment
└── manage.py
```

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 🏛️ Institution

Developed at **Université de Tours**  
Centre d'Études Supérieures de la Renaissance (CESR)  
Tours, France
