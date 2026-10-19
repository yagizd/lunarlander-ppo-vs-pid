"""README/REPORT icin TUM sayilari results/ dosyalarindan okuyup docs/sayilar.json'a yazar."""
import glob, json, os, re
import numpy as np, pandas as pd

V = ["baseline", "A", "B", "C"]


def ev(v, s):
    return pd.read_csv(f"results/{v}_eval.csv" if s == 0 else f"results/{v}_seed{s}_eval.csv")


def ozet(d):
    return dict(ort=float(d.skor.mean()), std=float(d.skor.std(ddof=0)), basari=float(100 * (d.skor > 200).mean()),
                uzunluk=float(d.uzunluk.mean()), zaman_asimi=int(d.truncated.sum()), iki_bacak=int(d.iki_bacak_yerde.sum()), n=int(len(d)))


S = {}
# rastgele ajan
r = pd.read_csv("results/rastgele.csv")
S["rastgele"] = dict(ort=float(r.skor.mean()), std=float(r.skor.std(ddof=0)), ustu200=int((r.skor > 200).sum()), n=int(len(r)))

# PPO varyantlari
S["ppo"] = {}
for v in V:
    ds = [ev(v, s) for s in range(5)]
    per = [ozet(d) for d in ds]
    ort = np.array([p["ort"] for p in per]); tum = pd.concat(ds)
    S["ppo"][v] = dict(seed=per, ortalamalarin_ort=float(ort.mean()), seedler_arasi_std=float(ort.std(ddof=1)),
                       en_dusuk=float(ort.min()), en_yuksek=float(ort.max()),
                       toplam_zaman_asimi=int(tum.truncated.sum()), toplam_deneme=int(len(tum)),
                       basari_toplam=float(100 * (tum.skor > 200).mean()), uzunluk=float(tum.uzunluk.mean()),
                       deneme_std=float(tum.skor.std(ddof=0)))
# PID / heuristic
for v in ("pid", "heuristic"):
    S[v] = dict(yuz=ozet(pd.read_csv(f"results/{v}_eval.csv")), ek500=ozet(pd.read_csv(f"results/{v}_eval_ek500.csv")))
pa = json.load(open("results/pid_ayarlar.json"))
S["pid_ayar"] = dict(denenen=pa["denenen_ayar_sayisi"], secilen_seed0_99=pa["seed0_99_ort"], ilk5_seed0_99=pa["ilk5_seed0_99"],
                     ilk5_ki0_seed0_99=pa["ilk5_ki0_seed0_99"], elle_seed0_19=pa["tum_seed0_19_ort"][0],
                     ki_h=pa["secilen"]["ki_h"], ki_a=pa["secilen"]["ki_a"])
# egitim sureleri
def sure(f):
    m = re.match(r"(\d+) adim, ([\d.]+) sn, ([\d.]+) adim/sn", open(f).read())
    return dict(adim=int(m[1]), sn=float(m[2]), sps=float(m[3]))
sr = {}
for f in sorted(glob.glob("results/*_seed*/sure.txt")):
    sr[os.path.basename(os.path.dirname(f))] = sure(f)
S["sure"] = sr
def grp(isimler): 
    a = [sr[k]["sn"] for k in isimler]; b = [sr[k]["sps"] for k in isimler]
    return dict(sn_min=min(a), sn_max=max(a), sps_min=min(b), sps_max=max(b), n=len(a))
S["sure_dalga"] = dict(
    asama1_baseline_seed0=sr["baseline_seed0"],
    asama2_ABC_seed0=grp(["A_seed0", "B_seed0", "C_seed0"]),
    dalga1=grp([f"{v}_seed{s}" for v in ("baseline", "A") for s in range(1, 5)]),
    dalga2=grp([f"{v}_seed{s}" for v in ("B", "C") for s in range(1, 5)]))
S["olcum_50k"] = dict(sps=740.4)  # STATUS_asama0.md'de ölçülen; scripts/olcum_ppo.py çıktısı (sure dosyası yok)
os.makedirs("docs", exist_ok=True)
json.dump(S, open("docs/sayilar.json", "w"), indent=1)
print("docs/sayilar.json yazildi;", len(json.dumps(S)), "bayt")
