"""PID ayari. SADECE seed 0-99 kullanilir (degerlendirme seed'leri 1000+ burada GECMEZ)."""
import os, sys, json
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from multiprocessing import Pool
from pid_kontrolcu import VARSAYILAN
from pid_ortak import oyna

AYAR_SEEDLERI_20 = list(range(0, 20))
AYAR_SEEDLERI_100 = list(range(0, 100))
assert max(AYAR_SEEDLERI_100) < 1000  # degerlendirme seed'leri (1000+) ayarda yok


def puan(p, seedler):
    return float(np.mean([x[0] for x in oyna(p, seedler)]))


def f20(p): return puan(p, AYAR_SEEDLERI_20)
def f100(p): return puan(p, AYAR_SEEDLERI_100)


def rastgele_ayar(rng):
    p = {}
    for k, v in VARSAYILAN.items():
        if k in ("ki_h", "ki_a"):
            p[k] = float(rng.uniform(0, 0.05))
        elif k == "kd_h":
            p[k] = float(rng.uniform(0, 1.0))
        else:
            p[k] = float(v * np.exp(rng.normal(0, 0.4)))
    p["amax"] = float(min(p["amax"], 0.8))
    return p


if __name__ == "__main__":
    rng = np.random.default_rng(12345)
    adaylar = [dict(VARSAYILAN)] + [rastgele_ayar(rng) for _ in range(199)]  # toplam 200
    with Pool(8) as pool:
        s20 = pool.map(f20, adaylar)
        sira = np.argsort(s20)[::-1]
        ilk5 = [adaylar[i] for i in sira[:5]]
        s100 = pool.map(f100, ilk5)
        # ki=0 karsilastirmasi (yeniden ayar YOK, ayni 5 ayarda sadece ki=0 yapildi)
        ilk5_ki0 = [dict(a, ki_h=0.0, ki_a=0.0) for a in ilk5]
        s100_ki0 = pool.map(f100, ilk5_ki0)
    en = int(np.argmax(s100))
    json.dump(dict(secilen=ilk5[en], seed0_99_ort=s100[en], denenen_ayar_sayisi=len(adaylar),
                   ilk5_seed0_99=s100, ilk5_ki0_seed0_99=s100_ki0, ilk5_seed0_19=[s20[i] for i in sira[:5]],
                   tum_seed0_19_ort=s20, ilk5_ayarlar=ilk5,
                   ayar_seedleri="0-99 (arama: 0-19, finalist: 0-99)"),
              open("results/pid_ayarlar.json", "w"), indent=1)
    print("denenen", len(adaylar), "| en iyi 5 (seed0-19):", [round(s20[i], 1) for i in sira[:5]])
    print("ilk5 seed0-99:", [round(x, 1) for x in s100], "| ki=0:", [round(x, 1) for x in s100_ki0])
    print("secilen seed0-99 ort", round(s100[en], 1), "ki_h", ilk5[en]["ki_h"], "ki_a", ilk5[en]["ki_a"])
    print("baslangic (elle) seed0-19:", round(s20[0], 1), "| tum 200 ortalamasi:", round(float(np.mean(s20)), 1))
