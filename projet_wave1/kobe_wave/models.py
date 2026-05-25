import os
from django.db import models
from django.db.models import UniqueConstraint, CheckConstraint, Q


class Category(models.Model):
    id_category = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)

    class Meta:
        db_table = "category"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Image(models.Model):
    id_image = models.AutoField(primary_key=True)
    filename = models.CharField(max_length=200, unique=True)
    year = models.IntegerField()
    month = models.IntegerField()
    words = models.TextField()
    rgb = models.CharField(max_length=200)
    hsl = models.CharField(max_length=200)
    hexadecimal = models.CharField(max_length=7)
    red = models.IntegerField()
    green = models.IntegerField()
    blue = models.IntegerField()
    hue = models.IntegerField()
    sat = models.IntegerField()
    bri = models.IntegerField()

    class Meta:
        db_table = "image"
        ordering = ["-year", "-month"]
        constraints = [
            UniqueConstraint(
                fields=["filename", "year", "month"], name="unique_image_filename_year_month"
            ),
            CheckConstraint(
                condition=Q(month__gte=1) & Q(month__lte=12), name="check_month_valide"
            ),
            CheckConstraint(condition=Q(year__gte=1900), name="check_year_valide"),
            CheckConstraint(condition=Q(red__gte=0) & Q(red__lte=255), name="check_red_valide"),
            CheckConstraint(
                condition=Q(green__gte=0) & Q(green__lte=255), name="check_green_valide"
            ),
            CheckConstraint(condition=Q(blue__gte=0) & Q(blue__lte=255), name="check_blue_valide"),
            CheckConstraint(condition=Q(hue__gte=0) & Q(hue__lte=360), name="check_hue_valide"),
            CheckConstraint(condition=Q(sat__gte=0) & Q(sat__lte=100), name="check_sat_valide"),
            CheckConstraint(condition=Q(bri__gte=0) & Q(bri__lte=100), name="check_bri_valide"),
        ]

    def __str__(self):
        return self.filename

    @property
    def cover_url(self):
        cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME')
        return f"https://res.cloudinary.com/{dtkw6dnfa}/image/upload/wave_cover/{self.filename}"


class Article(models.Model):
    id_articles = models.AutoField(primary_key=True)
    title = models.CharField(max_length=500, null=True, blank=True)
    url = models.URLField(max_length=500)
    author = models.CharField(max_length=200, null=True, blank=True)
    image = models.ForeignKey(Image, on_delete=models.CASCADE, db_column="id_image", db_index=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, db_column="id_category"
    )
    created_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "articles"
        ordering = ["title"]
        constraints = [UniqueConstraint(fields=["url"], name="unique_article_url")]

    def __str__(self):
        return self.title if self.title else self.url