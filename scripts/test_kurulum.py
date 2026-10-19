import gymnasium, stable_baselines3, moviepy, numpy, torch
print("gymnasium", gymnasium.__version__, "sb3", stable_baselines3.__version__, "moviepy", moviepy.__version__, "torch", torch.__version__, "numpy", numpy.__version__)
import gymnasium as gym
env = gym.make("LunarLander-v3", render_mode=None)
obs, _ = env.reset(seed=0)
print("kare0", obs.tolist())
total, n, done = 0.0, 0, False
while not done:
    obs, r, term, trunc, _ = env.step(env.action_space.sample())
    total += r; n += 1
    if n <= 2: print(f"kare{n}", obs.tolist())
    done = term or trunc
print("adim", n, "toplam skor", total)
import gymnasium.envs.box2d.lunar_lander as ll
print("heuristic var mi:", hasattr(ll, "heuristic"), ll.__file__)
from gymnasium.wrappers import RecordVideo
e = RecordVideo(gym.make("LunarLander-v3", render_mode="rgb_array"), video_folder="videos", name_prefix="rastgele_test", episode_trigger=lambda i: True)
e.reset(seed=1); d = False; k = 0
while not d and k < 150:
    _, _, t, tr, _ = e.step(e.action_space.sample()); d = t or tr; k += 1
e.close()
print("video tamam")
