import gymnasium as gym
from gymnasium.wrappers import RecordVideo
from stable_baselines3 import PPO
model = PPO.load("models/ppo_baseline_seed0.zip", device="cpu")
env = RecordVideo(gym.make("LunarLander-v3", render_mode="rgb_array"), video_folder="videos",
                  name_prefix="ppo_baseline_seed0", episode_trigger=lambda i: True)
for i in range(3):
    obs, _ = env.reset(seed=1000 + i); d = False; tot = 0
    while not d:
        act, _ = model.predict(obs, deterministic=True)
        obs, r, t, tr, _ = env.step(int(act)); tot += r; d = t or tr
    print("deneme", i, "skor", tot)
env.close()
