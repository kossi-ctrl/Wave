# 📖 WAVE — User Guide

## Welcome to WAVE

WAVE (Wired Archive of Visual Explorations) is a web application that allows you to explore and visualize data from the Kobe Wave music journal (1993–2025).

**Access the application**: [https://wave-production-abb3.up.railway.app](https://wave-production-abb3.up.railway.app)

---

## 🏠 Home Page

The home page gives you an overview of the entire dataset:

- **193,379 articles** indexed
- **362 covers** from 1993 to 2025
- **Cover of the moment** — a randomly selected cover with its publication year
- **Timeline of covers** — scroll through all covers chronologically
- **Explore** section — quick access to main features

---

## 🖼️ Covers Library

Browse every Wired cover from 1993 to today.

### How to use

1. **Color strip** — a horizontal strip showing all covers as colored bars
2. **Click a bar** — the full cover image appears on the left
3. **Bubble chart** — shows the most frequent words in articles from that issue
4. **Keyboard navigation** — use ← → arrow keys to browse covers

### Filters

| Filter | Description |
|--------|-------------|
| **Year** | Filter covers by year (1993–2025) |
| **Month** | Filter by month of publication |
| **Category** | Filter by article category |

Click **✕ Reset** to clear all filters.

---

## 📊 Data

The Data page offers advanced visualizations:

### Co-occurrence Network
Shows which words appear together most frequently in article titles. 
- **Nodes** = words, sized by frequency
- **Links** = words that appear together
- Click two connected nodes to see related articles

### Radial Chart
Shows word distribution across categories.

### Heatmap
Visualizes article frequency by year and category/author/word.

### Color Analysis
3D scatter plot of cover colors by hue, saturation, and brightness.

---

## 📅 Timeline

Follow the visual evolution of Wired covers year by year.

- Scroll horizontally through the timeline
- Click any cover to see details
- Color analysis of each cover is displayed

---

## 🔍 Search & Explore

Search through all 193,379 articles:

- **Search by keyword** — search in article titles
- **Filter by category** — select from 44 categories
- **Filter by year** — from 1993 to 2025
- **Filter by month** — narrow down by month
- Click any article to see its full details

---

## 🔗 API

WAVE provides a REST API for developers:

| Endpoint | Description |
|----------|-------------|
| `/api/articles/` | List articles with filters |
| `/api/categories/` | List all categories |
| `/api/images/` | List all covers |
| `/api/stats/` | Global statistics |
| `/api/covers/` | Cover data with colors |
| `/api/wordcloud/` | Word frequency data |
| `/api/cooccurrence/` | Word co-occurrence network |
| `/api/heatmap/` | Heatmap data |
| `/api/color-analysis/` | Color analysis data |

---

## 📬 Contact

Use the **Contact** page to send feedback or questions about WAVE.

Fill in your name, email address, and message, then click **Send**.
