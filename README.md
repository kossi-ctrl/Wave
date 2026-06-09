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


## 🚀 Quick Start — Run locally

### Step 1 — Install Python

You need **Python 3.11+** installed on your computer.  
→ [Python installation guide (by OS)](INSTALLER_PYTHON.md)

### Step 2 — Clone and launch

Open a terminal and run:

```bash
git clone https://kossi:glpat-EiK-kTgQ2F32PfrONYkmcm86MQp1OjEzYgk.01.0z09wqyki@scm.univ-tours.fr/22510981t/wave.git
cd wave

# Windows: double-click lancer_windows.bat
# Mac/Linux:
chmod +x lancer_mac_linux.sh && ./lancer_mac_linux.sh
```

The script handles everything automatically: dependencies, database setup, data loading, and opens the app in your browser.

➡️ The app will be available at **http://localhost:8000**

### Troubleshooting

**❌ "Python is not installed"**  
→ Follow the [Python installation guide](INSTALLER_PYTHON.md) and rerun the script.

**❌ Port 8000 is already in use**  
→ Close the other application using it, then rerun the script.

**❌ Images are not showing**  
→ Check your internet connection — images are hosted on Cloudinary.

---

## 📁 Project Structure


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


---

## 📄 License

This project is licensed under the **CC-BY-4.0** — see the [LICENSE](LICENSE) file for details.

---

## 🏛️ Institution

Developed at **Université de Tours**  
Centre d'Études Supérieures de la Renaissance (CESR)  
Tours, France
