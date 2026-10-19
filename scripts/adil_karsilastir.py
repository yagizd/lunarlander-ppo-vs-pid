"""Adim 4 tablosu ve grafigi. Tum sayilar results/ dosyalarindan okunur (hafizadan yazilmaz)."""
import numpy as np, pandas as pd, json
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

def ppo_seedler(yollar):
    return [pd.read_csv(y) for y in yollar]

gruplar = {
    "PPO varsayılan ayar (seed 0-4)": ppo_seedler([f"results/baseline_eval.csv"] + [f"results/baseline_seed{s}_eval.csv" for s in range(1, 5)]),
    "PPO ayarlı (16 ayardan seçilen, seed 10-14)": ppo_seedler([f"results/ayar_ppo/kazanan_seed{s}_eval.csv" for s in range(10, 15)]),
}
tek = {"PID (200 ayar)": pd.read_csv("results/pid_eval.csv"), "Gymnasium heuristic": pd.read_csv("results/heuristic_eval.csv")}
rast = pd.read_csv("results/rastgele.csv")

satir, nokta = [], {}
for ad, ds in gruplar.items():
    ort = np.array([d.skor.mean() for d in ds]); tum = pd.concat(ds); nokta[ad] = ort
    satir.append((ad, f"{ort.mean():.1f} ± {ort.std(ddof=1):.1f}", f"{tum.skor.std(ddof=0):.1f}", f"%{100*(tum.skor>200).mean():.1f}",
                  f"{tum.uzunluk.mean():.0f}", f"{int(tum.truncated.sum())} / {len(tum)}", f"{ort.min():.1f} – {ort.max():.1f}"))
for ad, d in tek.items():
    nokta[ad] = np.array([d.skor.mean()])
    satir.append((ad, f"{d.skor.mean():.1f} (tek kontrolcü)", f"{d.skor.std(ddof=0):.1f}", f"%{100*(d.skor>200).mean():.1f}", f"{d.uzunluk.mean():.0f}", f"{int(d.truncated.sum())} / {len(d)}", "–"))
nokta["Rastgele ajan"] = np.array([rast.skor.mean()])
satir.append(("Rastgele ajan", f"{rast.skor.mean():.1f} (tek ölçüm)", f"{rast.skor.std(ddof=0):.1f}", f"%{100*(rast.skor>200).mean():.1f}", "–", "–", "–"))

with open("results/ayar_ppo/adil_karsilastirma.md", "w", encoding="utf-8") as f:
    f.write("# Adil karşılaştırma (Bütçe A: PPO'ya 16 ayar)\n\nHepsi: wrapper kapalı, oyunun kendi skoru, deterministik, 100 bölüm, başlangıç seed 1000-1099.\n"
            "PPO satırlarında 'ortalama ± std' = 5 seed'in ortalamalarının ortalaması ± seed'ler arası std (ddof=1). 'std (bölümler)' = tüm bölümlerin skor yayılımı.\n\n")
    f.write("| yöntem | ortalama skor | std (bölümler) | başarı (skor>200) | ort. uzunluk | zaman aşımı | en düşük – en yüksek seed ort. |\n|---|---|---|---|---|---|---|\n")
    for r in satir: f.write("| " + " | ".join(r) + " |\n")
    f.write("\nPID ek 500 bölüm (seed 1100-1599, ayrı dosya): ort %.1f. Ayarlı PPO için ek 500 bölüm çalıştırılmadı.\n" % pd.read_csv("results/pid_eval_ek500.csv").skor.mean())
    kz = json.load(open("results/ayar_ppo/secim_kazanan.json"))
    f.write(f"\nSeçim: ayar {kz['kazanan_id']} (tuning seed 0-99'da ortalama {[t for t in kz['tablo'] if t['id']==kz['kazanan_id']][0]['ort']:.1f}). Eski/yeni sonuç dosyaları: results/baseline*_eval.csv, results/ayar_ppo/kazanan_seed*_eval.csv.\n")

renk = ["#0072B2", "#E69F00", "#009E73", "#CC79A7", "#999999"]
fig, ax = plt.subplots(figsize=(11, 6)); ad = list(nokta)
for i, a in enumerate(ad):
    ax.bar(i, nokta[a].mean(), color=renk[i], alpha=0.6, width=0.6)
    if len(nokta[a]) > 1: ax.scatter([i + (j - 2) * 0.08 for j in range(5)], nokta[a], color="black", zorder=3, s=26)
ax.scatter([], [], color="black", s=26, label="PPO: her nokta = bir seed'in ortalaması")
ax.axhline(200, color="gray", ls="--", lw=1); ax.axhline(0, color="black", lw=0.8)
ax.set_xticks(range(len(ad))); ax.set_xticklabels([a.replace(" (", "\n(") for a in ad], fontsize=8.5)
ax.set_ylabel("Ortalama skor (100 bölüm, seed 1000-1099)"); ax.set_title("Adil karşılaştırma (bütçe A): PPO'ya 16 ayar, PID'e 200 ayar")
ax.legend(loc="upper right"); ax.grid(axis="y", alpha=0.3)
fig.tight_layout(); fig.savefig("results/ayar_ppo/adil_karsilastirma.png", dpi=130)
print(open("results/ayar_ppo/adil_karsilastirma.md", encoding="utf-8").read())
