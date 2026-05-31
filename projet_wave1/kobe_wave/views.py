from django.core.mail import send_mail
from django.http import Http404, JsonResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from django.db.models import Count
from kobe_wave.models import Article, Image, Category
from collections import Counter
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from django.db.models import Q
import json
import calendar
import re
import requests


# -----------------------
# 🔍 API CO-OCCURRENCE
# Gère deux cas :
#   /api/cooccurrence/           → graphe initial (top mots globaux)
#   /api/cooccurrence/?word=xxx  → nœud à injecter dans le graphe
# -----------------------

STOP_WORDS = {
    "the","a","an","is","in","on","at","to","for","of","and","or",
    "but","it","its","this","that","with","are","was","be","as","by",
    "from","has","have","how","what","why","when","who","will","can",
    "about","up","out","not","no","so","do","if","your","you","we",
    "our","they","their","new","get","more","all","into","over","just",
    "now","like","then","could","would","should","there","been","were",
    "which","even","most","also","back","make","made","may","one","two",
    "three","first","last","here","still","us","he","she","his","her",
    "does","did","had","via","say","says","want","need","use","used",
    "using","look","way","time","year","very","some","been","have","only",
}


def explore_word(request):
    word = request.GET.get("word", "").lower().strip()

    # ── CAS 1 : pas de mot → graphe initial ──────────────────────
    if not word:
        titles = list(Article.objects.values_list("title", flat=True)[:20000])

        # Fréquence globale des mots
        all_words = []
        for title in titles:
            tokens = re.findall(r"\b[a-zA-Z]{4,}\b", title.lower())
            all_words += [t for t in tokens if t not in STOP_WORDS]

        word_freq = Counter(all_words)
        top_words = [w for w, _ in word_freq.most_common(40)]
        top_set = set(top_words)

        # Co-occurrences entre les top mots
        co_counts = Counter()
        for title in titles:
            tokens = set(re.findall(r"\b[a-zA-Z]{4,}\b", title.lower())) & top_set
            token_list = list(tokens)
            for i in range(len(token_list)):
                for j in range(i + 1, len(token_list)):
                    pair = tuple(sorted([token_list[i], token_list[j]]))
                    co_counts[pair] += 1

        nodes = [
            {"id": w, "value": word_freq[w]}
            for w in top_words
        ]

        links = [
            {"source": p[0], "target": p[1], "value": c}
            for p, c in co_counts.most_common(80)
            if c >= 3
        ]

        return JsonResponse({"nodes": nodes, "links": links})

    # ── CAS 2 : mot fourni → injection dans le graphe ────────────
    articles = Article.objects.filter(title__icontains=word)
    freq = articles.count()

    if freq == 0:
        return JsonResponse({"nodes": [], "links": [], "value": 0})

    co_counts = Counter()
    for article in articles:
        tokens = set(re.findall(r"\b[a-zA-Z]{4,}\b", article.title.lower()))
        tokens -= STOP_WORDS
        if word in tokens:
            for t in tokens:
                if t != word:
                    co_counts[tuple(sorted([word, t]))] += 1

    top_pairs = co_counts.most_common(20)

    links = [
        {"source": p[0], "target": p[1], "value": c}
        for p, c in top_pairs
        if c >= 2
    ]

    neighbor_words = set()
    for p, _ in top_pairs:
        neighbor_words.update(p)
    neighbor_words.discard(word)

    nodes = [{"id": word, "value": freq}]
    for w in neighbor_words:
        w_freq = Article.objects.filter(title__icontains=w).count()
        nodes.append({"id": w, "value": w_freq})

    return JsonResponse({"nodes": nodes, "links": links, "value": freq})


# -----------------------
# 🔍 API ARTICLES PAR MOT
# /api/articles/?q=xxx
# -----------------------
def api_articles(request):
    q = request.GET.get("q", "").strip()
    if not q:
        return JsonResponse([], safe=False)
    articles = Article.objects.filter(title__icontains=q).values(
        "id_articles", "title", "author"
    )[:50]
    return JsonResponse(list(articles), safe=False)


# -----------------------
# 🔍 API ARTICLES CO-OCCURRENCE
# /api/articles-cooccurrence/?w1=xxx&w2=yyy
# -----------------------
def api_articles_cooccurrence(request):
    w1 = request.GET.get("w1", "").strip()
    w2 = request.GET.get("w2", "").strip()
    if not w1 or not w2:
        return JsonResponse([], safe=False)
    articles = Article.objects.filter(
        title__icontains=w1
    ).filter(
        title__icontains=w2
    ).values("id_articles", "title", "author")[:50]
    return JsonResponse(list(articles), safe=False)


