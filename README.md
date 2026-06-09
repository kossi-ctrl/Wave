# 🌊 WAVE — Wired Archive of Visual Explorations

> A Django web application for visualizing and exploring data from the USA Wired magazine.

[![Python](https://img.shields.io/badge/Python-3.13-blue)](https://python.org)
[![Django](https://img.shields.io/badge/Django-5.2.4-green)](https://djangoproject.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)](https://postgresql.org)
[![Railway](https://img.shields.io/badge/Hosted%20on-Railway-purple)](https://railway.app)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

---

## 🌐 Live Demo

**[https://wave-production-abb3.up.railway.app](https://wave-production-abb3.up.railway.app)**

---

## 🎨 Prototype Figma
[Voir le prototype](https://www.figma.com/proto/mewZid3X8Ixe3o3WgJsXHu/wave_prototype?node-id=5-165&p=f&viewport=333\%2C175\%2C0.1&t=sBeXYD1dA80R4Qzm-1&scaling=contain&content-scaling=fixed&page-id=0\%3A1)

---

## 📖 About

WAVE is an academic web application developed at the **Centre d'Études Supérieures de la Renaissance (CESR)**, Université de Tours. It allows researchers to analyze and visualize data from the **Wired** magazine, covering publications from **1993 to 2025**.

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

**Supervisor**: 
 Federico Biggio — Université de Tours, CESR
 Carlos Gallardo — Université de Tours, CESR

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


## �🚀 Quick Start

## 🚀 Lancer le projet en local

### Étape 1 — Installer Python

Tu as besoin de **Python 3.11+** installé sur ton ordinateur.  
→ [Guide d'installation Python par OS](INSTALLER_PYTHON.md)

### Étape 2 — Cloner le repo

```bash
git clone https://kossi:glpat-EiK-kTgQ2F32PfrONYkmcm86MQp1OjEzYgk.01.0z09wqyki@scm.univ-tours.fr/22510981t/wave.git
cd wave

# Windows : double-cliquer sur lancer_windows.bat

# Mac/Linux :
chmod +x lancer_mac_linux.sh && ./lancer_mac_linux.sh
cd wave/projet_wave1
```

### Étape 3 — Double-cliquer sur le script

| Ton OS | Fichier à lancer |
|---|---|
| Windows | `lancer_windows.bat` |
| Mac / Linux | `lancer_mac_linux.sh` |

Le script fait tout automatiquement : installation des dépendances, base de données, chargement des données, et ouverture du navigateur.

➡️ L'application s'ouvre sur **http://localhost:8000**

> **Mac/Linux** — si le double-clic ne fonctionne pas, ouvre un terminal dans le dossier et tape :
> ```bash
> chmod +x lancer_mac_linux.sh && ./lancer_mac_linux.sh
> ```

### Problèmes fréquents

**❌ "Python n'est pas installé"**  
→ Suis le [guide d'installation Python](INSTALLER_PYTHON.md) puis relance le script.

**❌ Le port 8000 est déjà utilisé**  
→ Ferme l'autre application qui l'utilise, ou relance le script.

**❌ Les images ne s'affichent pas**  
→ Vérifie ta connexion internet — les images sont hébergées sur Cloudinary.

# Load data
python manage.py loaddata wave_data_fixed.json

# Start development server
python manage.py runserver
```


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

This project is licensed under the **CC-BY-4.0** — see the [LICENSE](LICENSE) file for details.

---

## 🏛️ Institution

Developed at **Université de Tours**  
Centre d'Études Supérieures de la Renaissance (CESR)  
Tours, France
