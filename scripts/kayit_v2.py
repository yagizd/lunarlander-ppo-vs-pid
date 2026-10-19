import argparse
import gymnasium as gym
from gymnasium.wrappers import RecordVideo
from stable_baselines3 import PPO
p = argparse.ArgumentParser()
p.add_argument("--model", required=True); p.add_argument("--etiket", required=True)
a = p.parse_args()
model = PPO.load(a.model, device="cpu")
env = RecordVideo(gym.make("LunarLander-v3", render_mode="rgb_array"), video_folder="videos",
                  name_prefix=a.etiket, episode_trigger=lambda i: True)
obs, _ = env.reset(seed=1000); d = False; tot = 0; n = 0
while not d:
    act, _ = model.predict(obs, deterministic=True)
    obs, r, t, tr, _ = env.step(int(act)); tot += r; n += 1; d = t or tr
env.close()
print(a.etiket, "skor", tot, "adim", n, "term", t, "trunc", tr)
