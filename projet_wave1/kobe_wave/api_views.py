from rest_framework.decorators import api_view
from kobe_wave.serializers import ArticleSerializer, ImageSerializer
from rest_framework.response import Response
from django.db.models import Count
from django.core.cache import cache
from kobe_wave.models import Article, Image, Category
from collections import Counter, defaultdict
import cloudinary
import cloudinary.utils
import re
import os
from kobe_wave import precompute as pc

STOP_WORDS = frozenset(
    {
        # Articles / determiners FR
        "le", "la", "les", "un", "une", "des", "du", "au", "aux",
        "ce", "cet", "cette", "ces", "mon", "ton", "son", "mes",
        "tes", "ses", "notre", "votre", "leur", "leurs", "nos", "vos",
        # Prepositions / conjunctions FR
        "de", "en", "dans", "sur", "sous", "avec", "sans", "pour",
        "par", "vers", "entre", "donc", "mais", "ainsi", "comme",
        "puis", "car", "que", "qui", "dont", "quoi", "quand", "depuis",
        "selon", "lors", "tout", "plus", "tres", "trop", "bien", "meme",
        "aussi", "deja", "encore", "toujours", "jamais", "chez", "pres",
        "apres", "avant", "pendant", "contre",
        # Common verbs FR
        "est", "sont", "etre", "avoir", "fait", "font", "peut", "peuvent",
        "doit", "doivent", "faut", "vient", "devient", "reste", "sera",
        "seront", "etait", "avait",
        # Pronouns FR
        "il", "elle", "ils", "elles", "nous", "vous", "eux", "cela",
        "ceci", "celui", "celle", "ceux",
        # Articles EN
        "the", "a", "an",
        # Prepositions / conjunctions EN
        "in", "on", "at", "to", "for", "of", "and", "or", "but", "with",
        "from", "by", "as", "into", "over", "after", "about", "than",
        "via", "within", "between", "through", "against", "during",
        "before", "up", "out", "off",
        # Auxiliary verbs EN
        "is", "are", "was", "were", "be", "been", "has", "have", "had",
        "will", "would", "could", "should", "may", "might", "does", "did", "do", "can",
        # Pronouns EN
        "it", "its", "this", "that", "they", "their", "there", "which",
        "who", "what", "how", "when", "where", "why", "he", "she", "his",
        "her", "we", "our", "you", "your", "us", "my",
        # Adverbs / filler words EN
        "not", "no", "so", "if", "just", "now", "also", "even", "still",
        "back", "most", "more", "all", "then", "here", "only", "very",
        "too", "yet", "both", "each", "other", "such", "same", "new",
        # Generic verbs EN
        "get", "make", "made", "use", "used", "using", "say", "says",
        "said", "want", "need", "look", "know", "take", "come", "give",
        "find", "think", "see", "like", "show",
        # Time-related
        "time", "year", "years", "day", "days", "week", "month", "today",
        "last", "first", "one", "two", "three", "ans", "jour", "mois",
        "semaine", "fois",
    }
)

WORD_PATTERN = re.compile(r"\b[a-zA-ZÀ-ÿ]{5,}\b")

# ── /api/cooccurrence/ ──────────────────────────────────────────
@api_view(["GET"])
def api_cooccurrence(request):
    word = request.GET.get("word", "").lower().strip()

    if not pc.is_ready:
        return Response({"error": "Précalcul en cours, réessayez dans quelques secondes."}, status=503)

    if not word:
        cached = cache.get("cooccurrence_graph")
        if cached:
            return Response(cached)

    top_n = int(request.GET.get("top", 30))

    if word:
        cache_key = f"cooccurrence_word_{word}"
        cached_word = cache.get(cache_key)
        if cached_word:
            return Response(cached_word)

        related = {}
        for (w1, w2), count in pc.cooccur.items():
            if word == w1:
                related[w2] = count
            elif word == w2:
                related[w1] = count

        if not related:
            return Response({"nodes": [], "links": [], "value": 0})

        top_related = sorted(related.items(), key=lambda x: x[1], reverse=True)[:15]
        nodes = [{"id": word, "value": pc.word_freq.get(word, 1)}]
        links = []
        for w, count in top_related:
            nodes.append({"id": w, "value": pc.word_freq.get(w, 1)})
            links.append({"source": word, "target": w, "value": count})

        result = {"nodes": nodes, "links": links, "value": pc.word_freq.get(word, 1)}
        cache.set(cache_key, result, 60 * 60)
        return Response(result)

    # Cas général
    top_words = [w for w, _ in pc.word_freq.most_common(top_n)]
    top_set = set(top_words)
    nodes = [{"id": w, "value": pc.word_freq[w]} for w in top_words]
    links = [
        {"source": w1, "target": w2, "value": count}
        for (w1, w2), count in pc.cooccur.items()
        if w1 in top_set and w2 in top_set
    ]
    result = {"nodes": nodes, "links": links}
    cache.set("cooccurrence_graph", result, 60 * 60)
    return Response(result)
    return Response(result)

