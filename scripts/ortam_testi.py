"""Quick environment check: imports, versions, one random LunarLander-v3 episode (no window, no files written)."""
import gymnasium as gym, stable_baselines3, torch, numpy
print("gymnasium", gym.__version__, "| stable-baselines3", stable_baselines3.__version__, "| torch", torch.__version__, "| numpy", numpy.__version__)
env = gym.make("LunarLander-v3")
obs, _ = env.reset(seed=0)
print("first observation (8 numbers):", obs.round(3).tolist())
total, done = 0.0, False
while not done:
    obs, r, term, trunc, _ = env.step(env.action_space.sample()); total += r; done = term or trunc
print("random episode score:", round(total, 1))