# -----------------------
# 🔍 API RADIAL CHART
# /api/radial/
# -----------------------
def api_radial(request):
    STOP_WORDS_RADIAL = STOP_WORDS | {"wired", "review", "best", "guide", "inside"}

    titles = Article.objects.select_related("category").values_list(
        "title", "category__name"
    )[:20000]

    all_words = []
    for title, _ in titles:
        tokens = re.findall(r"\b[a-zA-Z]{4,}\b", title.lower())
        all_words += [t for t in tokens if t not in STOP_WORDS_RADIAL]

    word_freq = Counter(all_words)
    top_words = [w for w, _ in word_freq.most_common(20)]

    categories = list(
        Category.objects.annotate(total=Count("article"))
        .filter(total__gt=0)
        .order_by("-total")
        .values_list("name", flat=True)[:12]
    )

    # Comptage mot × catégorie
    word_cat_counts = {w: Counter() for w in top_words}
    for title, cat_name in titles:
        if not cat_name:
            continue
        tokens = set(re.findall(r"\b[a-zA-Z]{4,}\b", title.lower()))
        for w in top_words:
            if w in tokens:
                word_cat_counts[w][cat_name] += 1

    words_data = [
        {
            "word": w,
            "by_category": [
                {"category": cat, "count": word_cat_counts[w].get(cat, 0)}
                for cat in categories
            ]
        }
        for w in top_words
    ]

    return JsonResponse({"words": words_data, "categories": categories})


# -----------------------
# PAGES
# -----------------------
def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        try:
            send_mail(
                subject=f"Message de {name} via Wave",
                message=f"Nom: {name}\nEmail: {email}\n\nMessage:\n{message}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )
            messages.success(request, "Message envoyé ✔️")
        except Exception as e:
            print("ERREUR EMAIL:", repr(e))
            messages.error(request, f"Erreur technique: {e}")
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
    categories = Category.objects.annotate(total=Count("article")).order_by("-total")
    cat_labels = [c.name for c in categories]
    cat_data = [c.total for c in categories]

    top10_cats = categories[:10]
    pie_labels = [c.name for c in top10_cats]
    pie_data = [c.total for c in top10_cats]

    top_authors = (
        Article.objects.values("author")
        .annotate(total=Count("id_articles"))
        .order_by("-total")[:10]
    )
    author_labels = [a["author"] or "Inconnu" for a in top_authors]
    author_data = [a["total"] for a in top_authors]

    images_by_year = Image.objects.values("year").annotate(total=Count("id_image")).order_by("year")
    year_labels = [str(i["year"]) for i in images_by_year]
    year_data = [i["total"] for i in images_by_year]

    articles_by_year = (
        Article.objects.values("created_at__year")
        .annotate(total=Count("id_articles"))
        .order_by("created_at__year")
    )
    art_year_labels = [str(a["created_at__year"]) for a in articles_by_year]
    art_year_data = [a["total"] for a in articles_by_year]

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

    top_colors = (
        Image.objects.values("hexadecimal")
        .annotate(total=Count("id_image"))
        .order_by("-total")[:12]
    )
    color_labels = [c["hexadecimal"] or "#cccccc" for c in top_colors]
    color_data = [c["total"] for c in top_colors]

    article_count = Article.objects.count()
    category_count = Category.objects.count()
    image_count = Image.objects.count()

    stats = {
        "articles": article_count,
        "images": image_count,
        "categories": category_count,
        "avg_articles_per_category": round(article_count / max(category_count, 1), 2),
    }

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
# HOME
# -----------------------
class HomeView(TemplateView):
    template_name = "kobe_wave/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        article_count = Article.objects.count()
        category_count = Category.objects.count()
        image_count = Image.objects.count()

        context["nb_articles"] = article_count
        context["nb_images"] = image_count
        context["nb_categories"] = category_count
        context["avg_per_cat"] = round(article_count / max(category_count, 1), 2)

        categories = Category.objects.annotate(total=Count("article")).order_by("-total")
        context["cat_labels"] = json.dumps([c.name for c in categories] or [])
        context["cat_data"] = json.dumps([c.total for c in categories] or [])

        top10 = categories[:10]
        context["pie_labels"] = json.dumps([c.name for c in top10] or [])
        context["pie_data"] = json.dumps([c.total for c in top10] or [])

        top_authors = (
            Article.objects.values("author")
            .annotate(total=Count("id_articles"))
            .order_by("-total")[:10]
        )
        context["author_labels"] = json.dumps([a["author"] or "Inconnu" for a in top_authors] or [])
        context["author_data"] = json.dumps([a["total"] for a in top_authors] or [])

        images_by_year = (
            Image.objects.values("year").annotate(total=Count("id_image")).order_by("year")
        )
        context["year_labels"] = json.dumps([str(i["year"]) for i in images_by_year] or [])
        context["year_data"] = json.dumps([i["total"] for i in images_by_year] or [])

        articles_by_year = (
            Article.objects.values("created_at__year")
            .annotate(total=Count("id_articles"))
            .order_by("created_at__year")
        )
        context["art_year_labels"] = json.dumps(
            [str(a["created_at__year"]) for a in articles_by_year] or []
        )
        context["art_year_data"] = json.dumps([a["total"] for a in articles_by_year] or [])

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
# ARTICLES LIST
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
            1: "January", 2: "February", 3: "March", 4: "April",
            5: "May", 6: "June", 7: "July", 8: "August",
            9: "September", 10: "October", 11: "November", 12: "December",
        }
        context["total_articles"] = self.get_queryset().count()
        return context