# ── /api/radial/ ────────────────────────────────────────────────
@api_view(["GET"])
def api_radial(request):
    cached = cache.get("api_radial")
    if cached:
        return Response(cached)

    word_cat = defaultdict(lambda: defaultdict(int))
    word_total = Counter()

    for title, cat in Article.objects.values_list("title", "category__name"):
        cat = cat or "Unknown"
        if not title:
            continue
        for word in WORD_PATTERN.findall(title.lower()):
            if word not in STOP_WORDS:
                word_cat[word][cat] += 1
                word_total[word] += 1

    top_words = [w for w, _ in word_total.most_common(15)]
    all_cats = list(
        Category.objects.annotate(total=Count("article"))
        .order_by("-total")
        .values_list("name", flat=True)
    )
    result = {
        "words": [
            {
                "word": w,
                "total": word_total[w],
                "by_category": [
                    {"category": cat, "count": word_cat[w].get(cat, 0)} for cat in all_cats
                ],
            }
            for w in top_words
        ],
        "categories": all_cats,
    }

    cache.set("api_radial", result, 60 * 30)  # cache 30 min
    return Response(result)


# ── /api/articles_cooccurrence/ ─────────────────────────────────
@api_view(["GET"])
def api_articles_cooccurrence(request):
    w1 = request.GET.get("w1", "").strip()
    w2 = request.GET.get("w2", "").strip()
    if not w1 or not w2:
        return Response([])
    qs = (
        Article.objects.filter(title__icontains=w1)
        .filter(title__icontains=w2)
        .select_related("category")[:50]
    )
    return Response(ArticleSerializer(qs, many=True).data)


# ── /api/articles/ ──────────────────────────────────────────────
@api_view(["GET"])
def api_articles(request):
    qs = Article.objects.select_related("category", "image").all()
    if request.GET.get("category"):
        qs = qs.filter(category__name__icontains=request.GET["category"])
    if request.GET.get("year"):
        qs = qs.filter(created_at__year=request.GET["year"])
    if request.GET.get("author"):
        qs = qs.filter(author__icontains=request.GET["author"])
    if request.GET.get("q"):
        qs = qs.filter(title__icontains=request.GET["q"])
    return Response(ArticleSerializer(qs[:100], many=True).data)


# ── /api/categories/ ────────────────────────────────────────────
@api_view(["GET"])
def api_categories(request):
    qs = Category.objects.annotate(total=Count("article")).order_by("-total")
    return Response([{"id": c.id_category, "name": c.name, "total": c.total} for c in qs])


# ── /api/images/ ────────────────────────────────────────────────
@api_view(["GET"])
def api_images(request):
    qs = Image.objects.all()
    if request.GET.get("year"):
        qs = qs.filter(year=request.GET["year"])
    return Response(ImageSerializer(qs[:100], many=True).data)


# ── /api/stats/ ─────────────────────────────────────────────────
@api_view(["GET"])
def api_stats(request):
    cached = cache.get("api_stats")
    if cached:
        return Response(cached)

    result = {
        "articles": Article.objects.count(),
        "images": Image.objects.count(),
        "categories": Category.objects.count(),
    }

    cache.set("api_stats", result, 60 * 10)  # cache 10 min
    return Response(result)


# ── /api/covers/ ─────────────────────────────────────────────────
@api_view(["GET"])
def api_covers(request):
    cached = cache.get("api_covers")
    if cached:
        return Response(cached)

    cloud_name = os.environ.get("CLOUDINARY_CLOUD_NAME")
    cat_map = defaultdict(set)
    for row in Article.objects.filter(category__isnull=False).values("image_id", "category_id"):
        cat_map[row["image_id"]].add(row["category_id"])

    images = Image.objects.only(
        "id_image", "filename", "year", "month", "hexadecimal", "hue", "sat", "bri"
    ).order_by("year", "month")

    result = [
        {
            "id": img.id_image,
            "url": f"https://res.cloudinary.com/{cloud_name}/image/upload/wave_cover/{img.filename}.jpg",
            "year": img.year,
            "month": img.month,
            "hex": img.hexadecimal or "#cccccc",
            "hue": img.hue,
            "sat": img.sat,
            "bri": img.bri,
            "categories": list(cat_map.get(img.id_image, [])),
        }
        for img in images
    ]

    cache.set("api_covers", result, 60 * 30)  # cache 30 min
    return Response(result)


# ── /api/colors/ ────────────────────────────────────────────────
@api_view(["GET"])
def api_colors(request):
    category = request.GET.get("category", "")
    cache_key = f"api_colors_{category}"

    cached = cache.get(cache_key)
    if cached:
        return Response(cached)

    qs = Image.objects.all()
    if category:
        qs = qs.filter(article__category__name__icontains=category)
    colors = list(qs.values("hexadecimal").annotate(total=Count("id_image")).order_by("-total")[:20])

    cache.set(cache_key, colors, 60 * 30)  # cache 30 min
    return Response(colors)


