import os
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

VARYANTLAR = ["baseline", "A", "B", "C"]
SEEDLER = range(5)
ISIM = {"baseline": "baseline (kural yok)", "A": "A (zaman cezası)", "B": "B (hile kuralı)", "C": "C (düzeltilmiş)"}
RENK = {"baseline": "#0072B2", "A": "#E69F00", "B": "#D55E00", "C": "#009E73"}  # renk körlüğüne uygun

# ---- değerlendirme verisi ----
ev = {}
for v in VARYANTLAR:
    for s in SEEDLER:
        f = f"results/{v}_seed{s}_eval.csv"
        if s == 0:
            f = f"results/{v}_eval.csv"  # seed 0: Asama 2 degerlendirmesi (v2 formati: zaman asimi sutunlari var)
        if os.path.exists(f):
            ev[(v, s)] = pd.read_csv(f)
eksik = [(v, s) for v in VARYANTLAR for s in SEEDLER if (v, s) not in ev]

rows = []
for (v, s), d in ev.items():
    rows.append(dict(varyant=v, seed=s, ort=d.skor.mean(), std=d.skor.std(ddof=0), basari=100 * (d.skor > 200).mean(),
                     uzunluk=d.uzunluk.mean(), zaman_asimi=int(d.truncated.sum()), iki_bacak=int(d.iki_bacak_yerde.sum())))
T = pd.DataFrame(rows).sort_values(["varyant", "seed"], key=lambda c: c.map({k: i for i, k in enumerate(VARYANTLAR)}) if c.name == "varyant" else c)

with open("results/ozet_seed_tablosu.md", "w", encoding="utf-8") as f:
    f.write("# Seed tablosu (her seed için 100 deneme, wrapper YOK, oyunun kendi ödülü)\n\n")
    f.write("| varyant | seed | ort. skor | std | başarı % (skor>200) | ort. uzunluk | zaman aşımı | iki bacak yerde |\n|---|---|---|---|---|---|---|---|\n")
    for _, r in T.iterrows():
        f.write(f"| {r.varyant} | {r.seed} | {r.ort:.1f} | {r['std']:.1f} | {r.basari:.0f} | {r.uzunluk:.0f} | {r.zaman_asimi} | {r.iki_bacak} |\n")
    if eksik:
        f.write(f"\nEKSİK: {eksik}\n")

with open("results/ozet_varyant_tablosu.md", "w", encoding="utf-8") as f:
    f.write("# Varyant tablosu (5 seed; seed başına 100 deneme)\n\n")
    f.write("| varyant | seed sayısı | ortalamaların ort. | seed'ler arası std (ddof=1) | en düşük seed ort. | en yüksek seed ort. | toplam zaman aşımı | ort. uzunluk |\n|---|---|---|---|---|---|---|---|\n")
    for v in VARYANTLAR:
        t = T[T.varyant == v]
        if len(t) == 0:
            continue
        sd = t.ort.std(ddof=1) if len(t) > 1 else float("nan")
        f.write(f"| {v} | {len(t)} | {t.ort.mean():.1f} | {sd:.1f} | {t.ort.min():.1f} | {t.ort.max():.1f} | {t.zaman_asimi.sum()} / {100*len(t)} | {t.uzunluk.mean():.0f} |\n")
    if eksik:
        f.write(f"\nEKSİK: {eksik}\n")

# ---- eğitim eğrileri (gerçek skor, monitor.csv) ----
GRID = np.linspace(20_000, 1_000_000, 200)
fig, ax = plt.subplots(figsize=(10, 6))
for v in VARYANTLAR:
    egriler = []
    for s in SEEDLER:
        f = f"results/{v}_seed{s}/monitor.csv"
        if not os.path.exists(f):
            continue
        d = pd.read_csv(f, skiprows=1)
        adim = d.l.cumsum().values
        hm = d.r.rolling(100, min_periods=20).mean().values
        egriler.append(np.interp(GRID, adim, hm, left=np.nan, right=np.nan))
    if not egriler:
        continue
    E = np.array(egriler)
    ax.plot(GRID, np.nanmean(E, axis=0), color=RENK[v], label=f"{ISIM[v]} ({len(E)} seed)", lw=2)
    ax.fill_between(GRID, np.nanmin(E, axis=0), np.nanmax(E, axis=0), color=RENK[v], alpha=0.18)
ax.set_xlabel("Eğitim adımı"); ax.set_ylabel("Oyunun gerçek skoru (100 denemelik hareketli ortalama)")
ax.set_title("Eğitim eğrileri: çizgi = seed ortalaması, gölge = en düşük–en yüksek seed")
ax.axhline(200, color="gray", ls="--", lw=1); ax.legend(loc="lower right"); ax.grid(alpha=0.3)
fig.tight_layout(); fig.savefig("results/egitim_egrileri.png", dpi=130); plt.close(fig)

# ---- kutu grafiği ----
fig, ax = plt.subplots(figsize=(9, 6))
veri, etik = [], []
for v in VARYANTLAR:
    ds = [ev[(v, s)].skor.values for s in SEEDLER if (v, s) in ev]
    if ds:
        veri.append(np.concatenate(ds)); etik.append(f"{v}\n({len(ds)} seed)")
bp = ax.boxplot(veri, tick_labels=etik, patch_artist=True, showfliers=True)
for patch, v in zip(bp["boxes"], [x for x in VARYANTLAR if any((x, s) in ev for s in SEEDLER)]):
    patch.set_facecolor(RENK[v]); patch.set_alpha(0.45)
for i, v in enumerate([x for x in VARYANTLAR if any((x, s) in ev for s in SEEDLER)], start=1):
    for s in SEEDLER:
        if (v, s) in ev:
            ax.scatter(i + (s - 2) * 0.06, ev[(v, s)].skor.mean(), color="black", zorder=3, s=28)
ax.scatter([], [], color="black", s=28, label="her nokta = bir seed'in ortalaması")
ax.axhline(200, color="gray", ls="--", lw=1)
ax.set_ylabel("Skor (wrapper kapalı)"); ax.set_title("Değerlendirme: kutu = tüm denemeler (seed başına 100), nokta = seed ortalaması")
ax.legend(loc="lower right"); ax.grid(alpha=0.3)
fig.tight_layout(); fig.savefig("results/degerlendirme_kutu.png", dpi=130); plt.close(fig)

# ---- zaman aşımı ----
fig, ax = plt.subplots(figsize=(9, 5.5))
w = 0.16
for j, s in enumerate(SEEDLER):
    vals = [int(T[(T.varyant == v) & (T.seed == s)].zaman_asimi.sum()) if ((T.varyant == v) & (T.seed == s)).any() else 0 for v in VARYANTLAR]
    ax.bar(np.arange(4) + (j - 2) * w, vals, width=w, label=f"seed {s}", color=plt.cm.viridis(j / 4))
ax.set_xticks(range(4)); ax.set_xticklabels([ISIM[v] for v in VARYANTLAR])
ax.set_ylabel("Zaman aşımı sayısı (100 denemeden)"); ax.set_title("Havada asılı kalma: 1000 adımda bitmeyen denemeler")
ax.legend(); ax.grid(axis="y", alpha=0.3)
fig.tight_layout(); fig.savefig("results/zaman_asimi.png", dpi=130); plt.close(fig)
print("tamam; eksik:", eksik)
