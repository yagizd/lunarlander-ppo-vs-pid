"""README.md / REPORT.md / OZET_TR.md icindeki her sayinin docs/sayilar.json'da (veya beyaz listede) bulundugunu kontrol eder."""
import json, re, sys

S = json.load(open("docs/sayilar.json"))
vals = []
def topla(o):
    if isinstance(o, dict): [topla(v) for v in o.values()]
    elif isinstance(o, list): [topla(v) for v in o]
    elif isinstance(o, (int, float)) and not isinstance(o, bool): vals.append(float(o))
topla(S)
izinli = set()
for v in [abs(x) for x in vals] + vals:
    for fmt in (".0f", ".1f", ".2f"):
        izinli.add(f"{v:{fmt}}")
    if v == int(v): izinli.add(str(int(v)))
# protokol sabitleri ve surum numaralari (sayilar.json disinda, kodda/protokolde tanimli)
BEYAZ = set("0 1 2 3 4 5 6 7 8 9 10 20 30 50 64 100 200 500 1000 1099 1100 1599 1000000 50000 0.2 0.5 0.05 0.1 99 13 3.13 11 2017 3 4 8 1.4 0.0 1.0 2.0".split())
yanlis = []
for dosya in ("README.md", "REPORT.md", "OZET_TR.md"):
    t = open(dosya, encoding="utf-8").read()
    t = re.sub(r"```.*?```", " ", t, flags=re.S)       # kod bloklari
    t = re.sub(r"`[^`]*`", " ", t)                      # satir ici kod
    t = re.sub(r"\(https?://[^)]*\)|\]\([^)]*\)", " ", t)  # baglantilar / resim yollari
    t = re.sub(r"\d+\.\d+\.\d+", " ", t)                # surumler
    t = re.sub(r"[A-Za-z_]+\d+[A-Za-z_]*", " ", t)      # kimlikler (ppo_A_seed0, python3)
    for m in re.finditer(r"(?<![\w.])-?\d+(?:\.\d+)?", t):
        n = m.group(0).lstrip("-")
        if n not in izinli and n not in BEYAZ:
            baglam = t[max(0, m.start() - 40): m.end() + 20].replace("\n", " ")
            yanlis.append((dosya, n, baglam))
for y in yanlis: print("SAYI JSON'DA YOK:", y)
print("TAMAM: tum sayilar sayilar.json'da" if not yanlis else f"{len(yanlis)} uyusmayan sayi")
sys.exit(1 if yanlis else 0)
