#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 21:19:39 2026

@author: kossi
"""

import json
from collections import Counter

with open("wired_data.json", "r") as f:
    data = json.load(f)

categories = []
for image in data:
    for article in image.get("Articles", []):
        cat = article.get("category")
        if cat:
            categories.append(cat)

compteur = Counter(categories)

print(f"Total catégories uniques : {len(compteur)}")
print("\nListe des catégories :")
for cat, nb in compteur.most_common():
    print(f"  {cat} → {nb} articles")