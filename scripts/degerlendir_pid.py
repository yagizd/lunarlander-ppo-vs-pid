"""Dondurulmus PID (results/pid_ayarlar.json) ve Gymnasium heuristic'i, wrapper YOK, oyunun kendi odulu."""
import os, sys, json
sys.path.insert(0, os.path.dirname(__file__))
import pandas as pd, gymnasium as gym
from gymnasium.envs.box2d.lunar_lander import heuristic
from pid_kontrolcu import PIDKontrol

KOLONLAR = ["deneme", "seed", "skor", "uzunluk", "terminated", "truncated", "iki_bacak_yerde"]


def calistir(secici, seedler):
    env = gym.make("LunarLander-v3")
    rows = []
    for i, sd in enumerate(seedler):
        obs, _ = env.reset(seed=sd); secici.reset()
        tot, n, term, trunc = 0.0, 0, False, False
        while not (term or trunc):
            obs, r, term, trunc, _ = env.step(int(secici.act(obs))); tot += r; n += 1
        rows.append((i, sd, tot, n, term, trunc, bool(obs[6] and obs[7])))
    return pd.DataFrame(rows, columns=KOLONLAR)


class HeuristicSecici:
    def __init__(self): self.env = None
    def reset(self): pass
    def act(self, obs): return heuristic(self.env.unwrapped, obs)


def heur_calistir(seedler):
    env = gym.make("LunarLander-v3")
    h = HeuristicSecici(); h.env = env
    rows = []
    for i, sd in enumerate(seedler):
        obs, _ = env.reset(seed=sd)
        tot, n, term, trunc = 0.0, 0, False, False
        while not (term or trunc):
            obs, r, term, trunc, _ = env.step(int(h.act(obs))); tot += r; n += 1
        rows.append((i, sd, tot, n, term, trunc, bool(obs[6] and obs[7])))
    return pd.DataFrame(rows, columns=KOLONLAR)


def ozet(ad, df):
    print(f"{ad}: ort {df.skor.mean():.2f} std {df.skor.std(ddof=0):.2f} basari% {100*(df.skor>200).mean():.1f} "
          f"uzunluk {df.uzunluk.mean():.1f} zaman_asimi {int(df.truncated.sum())} iki_bacak {int(df.iki_bacak_yerde.sum())}")


if __name__ == "__main__":
    ayar = json.load(open("results/pid_ayarlar.json"))["secilen"]
    ana, ek = [1000 + i for i in range(100)], [1100 + i for i in range(500)]
    for ad, f in (("pid", lambda s: calistir(PIDKontrol(ayar), s)), ("heuristic", heur_calistir)):
        d = f(ana); d.to_csv(f"results/{ad}_eval.csv", index=False); ozet(ad + " (100)", d)
        d = f(ek); d.to_csv(f"results/{ad}_eval_ek500.csv", index=False); ozet(ad + " (ek500)", d)
