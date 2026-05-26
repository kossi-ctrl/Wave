# Django + Apache ECharts --- From Scratch Setup Guide

This guide walks you through:

-   Installing Django
-   Creating a project and app
-   Creating all required files
-   Adding Apache ECharts
-   Building first Line, Bar, Scatter, and Radar charts

------------------------------------------------------------------------

## 0) Prerequisites

-   Python 3.10+
-   pip

------------------------------------------------------------------------

## 1) Create Project and Install Dependencies

``` bash
mkdir django-echarts-demo
cd django-echarts-demo

python -m venv .venv
source .venv/bin/activate        # macOS/Linux
# .venv\Scripts\activate       # Windows PowerShell

pip install "Django>=5.0,<6.0"

django-admin startproject config .
python manage.py startapp dashboard
```

------------------------------------------------------------------------

## 2) Configure Django

### Edit: `config/settings.py`

Add `dashboard` to `INSTALLED_APPS`:

``` python
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "dashboard",
]
```

Update templates configuration:

``` python
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
    },
]
```

------------------------------------------------------------------------

## 3) Create URLs and Views

### Create: `dashboard/urls.py`

``` python
from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("api/line-bar/", views.api_line_bar, name="api_line_bar"),
    path("api/scatter/", views.api_scatter, name="api_scatter"),
    path("api/radar/", views.api_radar, name="api_radar"),
]
```

------------------------------------------------------------------------

### Edit: `config/urls.py`

``` python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("dashboard.urls")),
]
```

------------------------------------------------------------------------

### Replace: `dashboard/views.py`

``` python
import random
from datetime import date, timedelta
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET


def dashboard(request):
    return render(request, "dashboard.html")


@require_GET
def api_line_bar(request):
    days = int(request.GET.get("days", "30"))
    end = date.today()
    start = end - timedelta(days=days - 1)

    x = [(start + timedelta(days=i)).isoformat() for i in range(days)]
    revenue = [200 + i * 7 + random.randint(-25, 25) for i in range(days)]
    orders = [80 + random.randint(-15, 15) for _ in range(days)]

    return JsonResponse({
        "x": x,
        "series": [
            {"name": "Revenue", "type": "line", "data": revenue, "smooth": True},
            {"name": "Orders", "type": "bar", "data": orders},
        ],
    })


@require_GET
def api_scatter(request):
    n = int(request.GET.get("n", "5000"))
    points = [[random.random() * 100, random.random() * 100] for _ in range(n)]
    return JsonResponse({"points": points})


@require_GET
def api_radar(request):
    indicators = [
        {"name": "Quality", "max": 100},
        {"name": "Speed", "max": 100},
        {"name": "Reliability", "max": 100},
        {"name": "Cost", "max": 100},
        {"name": "Support", "max": 100},
    ]
    values = [82, 74, 88, 61, 79]

    return JsonResponse({
        "indicators": indicators,
        "values": values,
    })
```

------------------------------------------------------------------------

## 4) Create Template

Create folder: `templates/`

Create file: `templates/dashboard.html`

``` html
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <title>Django + ECharts</title>
  <script src="https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js"></script>
  <style>
    body { font-family: system-ui; margin: 24px; }
    .chart { width: 100%; height: 400px; margin-bottom: 30px; }
  </style>
</head>
<body>

<h1>Django + Apache ECharts</h1>

<h2>Line + Bar</h2>
<div id="lineBar" class="chart"></div>

<h2>Scatter</h2>
<div id="scatter" class="chart"></div>

<h2>Radar</h2>
<div id="radar" class="chart"></div>

<script>
const lineBar = echarts.init(document.getElementById("lineBar"));
const scatter = echarts.init(document.getElementById("scatter"));
const radar = echarts.init(document.getElementById("radar"));

async function loadLineBar() {
  const res = await fetch("/api/line-bar/");
  const payload = await res.json();

  lineBar.setOption({
    tooltip: { trigger: "axis" },
    legend: {},
    xAxis: { type: "category", data: payload.x },
    yAxis: { type: "value" },
    series: payload.series
  });
}

async function loadScatter() {
  const res = await fetch("/api/scatter/");
  const payload = await res.json();

  scatter.setOption({
    tooltip: {},
    xAxis: {},
    yAxis: {},
    series: [{
      type: "scatter",
      data: payload.points,
      large: true
    }]
  });
}

async function loadRadar() {
  const res = await fetch("/api/radar/");
  const payload = await res.json();

  radar.setOption({
    tooltip: {},
    radar: { indicator: payload.indicators },
    series: [{
      type: "radar",
      data: [{ value: payload.values, name: "Score" }]
    }]
  });
}

loadLineBar();
loadScatter();
loadRadar();
</script>

</body>
</html>
```

------------------------------------------------------------------------

## 5) Run the Server

``` bash
python manage.py migrate
python manage.py runserver
```

Open:

    http://127.0.0.1:8000/

You now have working Line, Bar, Scatter, and Radar charts powered by
Django + Apache ECharts.
