import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np, gymnasium as gym
from pid_kontrolcu import PIDKontrol


def oyna(p, seedler, kontrol=None):
    """Her seed için bir deneme oyna; (skor, uzunluk, terminated, truncated, iki_bacak) listesi döner."""
    env = gym.make("LunarLander-v3")
    k = kontrol or PIDKontrol(p)
    out = []
    for s in seedler:
        obs, _ = env.reset(seed=int(s)); k.reset()
        tot, n, term, trunc = 0.0, 0, False, False
        while not (term or trunc):
            obs, r, term, trunc, _ = env.step(int(k.act(obs))); tot += r; n += 1
        out.append((tot, n, term, trunc, bool(obs[6] and obs[7])))
    return out
