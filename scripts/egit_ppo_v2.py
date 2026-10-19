import argparse, os, time, sys
sys.path.insert(0, os.path.dirname(__file__))
import torch
torch.set_num_threads(1)
import gymnasium as gym
from stable_baselines3 import PPO
from stable_baselines3.common.monitor import Monitor
from odul_wrapper import OdulWrapper

p = argparse.ArgumentParser()
p.add_argument("--varyant", choices=["baseline", "A", "B", "C"], required=True)
p.add_argument("--seed", type=int, default=0)
p.add_argument("--adim", type=int, default=1_000_000)
a = p.parse_args()
d = f"results/{a.varyant}_seed{a.seed}"
os.makedirs(d, exist_ok=True); os.makedirs("models", exist_ok=True)
# ONEMLI: Monitor wrapper'in ICINDE. Boylece monitor.csv oyunun GERCEK skorunu yazar
# (bizim eklediğimiz bonusu degil); varyantlar birbiriyle karsilastirilabilir.
env = Monitor(gym.make("LunarLander-v3"), f"{d}/monitor.monitor.csv")
if a.varyant != "baseline":
    env = OdulWrapper(env, a.varyant)
model = PPO("MlpPolicy", env, seed=a.seed, device="cpu")
t0 = time.perf_counter()
model.learn(total_timesteps=a.adim)
dt = time.perf_counter() - t0
model.save(f"models/ppo_{a.varyant}_seed{a.seed}")
open(f"{d}/sure.txt", "w").write(f"{a.adim} adim, {dt:.1f} sn, {a.adim/dt:.1f} adim/sn (olculdu)\n")
env.close()
os.replace(f"{d}/monitor.monitor.csv", f"{d}/monitor.csv")
print("bitti", dt)
