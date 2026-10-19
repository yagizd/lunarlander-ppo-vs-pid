"""Kisi adi taramasi (buyuk/kucuk harf, ASCII ve Turkce yazim; desen asagida). Sadece GitHub'a gidecek metin dosyalari."""
import os, re, sys, glob
rg = re.compile(r"y[aâ][gğ][iıİI]z", re.I)
dosyalar = ["README.md", "REPORT.md", "OZET_TR.md", "ROADMAP.md", ".gitignore"]
dosyalar += [f for f in glob.glob("requirements*.txt")]
for kok in ("docs", "scripts", "results"):
    for r, ds, fs in os.walk(kok):
        ds[:] = [d for d in ds if d not in ("_gecici", "__pycache__", "kareler")]
        for f in fs:
            p = os.path.join(r, f).replace("\\", "/")
            if kok == "results" and not f.endswith((".md", ".json")): continue   # results: sadece .md ve .json (talimat)
            if f.endswith((".png", ".gif", ".mp4", ".zip", ".pyc")): continue
            if p.endswith((".bak",)): continue
            dosyalar.append(p)
n = 0
for p in sorted(set(dosyalar)):
    if not os.path.exists(p) or p.endswith(".bak"): continue
    try: satirlar = open(p, encoding="utf-8").read().splitlines()
    except Exception: continue
    for i, s in enumerate(satirlar, 1):
        if rg.search(s): print(f"{p}\t{i}\t{s}"); n += 1
print("TOPLAM", n, "satir; taranan dosya", len(set(dosyalar)))
