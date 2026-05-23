from django.http import Http404
from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from django.db.models import Count
from kobe_wave.models import Article, Image, Category
from collections import Counter
import json
import calendar
import re


def contact(request):
    return render(request, "kobe_wave/contact.html")


def project(request):
    return render(request, "kobe_wave/project.html")


def data(request):
    return render(request, "kobe_wave/data.html")


def timeline(request):
    return render(request, "kobe_wave/timeline.html")


def legal(request):
    return render(request, "kobe_wave/legal.html")


def credits(request):
    return render(request, "kobe_wave/credits.html")


def test_404(request):
    raise Http404


def test_500(request):
    raise Exception("Test 500 error")


def custom_404(request, exception):
    return render(request, "404.html", status=404)


def custom_500(request):
    return render(request, "500.html", status=500)


# -----------------------
# DASHBOARD
# -----------------------


def dashboard(request):

    # ── Catégories ──────────────────────────────────────────────
    categories = Category.objects.annotate(total=Count("article")).order_by("-total")
    cat_labels = [c.name for c in categories]
    cat_data = [c.total for c in categories]

    # ── Top 10 catégories (camembert) ───────────────────────────
    top10_cats = categories[:10]
    pie_labels = [c.name for c in top10_cats]
    pie_data = [c.total for c in top10_cats]

    # ── Top 10 auteurs ──────────────────────────────────────────
    top_authors = (
        Article.objects.values("author")
        .annotate(total=Count("id_articles"))
        .order_by("-total")[:10]
    )
    author_labels = [a["author"] or "Inconnu" for a in top_authors]
    author_data = [a["total"] for a in top_authors]

    # ── Images par année ────────────────────────────────────────
    images_by_year = Image.objects.values("year").annotate(total=Count("id_image")).order_by("year")
    year_labels = [str(i["year"]) for i in images_by_year]
    year_data = [i["total"] for i in images_by_year]

    # ── Articles par année ──────────────────────────────────────
    articles_by_year = (
        Article.objects.values("created_at__year")
        .annotate(total=Count("id_articles"))
        .order_by("created_at__year")
    )
    art_year_labels = [str(a["created_at__year"]) for a in articles_by_year]
    art_year_data = [a["total"] for a in articles_by_year]

    # ── Articles par mois ───────────────────────────────────────
    months = list(calendar.month_name)[1:]

    articles_by_month = (
        Article.objects.values("created_at__month")
        .annotate(total=Count("id_articles"))
        .order_by("created_at__month")
    )
    month_map = {i: 0 for i in range(1, 13)}
    for row in articles_by_month:
        month_map[row["created_at__month"]] = row["total"]
    month_data = [month_map[i] for i in range(1, 13)]

    # ── Couleurs dominantes des images ──────────────────────────
    top_colors = (
        Image.objects.values("hexadecimal")
        .annotate(total=Count("id_image"))
        .order_by("-total")[:12]
    )
    color_labels = [c["hexadecimal"] or "#cccccc" for c in top_colors]
    color_data = [c["total"] for c in top_colors]

    # ── Stats globaux ───────────────────────────────────────────
    article_count = Article.objects.count()
    category_count = Category.objects.count()
    image_count = Image.objects.count()

    stats = {
        "articles": article_count,
        "images": image_count,
        "categories": category_count,
        "avg_articles_per_category": round(article_count / max(category_count, 1), 2),
    }

    # ── Context ─────────────────────────────────────────────────
    context = {
        "stats": stats,
        "cat_labels": json.dumps(cat_labels or []),
        "cat_data": json.dumps(cat_data or []),
        "pie_labels": json.dumps(pie_labels or []),
        "pie_data": json.dumps(pie_data or []),
        "author_labels": json.dumps(author_labels or []),
        "author_data": json.dumps(author_data or []),
        "year_labels": json.dumps(year_labels or []),
        "year_data": json.dumps(year_data or []),
        "art_year_labels": json.dumps(art_year_labels or []),
        "art_year_data": json.dumps(art_year_data or []),
        "months": json.dumps(months or []),
        "month_data": json.dumps(month_data or []),
        "color_labels": json.dumps(color_labels or []),
        "color_data": json.dumps(color_data or []),
    }
    return render(request, "kobe_wave/dashboard.html", context)


