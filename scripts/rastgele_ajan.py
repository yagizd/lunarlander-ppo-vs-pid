import numpy as np, pandas as pd, gymnasium as gym
env = gym.make("LunarLander-v3")
env.action_space.seed(0)
rows = []
for i in range(100):
    env.reset(seed=1000 + i)
    tot, d = 0.0, False
    while not d:
        _, r, t, tr, _ = env.step(env.action_space.sample())
        tot += r; d = t or tr
    rows.append((i, 1000 + i, tot))
df = pd.DataFrame(rows, columns=["deneme", "seed", "skor"])
df.to_csv("results/rastgele.csv", index=False)
print(f"ortalama {df.skor.mean():.2f} std {df.skor.std(ddof=0):.2f} 200_ustu {(df.skor>200).sum()}")
