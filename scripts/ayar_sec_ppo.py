"""Ayar secimi: modelleri SADECE tuning seed'leri 0-99 ile degerlendirir. 1000-1099'a bakmaz (assert)."""
import argparse, json, os, sys
import numpy as np, pandas as pd, gymnasium as gym
from multiprocessing import Pool
from stable_baselines3 import PPO

SEEDLER = list(range(100))


def oyna(yol):
    assert all(0 <= s <= 99 for s in SEEDLER), "ayar seed'leri 0-99 disina cikti: DUR"
    model = PPO.load(yol, device="cpu"); env = gym.make("LunarLander-v3"); rows = []
    for s in SEEDLER:
        assert 0 <= s <= 99, "ayar seed'leri 0-99 disina cikti: DUR"
        obs, _ = env.reset(seed=s); tot, n, term, trunc = 0.0, 0, False, False
        while not (term or trunc):
            act, _ = model.predict(obs, deterministic=True)
            obs, r, term, trunc, _ = env.step(int(act)); tot += r; n += 1
        rows.append((s, tot, n, term, trunc))
    return pd.DataFrame(rows, columns=["seed", "skor", "uzunluk", "terminated", "truncated"])


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--onek", default="ayar"); p.add_argument("--sonek", default="_seed0")
    p.add_argument("--idler", default="0-15"); p.add_argument("--etiket", default="secim")
    a = p.parse_args()
    lo, hi = map(int, a.idler.split("-")); idler = list(range(lo, hi + 1))
    yollar = [f"models/ayar_ppo/{a.onek}{i}{a.sonek}.zip" for i in idler]
    with Pool(8) as pool: dfs = pool.map(oyna, yollar)
    satir = []
    for i, d in zip(idler, dfs):
        d.to_csv(f"results/ayar_ppo/{a.onek}{i}{a.sonek}_tuneval_{a.etiket}.csv", index=False)
        assert d.seed.between(0, 99).all()
        satir.append(dict(id=i, ort=d.skor.mean(), std=d.skor.std(ddof=0), basari=100 * (d.skor > 200).mean(), zaman_asimi=int(d.truncated.sum())))
    T = pd.DataFrame(satir)
    sira = T.sort_values(["ort", "basari", "id"], ascending=[False, False, True])
    kazanan = int(sira.iloc[0].id)
    with open(f"results/ayar_ppo/{a.etiket}_tablosu.md", "w", encoding="utf-8") as f:
        f.write(f"# Ayar secim tablosu (SADECE tuning seed 0-99, 100 bolum, wrapper kapali, deterministik)\n\n| ayar id | ortalama | std | basari % (>200) | zaman asimi |\n|---|---|---|---|---|\n")
        for _, r in T.iterrows(): f.write(f"| {int(r.id)} | {r.ort:.1f} | {r['std']:.1f} | {r.basari:.0f} | {r.zaman_asimi} |\n")
        f.write(f"\nKazanan: ayar {kazanan} (en yuksek ortalama; esitlikte yuksek basari, sonra dusuk id).\nKullanilan seed'ler: {SEEDLER[0]}-{SEEDLER[-1]}. 1000-1099 kullanilmadi.\n")
    json.dump(dict(kazanan_id=kazanan, secim_seedleri="0-99", tablo=satir), open(f"results/ayar_ppo/{a.etiket}_kazanan.json", "w"), indent=1)
    print(f"SECIM seed {SEEDLER[0]}-{SEEDLER[-1]} ile yapildi (assert gecti). Kazanan ayar {kazanan}")
    print(T.round(1).to_string(index=False))
