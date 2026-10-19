import numpy as np, pandas as pd, gymnasium as gym
from stable_baselines3 import PPO
model = PPO.load("models/ppo_baseline_seed0.zip", device="cpu")
env = gym.make("LunarLander-v3")
rows = []
for i in range(100):
    obs, _ = env.reset(seed=1000 + i)
    tot, n, d = 0.0, 0, False
    while not d:
        act, _ = model.predict(obs, deterministic=True)
        obs, r, t, tr, _ = env.step(int(act))
        tot += r; n += 1; d = t or tr
    rows.append((i, 1000 + i, tot, n))
df = pd.DataFrame(rows, columns=["deneme", "seed", "skor", "uzunluk"])
df.to_csv("results/baseline_seed0_eval.csv", index=False)
print(f"ortalama {df.skor.mean():.2f} std {df.skor.std(ddof=0):.2f} basari% {100*(df.skor>200).mean():.0f} uzunluk {df.uzunluk.mean():.1f}")
