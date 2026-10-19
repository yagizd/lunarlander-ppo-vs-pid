import argparse, os, time
import gymnasium as gym
from stable_baselines3 import PPO
from stable_baselines3.common.monitor import Monitor

p = argparse.ArgumentParser()
p.add_argument("--seed", type=int, default=0)
p.add_argument("--adim", type=int, default=1_000_000)
a = p.parse_args()
d = f"results/baseline_seed{a.seed}"
os.makedirs(d, exist_ok=True); os.makedirs("models", exist_ok=True)
env = Monitor(gym.make("LunarLander-v3"), f"{d}/monitor")
model = PPO("MlpPolicy", env, seed=a.seed, device="cpu")
t0 = time.perf_counter()
model.learn(total_timesteps=a.adim)
dt = time.perf_counter() - t0
model.save(f"models/ppo_baseline_seed{a.seed}")
open(f"{d}/sure.txt", "w").write(f"{a.adim} adim, {dt:.1f} sn, {a.adim/dt:.1f} adim/sn (olculdu)\n")
env.close()
os.replace(f"{d}/monitor.monitor.csv", f"{d}/monitor.csv")
print("bitti", dt)