# -----------------------
# 🏠 HOME
# -----------------------
class HomeView(TemplateView):
    template_name = "kobe_wave/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # ── KPI ─────────────────────────────────────────────────
        article_count = Article.objects.count()
        category_count = Category.objects.count()
        image_count = Image.objects.count()

        context["nb_articles"] = article_count
        context["nb_images"] = image_count
        context["nb_categories"] = category_count
        context["avg_per_cat"] = round(article_count / max(category_count, 1), 2)

        # ── Catégories ──────────────────────────────────────────
        categories = Category.objects.annotate(total=Count("article")).order_by("-total")
        context["cat_labels"] = json.dumps([c.name for c in categories] or [])
        context["cat_data"] = json.dumps([c.total for c in categories] or [])

        # ── Top 10 catégories (camembert) ───────────────────────
        top10 = categories[:10]
        context["pie_labels"] = json.dumps([c.name for c in top10] or [])
        context["pie_data"] = json.dumps([c.total for c in top10] or [])

        # ── Top 10 auteurs ──────────────────────────────────────
        top_authors = (
            Article.objects.values("author")
            .annotate(total=Count("id_articles"))
            .order_by("-total")[:10]
        )
        context["author_labels"] = json.dumps([a["author"] or "Inconnu" for a in top_authors] or [])
        context["author_data"] = json.dumps([a["total"] for a in top_authors] or [])

        # ── Images par année ────────────────────────────────────
        images_by_year = (
            Image.objects.values("year").annotate(total=Count("id_image")).order_by("year")
        )
        context["year_labels"] = json.dumps([str(i["year"]) for i in images_by_year] or [])
        context["year_data"] = json.dumps([i["total"] for i in images_by_year] or [])

        # ── Articles par année ──────────────────────────────────
        articles_by_year = (
            Article.objects.values("created_at__year")
            .annotate(total=Count("id_articles"))
            .order_by("created_at__year")
        )
        context["art_year_labels"] = json.dumps(
            [str(a["created_at__year"]) for a in articles_by_year] or []
        )
        context["art_year_data"] = json.dumps([a["total"] for a in articles_by_year] or [])

        # ── Articles par mois ───────────────────────────────────
        months = list(calendar.month_name)[1:]
        articles_by_month = (
            Article.objects.values("created_at__month")
            .annotate(total=Count("id_articles"))
            .order_by("created_at__month")
        )
        month_map = {i: 0 for i in range(1, 13)}
        for row in articles_by_month:
            month_map[row["created_at__month"]] = row["total"]
        context["months"] = json.dumps(months)
        context["month_data"] = json.dumps([month_map[i] for i in range(1, 13)])

        # ── Couleurs dominantes ──────────────────────────────────
        top_colors = (
            Image.objects.values("hexadecimal")
            .annotate(total=Count("id_image"))
            .order_by("-total")[:12]
        )
        context["color_labels"] = json.dumps(
            [c["hexadecimal"] or "#cccccc" for c in top_colors] or []
        )
        context["color_data"] = json.dumps([c["total"] for c in top_colors] or [])

        return context


