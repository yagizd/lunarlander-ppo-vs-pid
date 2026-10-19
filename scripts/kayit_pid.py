import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import json, gymnasium as gym
from gymnasium.wrappers import RecordVideo
from pid_kontrolcu import PIDKontrol
from degerlendir_pid import HeuristicSecici

def kaydet(ad, k, env_ref=None):
    env = RecordVideo(gym.make("LunarLander-v3", render_mode="rgb_array"), video_folder="videos", name_prefix=ad, episode_trigger=lambda i: True)
    if env_ref is not None: k.env = env
    obs, _ = env.reset(seed=1000); k.reset(); tot, n, d = 0, 0, False
    while not d:
        obs, r, t, tr, _ = env.step(int(k.act(obs))); tot += r; n += 1; d = t or tr
    env.close(); print(ad, "skor", round(tot, 1), "adim", n, "term", t, "trunc", tr, "bacak", obs[6], obs[7])

kaydet("pid_seed1000", PIDKontrol(json.load(open("results/pid_ayarlar.json"))["secilen"]))
kaydet("heuristic_seed1000", HeuristicSecici(), env_ref=True)