# -----------------------
# ARTICLE DETAIL
# -----------------------
class ArticleDetailView(DetailView):
    model = Article
    template_name = "kobe_wave/article_detail.html"
    context_object_name = "article"


# -----------------------
# IMAGES LIST
# -----------------------
class ImageListView(ListView):
    model = Image
    template_name = "kobe_wave/image_list.html"
    context_object_name = "images"
    paginate_by = 20


# -----------------------
# CATEGORY DETAIL
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
    TECH_CATS = [
        "Science", "Security", "Artificial Intelligence", "Transportation",
        "Robots", "Cloud Computing", "Apps", "Phones", "Design",
        "Business", "Culture", "Gear",
    ]

    evo_raw = (
        Article.objects.filter(category__name__in=TECH_CATS)
        .values("created_at__year", "category__name")
        .annotate(total=Count("id_articles"))
        .order_by("created_at__year")
    )

    evo_years = sorted(set(r["created_at__year"] for r in evo_raw))
    evo_map = {y: {c: 0 for c in TECH_CATS} for y in evo_years}
    for r in evo_raw:
        evo_map[r["created_at__year"]][r["category__name"]] = r["total"]

    evo_year_labels = [str(y) for y in evo_years]
    evo_series = [{"name": cat, "data": [evo_map[y][cat] for y in evo_years]} for cat in TECH_CATS]

    heatmap_data = []
    for yi, year in enumerate(evo_years):
        for ci, cat in enumerate(TECH_CATS):
            heatmap_data.append([yi, ci, evo_map[year].get(cat, 0)])

    radar_totals = (
        Article.objects.filter(category__name__in=TECH_CATS)
        .values("category__name")
        .annotate(total=Count("id_articles"))
    )
    radar_map = {r["category__name"]: r["total"] for r in radar_totals}
    radar_max = max(radar_map.values(), default=1)
    radar_data = [radar_map.get(c, 0) for c in TECH_CATS]

    STOP_WORDS_CLOUD = STOP_WORDS | {
        "wired", "review", "best", "guide", "inside", "more", "about",
    }

    titles = Article.objects.values_list("title", flat=True)[:50000]
    words = []
    for title in titles:
        for word in re.findall(r"\b[a-zA-Z]{4,}\b", str(title).lower()):
            if word not in STOP_WORDS_CLOUD:
                words.append(word)

    word_freq = Counter(words).most_common(60)
    wordcloud_data = [{"name": w, "value": c} for w, c in word_freq]

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

    context = {
        "evo_year_labels": json.dumps(evo_year_labels),
        "evo_series": json.dumps(evo_series),
        "tech_cats": json.dumps(TECH_CATS),
        "heatmap_data": json.dumps(heatmap_data),
        "heatmap_years": json.dumps(evo_year_labels),
        "heatmap_cats": json.dumps(TECH_CATS),
        "radar_data": json.dumps(radar_data),
        "radar_max": radar_max,
        "radar_cats": json.dumps(TECH_CATS),
        "wordcloud_data": json.dumps(wordcloud_data),
        "color_by_cat": json.dumps(color_by_cat),
        "color_cats": json.dumps(top_cats_for_colors),
        "battle_year_labels": json.dumps(battle_year_labels),
        "battle_series": json.dumps(battle_series),
        "battle_cats": json.dumps(battle_cats),
    }
    return render(request, "kobe_wave/imaginaries.html", context)


def explore(request):
    categories = (
        Category.objects
        .annotate(total=Count("article"))
        .filter(total__gt=0)
        .order_by("-total")
    )
    context = {
        "categories": json.dumps([c.name for c in categories]),
    }
    return render(request, "kobe_wave/explore.html", context)


def wiredviz(request):
    return render(request, "kobe_wave/wiredviz.html", {})


def covers(request):
    return render(request, "kobe_wave/covers.html", {})