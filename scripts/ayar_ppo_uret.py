"""16 PPO ayarini rastgele uretir (aralik tablosu supervizor tarafindan sabitlendi). Uretici tohumu: 6001."""
import inspect, json, math
import numpy as np
from stable_baselines3 import PPO
import stable_baselines3

TOHUM = 6001
rng = np.random.default_rng(TOHUM)
SECIM = dict(
    n_steps=[512, 1024, 2048, 4096], batch_size=[64, 128, 256, 512], n_epochs=[5, 10, 20],
    gamma=[0.98, 0.99, 0.995, 0.999], gae_lambda=[0.9, 0.95, 0.98], ent_coef=[0, 1e-4, 1e-3, 1e-2],
    clip_range=[0.1, 0.2, 0.3], net_arch=[[64, 64], [128, 128], [256, 256]])
SIRA = ["learning_rate", "n_steps", "batch_size", "n_epochs", "gamma", "gae_lambda", "ent_coef", "clip_range", "net_arch"]


def cek():
    a = {}
    for k in SIRA:
        if k == "learning_rate":
            a[k] = float(math.exp(rng.uniform(math.log(1e-4), math.log(2e-3))))  # log-duzgun
        else:
            a[k] = SECIM[k][int(rng.integers(len(SECIM[k])))]
    return a


ayarlar, cekim = [], 0
while len(ayarlar) < 16:
    a = cek(); cekim += 1
    if a["batch_size"] > a["n_steps"] or a["n_steps"] % a["batch_size"] != 0:
        continue  # batch_size n_steps'i tam bolmeli
    if any({k: v for k, v in a.items() if k != "learning_rate"} == {k: v for k, v in b.items() if k != "id" and k != "learning_rate"}
           and a["learning_rate"] == b["learning_rate"] for b in ayarlar):
        continue  # ayni ayar yeniden cekilir
    ayarlar.append(dict(id=len(ayarlar), **a))

sig = inspect.signature(PPO.__init__).parameters
ref = {k: sig[k].default for k in SIRA if k != "net_arch"}
ref["net_arch"] = "dict(pi=[64, 64], vf=[64, 64]) (policies.py: net_arch None -> bu); liste [64,64] ile ayni"
ref = {k: (v if not callable(v) else repr(v)) for k, v in ref.items()}
json.dump(dict(uretici_tohumu=TOHUM, sb3_surumu=stable_baselines3.__version__, cekim_sayisi=cekim, referans_varsayilan=ref, ayarlar=ayarlar),
          open("results/ayar_ppo/ayarlar.json", "w"), indent=1)
print("cekim", cekim); print("referans", ref)
for a in ayarlar: print(a)
