#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 00:15:46 2026

@author: kossi
"""

import json

# ⚠️ Remplace par le nom de ton application Django
APP_NAME = "kobe_wave"

with open("wired_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

categories_fixtures = []
images_fixtures = []
articles_fixtures = []

article_pk = 1
category_cache = {}
category_pk = 1

# --- 1ère passe : collecte toutes les catégories ---
for item in data:
    for article in item.get("Articles", []):
        cat_name = article.get("category")
        if cat_name and cat_name not in category_cache:
            category_cache[cat_name] = category_pk
            categories_fixtures.append({
                "model": f"{APP_NAME}.category",
                "pk": category_pk,
                "fields": {
                    "name": cat_name
                }
            })
            category_pk += 1

# --- 2ème passe : images et articles ---
for item in data:
    # IMAGE
    images_fixtures.append({
        "model": f"{"kobe_wave"}.image",
        "pk": item["id"],
        "fields": {
            "filename": item["filename"],
            "year": item["year"],
            "month": item["month"],
            "words": item["words"],
            "rgb": item["Colors"]["RGB"],
            "hsl": item["Colors"]["HSL"],
            "hexadecimal": item["Colors"]["Hexadecimal"],
            "red": item["Colors"]["Red"],
            "green": item["Colors"]["Green"],
            "blue": item["Colors"]["Blue"],
            "hue": item["Colors"]["Hue"],
            "sat": item["Colors"]["Sat"],
            "bri": item["Colors"]["Bri"],
        }
    })

    # ARTICLES
    for article in item.get("Articles", []):
        cat_name = article.get("category")
        cat_id = category_cache.get(cat_name) if cat_name else None

        articles_fixtures.append({
            "model": f"{APP_NAME}.article",
            "pk": article_pk,
            "fields": {
                "title": article.get("title", ""),
                "url": article.get("url", ""),
                "author": article.get("author"),
                "image": item["id"],
                "category": cat_id,
            }
        })
        article_pk += 1

# Ordre important : category → image → article
fixtures = categories_fixtures + images_fixtures + articles_fixtures

with open("fixture_wired.json", "w", encoding="utf-8") as f:
    json.dump(fixtures, f, ensure_ascii=False, indent=2)

print(f"✅ Fixture générée avec succès !")
print(f"   - {len(categories_fixtures)} catégories")
print(f"   - {len(images_fixtures)} images")
print(f"   - {len(articles_fixtures)} articles")