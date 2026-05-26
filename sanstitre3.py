#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 01:09:09 2026

@author: kossi
"""

import json

with open('wave_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

def clean(obj):
    if isinstance(obj, str):
        return obj.replace('\x00', '')  # or replace with ' ' if preferred
    if isinstance(obj, list):
        return [clean(i) for i in obj]
    if isinstance(obj, dict):
        return {k: clean(v) for k, v in obj.items()}
    return obj

cleaned = clean(data)

with open('wave_data_clean.json', 'w', encoding='utf-8') as f:
    json.dump(cleaned, f, ensure_ascii=False, indent=2)

print("Done.")