# -----------------------
# 📰 ARTICLES LIST
# -----------------------
class ArticleListView(ListView):
    model = Article
    template_name = "kobe_wave/article_list.html"
    context_object_name = "articles"
    paginate_by = 20

    def get_queryset(self):
        qs = Article.objects.select_related("category", "image").all()

        self.q = self.request.GET.get("q", "")
        self.selected_category = self.request.GET.get("category", "")
        self.selected_year = self.request.GET.get("year", "")
        self.selected_month = self.request.GET.get("month", "")

        if self.q:
            qs = qs.filter(title__icontains=self.q)
        if self.selected_category:
            qs = qs.filter(category__id_category=self.selected_category)
        if self.selected_year:
            qs = qs.filter(created_at__year=self.selected_year)
        if self.selected_month:
            qs = qs.filter(created_at__month=self.selected_month)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["q"] = self.q
        context["selected_category"] = self.selected_category
        context["selected_year"] = self.selected_year
        context["selected_month"] = self.selected_month
        context["categories"] = Category.objects.all().order_by("name")
        context["years"] = (
            Article.objects.values_list("created_at__year", flat=True)
            .distinct()
            .order_by("created_at__year")
        )
        context["months"] = {
            1: "January",
            2: "February",
            3: "March",
            4: "April",
            5: "May",
            6: "June",
            7: "July",
            8: "August",
            9: "September",
            10: "October",
            11: "November",
            12: "December",
        }
        context["total_articles"] = self.get_queryset().count()
        return context


# -----------------------
# 📰 ARTICLE DETAIL
# -----------------------
class ArticleDetailView(DetailView):
    model = Article
    template_name = "kobe_wave/article_detail.html"
    context_object_name = "article"


# -----------------------
# 🖼️ IMAGES LIST
# -----------------------
class ImageListView(ListView):
    model = Image
    template_name = "kobe_wave/image_list.html"
    context_object_name = "images"
    paginate_by = 20


# -----------------------
# 📁 CATEGORY DETAIL
# -----------------------
class CategoryDetailView(DetailView):
    model = Category
    template_name = "kobe_wave/category_detail.html"
    context_object_name = "category"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["articles"] = Article.objects.filter(category=self.object)
        return context


