#!/usr/bin/env python3
"""Converte os PNG do dia em JPEG (a API da Meta só aceita JPEG). Uso: python3 to_jpg.py AAAA-MM-DD"""
import sys, glob, os
from PIL import Image
d = sys.argv[1]
n = 0
for f in glob.glob(f"../{d}/**/*.png", recursive=True):
    if "grupos" in f: continue
    Image.open(f).convert("RGB").save(f[:-4] + ".jpg", "JPEG", quality=92, optimize=True)
    n += 1
print(f"{n} JPEG gerados em {d}")
