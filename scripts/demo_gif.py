"""4 klip yan yana (2x2): rastgele ajan, PPO baseline seed0, PPO B (hile) seed0, PID. Hepsi baslangic seed 1000. Yeni egitim yok."""
import os
import numpy as np, imageio.v3 as iio, gymnasium as gym
from PIL import Image, ImageDraw
from gymnasium.wrappers import RecordVideo

os.makedirs("docs/_gecici/rastgele", exist_ok=True)
# rastgele ajan: seed 1000 ile yeniden kaydet (eski rastgele_test.mp4 baska seed'di)
env = RecordVideo(gym.make("LunarLander-v3", render_mode="rgb_array"), video_folder="docs/_gecici/rastgele", name_prefix="r", episode_trigger=lambda i: True)
env.action_space.seed(0); env.reset(seed=1000); d = False
while not d:
    _, _, t, tr, _ = env.step(env.action_space.sample()); d = t or tr
env.close()

KLIP = [("Random agent", "docs/_gecici/rastgele/r-episode-0.mp4"),
        ("PPO baseline (seed 0)", "videos/ppo_baseline_seed0-episode-0.mp4"),
        ("PPO + hack reward B (seed 0)", "videos/B_seed0-episode-0.mp4"),
        ("PID controller", "videos/pid_seed1000-episode-0.mp4")]
ADIM = 4          # her 4. kare (GIF kucuk olsun)
W, H = 300, 200
klipler = []
for ad, f in KLIP:
    fr = list(iio.imiter(f))
    klipler.append((ad, fr[::ADIM] + [fr[-1]], len(fr)))
n = max(len(k[1]) for k in klipler)
kareler = []
for i in range(n):
    sheet = Image.new("RGB", (2 * W, 2 * H))
    for j, (ad, fr, tam) in enumerate(klipler):
        im = Image.fromarray(fr[min(i, len(fr) - 1)]).resize((W, H))
        dr = ImageDraw.Draw(im)
        dr.rectangle([0, 0, W, 14], fill=(0, 0, 0)); dr.text((4, 1), ad, fill=(255, 255, 255))
        sheet.paste(im, ((j % 2) * W, (j // 2) * H))
    kareler.append(sheet.quantize(colors=64, method=Image.MEDIANCUT, dither=Image.NONE))
kareler[0].save("docs/demo.gif", save_all=True, append_images=kareler[1:], duration=40, loop=0, optimize=True)
print("kare sayisi", n, "klip uzunluklari (orijinal kare):", [k[2] for k in klipler], "boyut MB", round(os.path.getsize("docs/demo.gif") / 1e6, 2))
