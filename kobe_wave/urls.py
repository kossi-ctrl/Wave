from django.urls import path
from kobe_wave import views, api_views

urlpatterns = [
    # Pages
    path("", views.HomeView.as_view(), name="home"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("articles/", views.ArticleListView.as_view(), name="article_list"),
    path("articles/<int:pk>/", views.ArticleDetailView.as_view(), name="article_detail"),
    path("images/", views.ImageListView.as_view(), name="image_list"),
    path("categories/<int:pk>/", views.CategoryDetailView.as_view(), name="category_detail"),
    path("imaginaries/", views.imaginaries, name="imaginaries"),
    path("explore/", views.explore, name="explore"),
    # API
    path("api/articles/", api_views.api_articles, name="api_articles"),
    path("api/categories/", api_views.api_categories, name="api_categories"),
    path("api/images/", api_views.api_images, name="api_images"),
    path("api/stats/", api_views.api_stats, name="api_stats"),
    path("api/colors/", api_views.api_colors, name="api_colors"),
    path("wiredviz/", views.wiredviz, name="wiredviz"),
    path("api/radial/", api_views.api_radial, name="api_radial"),
    path("api/heatmap/", api_views.api_heatmap, name="api_heatmap"),
    path("api/color-analysis/", api_views.api_color_analysis, name="api_color_analysis"),
    path("api/cooccurrence/", api_views.api_cooccurrence, name="api_cooccurrence"),
    path("covers/", views.covers, name="covers"),
    path("api/covers/", api_views.api_covers, name="api_covers"),
    path("api/cover-words/", api_views.api_cover_words, name="api_cover_words"),
    path("test-404/", views.test_404, name="test_404"),
    path("test-500/", views.test_500, name="test_500"),
    path("legal/", views.legal, name="legal"),
    path("credits/", views.credits, name="credits"),
    path("contact/", views.contact, name="contact"),
    path("project/", views.project, name="project"),
    path("data/", views.data, name="data"),
    path("timeline/", views.timeline, name="timeline"),
    path(
        "api/articles-cooccurrence/",
        api_views.api_articles_cooccurrence,
        name="api_articles_cooccurrence",
    ),
]
