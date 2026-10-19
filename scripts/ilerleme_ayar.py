import glob, os, pandas as pd
for i in range(16):
    f = f"results/ayar_ppo/ayar{i}_seed0/monitor.monitor.csv"; g = f"models/ayar_ppo/ayar{i}_seed0.zip"
    if os.path.exists(g): print(f"ayar {i}: BITTI"); continue
    try:
        d = pd.read_csv(f, skiprows=1); print(f"ayar {i}: adim {int(d.l.sum())}, son100 gercek skor {d.r.tail(100).mean():.1f}")
    except Exception: pass