def imaginaries(request):

    # ── Catégories tech ciblées ──────────────────────────────────
    TECH_CATS = [
        "Science",
        "Security",
        "Artificial Intelligence",
        "Transportation",
        "Robots",
        "Cloud Computing",
        "Apps",
        "Phones",
        "Design",
        "Business",
        "Culture",
        "Gear",
    ]

    # ── 1. Évolution des catégories tech par année ───────────────
    evo_raw = (
        Article.objects.filter(category__name__in=TECH_CATS)
        .values("created_at__year", "category__name")
        .annotate(total=Count("id_articles"))
        .order_by("created_at__year")
    )

    # Restructurer : { année: { catégorie: total } }
    evo_years = sorted(set(r["created_at__year"] for r in evo_raw))
    evo_map = {y: {c: 0 for c in TECH_CATS} for y in evo_years}
    for r in evo_raw:
        evo_map[r["created_at__year"]][r["category__name"]] = r["total"]

    evo_year_labels = [str(y) for y in evo_years]
    evo_series = [{"name": cat, "data": [evo_map[y][cat] for y in evo_years]} for cat in TECH_CATS]

    # ── 2. Heatmap catégorie × année ─────────────────────────────
    heatmap_data = []
    for yi, year in enumerate(evo_years):
        for ci, cat in enumerate(TECH_CATS):
            heatmap_data.append([yi, ci, evo_map[year].get(cat, 0)])

    # ── 3. Radar des thèmes tech (volumes globaux) ───────────────
    radar_totals = (
        Article.objects.filter(category__name__in=TECH_CATS)
        .values("category__name")
        .annotate(total=Count("id_articles"))
    )
    radar_map = {r["category__name"]: r["total"] for r in radar_totals}
    radar_max = max(radar_map.values(), default=1)
    radar_data = [radar_map.get(c, 0) for c in TECH_CATS]

    # ── 4. Nuage de mots (titres d'articles) ─────────────────────
    STOP_WORDS = {
        "the",
        "a",
        "an",
        "is",
        "in",
        "on",
        "at",
        "to",
        "for",
        "of",
        "and",
        "or",
        "but",
        "it",
        "its",
        "this",
        "that",
        "with",
        "are",
        "was",
        "be",
        "as",
        "by",
        "from",
        "has",
        "have",
        "how",
        "what",
        "why",
        "when",
        "who",
        "will",
        "can",
        "about",
        "up",
        "out",
        "not",
        "no",
        "so",
        "do",
        "if",
        "your",
        "you",
        "we",
        "our",
        "they",
        "their",
        "my",
        "new",
        "get",
        "than",
        "more",
        "all",
        "into",
        "over",
        "after",
        "just",
        "now",
        "like",
        "other",
        "then",
        "could",
        "would",
        "should",
        "there",
        "been",
        "were",
        "which",
        "even",
        "most",
        "also",
        "back",
        "make",
        "made",
        "may",
        "one",
        "two",
        "three",
        "first",
        "last",
        "here",
        "still",
        "us",
        "its",
        "he",
        "she",
        "his",
        "her",
        "im",
        "its",
        "been",
        "does",
        "did",
        "had",
        "via",
        "say",
        "says",
        "want",
        "need",
        "use",
        "used",
        "using",
        "look",
        "way",
        "time",
        "year",
    }

    titles = Article.objects.values_list("title", flat=True)[:50000]
    words = []
    for title in titles:
        for word in re.findall(r"\b[a-zA-Z]{4,}\b", str(title).lower()):
            if word not in STOP_WORDS:
                words.append(word)

    word_freq = Counter(words).most_common(60)
    wordcloud_data = [{"name": w, "value": c} for w, c in word_freq]

    # ── 5. Couleurs dominantes par catégorie ─────────────────────
    top_cats_for_colors = ["Culture", "Business", "Science", "Security", "Gear"]
    color_by_cat = {}
    for cat in top_cats_for_colors:
        colors = (
            Image.objects.filter(article__category__name=cat)
            .values("hexadecimal")
            .annotate(total=Count("id_image"))
            .order_by("-total")[:5]
        )
        color_by_cat[cat] = [
            {"hex": c["hexadecimal"], "count": c["total"]} for c in colors if c["hexadecimal"]
        ]

    # ── 6. Articles : AI vs Security vs Science par année ────────
    battle_cats = ["Artificial Intelligence", "Security", "Science", "Robots", "Transportation"]
    battle_raw = (
        Article.objects.filter(category__name__in=battle_cats)
        .values("created_at__year", "category__name")
        .annotate(total=Count("id_articles"))
        .order_by("created_at__year")
    )
    battle_years = sorted(set(r["created_at__year"] for r in battle_raw))
    battle_map = {y: {c: 0 for c in battle_cats} for y in battle_years}
    for r in battle_raw:
        battle_map[r["created_at__year"]][r["category__name"]] = r["total"]

    battle_year_labels = [str(y) for y in battle_years]
    battle_series = [
        {"name": cat, "data": [battle_map[y][cat] for y in battle_years]} for cat in battle_cats
    ]

    # ── Context ──────────────────────────────────────────────────
    context = {
        # évolution multi-lignes
        "evo_year_labels": json.dumps(evo_year_labels),
        "evo_series": json.dumps(evo_series),
        "tech_cats": json.dumps(TECH_CATS),
        # heatmap
        "heatmap_data": json.dumps(heatmap_data),
        "heatmap_years": json.dumps(evo_year_labels),
        "heatmap_cats": json.dumps(TECH_CATS),
        # radar
        "radar_data": json.dumps(radar_data),
        "radar_max": radar_max,
        "radar_cats": json.dumps(TECH_CATS),
        # nuage de mots
        "wordcloud_data": json.dumps(wordcloud_data),
        # couleurs par catégorie
        "color_by_cat": json.dumps(color_by_cat),
        "color_cats": json.dumps(top_cats_for_colors),
        # bataille
        "battle_year_labels": json.dumps(battle_year_labels),
        "battle_series": json.dumps(battle_series),
        "battle_cats": json.dumps(battle_cats),
    }
    return render(request, "kobe_wave/imaginaries.html", context)


def explore(request):
    categories = Category.objects.annotate(total=Count("article")).order_by("-total")
    context = {
        "categories": json.dumps([c.name for c in categories]),
    }
    return render(request, "kobe_wave/explore.html", context)


def wiredviz(request):
    return render(request, "kobe_wave/wiredviz.html", {})


def covers(request):
    return render(request, "kobe_wave/covers.html", {})
