from django.test import TestCase, Client
from django.urls import reverse
from kobe_wave.models import Article, Image, Category


class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Science")

    def test_category_creation(self):
        self.assertEqual(self.category.name, "Science")

    def test_category_str(self):
        self.assertEqual(str(self.category), "Science")


class ImageModelTest(TestCase):
    def setUp(self):
        self.image = Image.objects.create(
            filename="test.jpg",
            year=2023,
            month=6,
            words="test words",
            rgb="255,0,0",
            hsl="0,100%,50%",
            hexadecimal="#FF0000",
            red=255,
            green=0,
            blue=0,
            hue=0,
            sat=100,
            bri=50,
        )

    def test_image_creation(self):
        self.assertEqual(self.image.filename, "test.jpg")

    def test_image_str(self):
        self.assertEqual(str(self.image), "test.jpg")


class ArticleModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Tech")
        self.image = Image.objects.create(
            filename="article.jpg",
            year=2023,
            month=1,
            words="words",
            rgb="0,0,0",
            hsl="0,0%,0%",
            hexadecimal="#000000",
            red=0,
            green=0,
            blue=0,
            hue=0,
            sat=0,
            bri=0,
        )
        self.article = Article.objects.create(
            title="Test Article",
            url="https://example.com",
            author="John",
            image=self.image,
            category=self.category,
        )

    def test_article_creation(self):
        self.assertEqual(self.article.title, "Test Article")

    def test_article_str(self):
        self.assertEqual(str(self.article), "Test Article")

    def test_article_str_no_title(self):
        self.article.title = None
        self.assertEqual(str(self.article), self.article.url)


class PageViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_page(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_contact_page(self):
        response = self.client.get(reverse("contact"))
        self.assertEqual(response.status_code, 200)

    def test_article_list_page(self):
        response = self.client.get(reverse("article_list"))
        self.assertEqual(response.status_code, 200)

    def test_image_list_page(self):
        response = self.client.get(reverse("image_list"))
        self.assertEqual(response.status_code, 200)

    def test_dashboard_page(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)

    def test_404_page(self):
        response = self.client.get("/page-inexistante/")
        self.assertEqual(response.status_code, 404)


class ApiViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_api_articles(self):
        response = self.client.get(reverse("api_articles"))
        self.assertEqual(response.status_code, 200)

    def test_api_categories(self):
        response = self.client.get(reverse("api_categories"))
        self.assertEqual(response.status_code, 200)

    def test_api_stats(self):
        response = self.client.get(reverse("api_stats"))
        self.assertEqual(response.status_code, 200)
