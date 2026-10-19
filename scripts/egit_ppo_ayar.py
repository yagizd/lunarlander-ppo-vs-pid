"""egit_ppo_v2.py'nin kopyasi + ayarlar.json'dan PPO ayari. Odul: sadece baseline (wrapper YOK)."""
import argparse, json, os, sys, time
import torch
torch.set_num_threads(1)
import gymnasium as gym
from stable_baselines3 import PPO
from stable_baselines3.common.monitor import Monitor

p = argparse.ArgumentParser()
p.add_argument("--ayar_id", type=int, required=True)
p.add_argument("--seed", type=int, default=0)
p.add_argument("--adim", type=int, default=1_000_000)
p.add_argument("--cikti", required=True, help="orn. ayar3_seed0 veya kazanan_seed10")
p.add_argument("--ayar_dosyasi", default="results/ayar_ppo/ayarlar.json")
a = p.parse_args()
ay = {x["id"]: x for x in json.load(open(a.ayar_dosyasi))["ayarlar"]}[a.ayar_id]
d = f"results/ayar_ppo/{a.cikti}"
os.makedirs(d, exist_ok=True); os.makedirs("models/ayar_ppo", exist_ok=True)
# Monitor dogrudan ortami sarar (wrapper yok): monitor.csv oyunun gercek skorunu yazar.
env = Monitor(gym.make("LunarLander-v3"), f"{d}/monitor.monitor.csv")
model = PPO("MlpPolicy", env, seed=a.seed, device="cpu", learning_rate=ay["learning_rate"], n_steps=ay["n_steps"],
            batch_size=ay["batch_size"], n_epochs=ay["n_epochs"], gamma=ay["gamma"], gae_lambda=ay["gae_lambda"],
            ent_coef=ay["ent_coef"], clip_range=ay["clip_range"], policy_kwargs=dict(net_arch=ay["net_arch"]))
t0 = time.perf_counter()
model.learn(total_timesteps=a.adim)
dt = time.perf_counter() - t0
model.save(f"models/ayar_ppo/{a.cikti}")
open(f"{d}/sure.txt", "w").write(f"{a.adim} adim, {dt:.1f} sn, {a.adim/dt:.1f} adim/sn (olculdu)\n")
env.close()
os.replace(f"{d}/monitor.monitor.csv", f"{d}/monitor.csv")
print("bitti", dt)
