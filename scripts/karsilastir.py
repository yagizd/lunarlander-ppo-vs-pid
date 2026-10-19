import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

def oku(v, s):
    f = f"results/{v}_eval.csv" if s == 0 else f"results/{v}_seed{s}_eval.csv"
    return pd.read_csv(f)

satirlar, nokta = [], {}
for v, ad in (("baseline", "PPO baseline"), ("A", "PPO A (zaman cezası)"), ("C", "PPO C (düzeltilmiş)")):
    ds = [oku(v, s) for s in range(5)]
    ort = np.array([d.skor.mean() for d in ds]); tum = pd.concat(ds)
    nokta[ad] = ort
    satirlar.append((ad, f"{ort.mean():.1f} ± {ort.std(ddof=1):.1f} (seed'ler arası)", f"{tum.skor.std(ddof=0):.1f}",
                     f"%{100*(tum.skor>200).mean():.1f} (500 denemede)", f"{tum.uzunluk.mean():.0f}", f"{int(tum.truncated.sum())} / 500"))
for v, ad in (("pid", "PID (dondurulmuş)"), ("heuristic", "Gymnasium heuristic (hazır referans)")):
    d = pd.read_csv(f"results/{v}_eval.csv"); nokta[ad] = np.array([d.skor.mean()])
    satirlar.append((ad, f"{d.skor.mean():.1f} (tek kontrolcü)", f"{d.skor.std(ddof=0):.1f}", f"%{100*(d.skor>200).mean():.0f} (100 denemede)",
                     f"{d.uzunluk.mean():.0f}", f"{int(d.truncated.sum())} / 100"))
with open("results/pid_vs_ppo_tablo.md", "w", encoding="utf-8") as f:
    f.write("# PID ve PPO karşılaştırması (hepsi: oyunun kendi ödülü, wrapper yok, seed 1000-1099)\n\n")
    f.write("| yöntem | ortalama skor | std (denemeler arası) | başarı oranı (skor>200) | ort. uzunluk | zaman aşımı |\n|---|---|---|---|---|---|\n")
    for r in satirlar: f.write("| " + " | ".join(r) + " |\n")
    f.write("\nNot: PPO satırları 5 seed (5 ayrı eğitim) × 100 deneme. PID ve heuristic tek kontrolcü × 100 deneme. "
            "PPO B (bilerek bozuk kural) tabloya konmadı; sonuçları Aşama 3'te.\n")
    ek = []
    for v in ("pid", "heuristic"):
        d = pd.read_csv(f"results/{v}_eval_ek500.csv")
        ek.append(f"- {v}, ek 500 deneme (seed 1100-1599): ort {d.skor.mean():.1f}, std {d.skor.std(ddof=0):.1f}, başarı %{100*(d.skor>200).mean():.1f}, zaman aşımı {int(d.truncated.sum())}")
    f.write("\n## Ek güven (ana karşılaştırmayı değiştirmez)\n" + "\n".join(ek) + "\n")

renk = ["#0072B2", "#E69F00", "#009E73", "#CC79A7", "#56B4E9"]
fig, ax = plt.subplots(figsize=(10, 6))
ad = list(nokta)
for i, a in enumerate(ad):
    ax.bar(i, nokta[a].mean(), color=renk[i], alpha=0.6, width=0.6)
    if len(nokta[a]) > 1:
        ax.scatter([i + (j - 2) * 0.08 for j in range(5)], nokta[a], color="black", zorder=3, s=26)
ax.scatter([], [], color="black", s=26, label="PPO: her nokta = bir seed'in ortalaması")
ax.set_xticks(range(len(ad))); ax.set_xticklabels([a.replace(" (", "\n(") for a in ad], fontsize=9)
ax.axhline(200, color="gray", ls="--", lw=1); ax.set_ylim(0, 300)
ax.set_ylabel("Ortalama skor (100 deneme)"); ax.set_title("PID ve PPO: oyunun kendi skoru (eksen 0'dan başlıyor)")
ax.legend(loc="lower right"); ax.grid(axis="y", alpha=0.3)
fig.tight_layout(); fig.savefig("results/pid_vs_ppo.png", dpi=130)
print(open("results/pid_vs_ppo_tablo.md", encoding="utf-8").read())
