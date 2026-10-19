import argparse
import pandas as pd, gymnasium as gym
from stable_baselines3 import PPO
p = argparse.ArgumentParser()
p.add_argument("--model", required=True); p.add_argument("--etiket", required=True)
a = p.parse_args()
model = PPO.load(a.model, device="cpu")
env = gym.make("LunarLander-v3")
rows = []
for i in range(100):
    obs, _ = env.reset(seed=1000 + i)
    tot, n, term, trunc = 0.0, 0, False, False
    while not (term or trunc):
        act, _ = model.predict(obs, deterministic=True)
        obs, r, term, trunc, _ = env.step(int(act)); tot += r; n += 1
    rows.append((i, 1000 + i, tot, n, term, trunc, bool(obs[6] and obs[7])))
df = pd.DataFrame(rows, columns=["deneme", "seed", "skor", "uzunluk", "terminated", "truncated", "iki_bacak_yerde"])
df.to_csv(f"results/{a.etiket}_eval.csv", index=False)
print(f"{a.etiket}: ort {df.skor.mean():.2f} std {df.skor.std(ddof=0):.2f} basari% {100*(df.skor>200).mean():.0f} "
      f"uzunluk {df.uzunluk.mean():.1f} zaman_asimi {int(df.truncated.sum())} iki_bacak {int(df.iki_bacak_yerde.sum())}")
