#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 20:57:14 2026

@author: kossi
"""

import json
from collections import Counter

# Charge ton fichier 
with open("wired_data.json", "r") as f:
    data = json.load(f)

# Récupère tous les auteurs
auteurs = []
for image in data:
    for article in image.get("Articles", []):  # ← .get() évite le KeyError
        if article.get("author"):  # évite les valeurs null
            auteurs.append(article["author"])

# Compte les occurrences
compteur = Counter(auteurs)

# Affiche les auteurs avec plusieurs articles
print("Auteurs ayant écrit plusieurs articles :")
for auteur, nb in compteur.most_common():
    if nb > 1:
        print(f"  {auteur} → {nb} articles")

print(f"\nTotal auteurs uniques : {len(compteur)}")
print(f"Total articles : {len(auteurs)}")