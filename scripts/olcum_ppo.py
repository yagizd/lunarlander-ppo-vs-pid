import time
import gymnasium as gym
from stable_baselines3 import PPO

env = gym.make("LunarLander-v3")
model = PPO("MlpPolicy", env, seed=0, device="cpu", verbose=0)
t0 = time.perf_counter()
model.learn(total_timesteps=50_000)
dt = time.perf_counter() - t0
sps = 50_000 / dt
print(f"OLCULDU: 50000 adim = {dt:.1f} sn, {sps:.1f} adim/sn")
print(f"TAHMIN: 1.000.000 adim = {1_000_000/sps:.0f} sn = {1_000_000/sps/60:.1f} dk")