# ── /api/heatmap/ ────────────────────────────────────────────────
@api_view(["GET"])
def api_heatmap(request):
    mode = request.GET.get("mode", "words")
    cache_key = f"api_heatmap_{mode}"

    cached = cache.get(cache_key)
    if cached:
        return Response(cached)

    years = list(range(1993, 2026))
    years_labels = [str(y) for y in years]

    if mode == "categories":
        rows_qs = (
            Article.objects.values("category__name", "image__year")
            .annotate(total=Count("id_articles"))
            .order_by("category__name", "image__year")
        )
        map_ = defaultdict(lambda: defaultdict(int))
        for r in rows_qs:
            map_[r["category__name"] or "Unknown"][r["image__year"]] = r["total"]
        top = (
            Article.objects.values("category__name")
            .annotate(total=Count("id_articles"))
            .order_by("-total")[:50]
        )
        rows = [r["category__name"] for r in top if r["category__name"]]

    elif mode == "authors":
        rows_qs = (
            Article.objects.values("author", "image__year")
            .annotate(total=Count("id_articles"))
            .order_by("author", "image__year")
        )
        map_ = defaultdict(lambda: defaultdict(int))
        for r in rows_qs:
            map_[r["author"] or "Unknown"][r["image__year"]] = r["total"]
        top = (
            Article.objects.values("author")
            .annotate(total=Count("id_articles"))
            .order_by("-total")[:50]
        )
        rows = [r["author"] for r in top if r["author"]]

    else:  # words
        word_year = defaultdict(lambda: defaultdict(int))
        word_total = Counter()
        for title, year in Article.objects.values_list("title", "image__year"):
            if not year or not title:
                continue
            for word in WORD_PATTERN.findall(title.lower()):
                if word not in STOP_WORDS:
                    word_year[word][year] += 1
                    word_total[word] += 1
        rows = [w for w, _ in word_total.most_common(50)]
        data = [[word_year[row][y] for y in years] for row in rows]
        result = {"rows": rows, "cols": years_labels, "data": data, "mode": mode}
        cache.set(cache_key, result, 60 * 30)
        return Response(result)

    data = [[map_[row][y] for y in years] for row in rows]
    result = {"rows": rows, "cols": years_labels, "data": data, "mode": mode}
    cache.set(cache_key, result, 60 * 30)  # cache 30 min
    return Response(result)


# ── /api/color-analysis/ ────────────────────────────────────────
@api_view(["GET"])
def api_color_analysis(request):
    import colorsys
    import traceback

    cached = cache.get("api_color_analysis")
    if cached:
        return Response(cached)

    cloud_name = os.environ.get("CLOUDINARY_CLOUD_NAME")

    try:
        images = (
            Image.objects.exclude(hexadecimal__isnull=True)
            .exclude(hexadecimal__exact="")
            .values("hexadecimal", "year", "filename")[:5000]
        )
        result = []
        for img in images:
            hex_color = img["hexadecimal"].strip().lstrip("#")
            if len(hex_color) != 6:
                continue
            try:
                r, g, b = (int(hex_color[i: i + 2], 16) / 255 for i in (0, 2, 4))
                h, s, v = colorsys.rgb_to_hsv(r, g, b)
                result.append({
                    "hex": "#" + hex_color,
                    "year": img["year"],
                    "hue": round(h * 360, 1),
                    "saturation": round(s * 100, 1),
                    "brightness": round(v * 100, 1),
                    "cover_url": (
                        f"https://res.cloudinary.com/{cloud_name}/image/upload/wave_cover/{img['filename']}.jpg"
                        if img["filename"] else None
                    ),
                })
            except Exception as e:
                continue

        cache.set("api_color_analysis", result, 60 * 30)  # cache 30 min
        return Response(result)

    except Exception:
        traceback.print_exc()
        return Response({"error": "server error"}, status=500)


# ── /api/cover-words/ ───────────────────────────────────────────
@api_view(["GET"])
def api_cover_words(request):
    year = request.GET.get("year")
    month = request.GET.get("month")
    if not year or not month:
        return Response({"error": "year and month required"}, status=400)

    cache_key = f"api_cover_words_{year}_{month}"
    cached = cache.get(cache_key)
    if cached:
        return Response(cached)

    image = Image.objects.filter(year=year, month=month).first()
    words_data = []

    if image and image.words:
        raw_words = WORD_PATTERN.findall(image.words.lower())
        freq = Counter(w for w in raw_words if w not in STOP_WORDS).most_common(40)
        words_data = [{"name": w, "value": c} for w, c in freq]

    if not words_data:
        all_words = []
        for title in Article.objects.filter(
            created_at__year=year, created_at__month=month
        ).values_list("title", flat=True):
            if title:
                filtered = (w for w in WORD_PATTERN.findall(title.lower()) if w not in STOP_WORDS)
                all_words.extend(filtered)
        words_data = [{"name": w, "value": c} for w, c in Counter(all_words).most_common(40)]

    result = {
        "year": year,
        "month": month,
        "cover_url": f"/media/wave_cover/{image.filename}" if image else "",
        "words": words_data,
    }

    cache.set(cache_key, result, 60 * 30)  # cache 30 min
    return Response(result)