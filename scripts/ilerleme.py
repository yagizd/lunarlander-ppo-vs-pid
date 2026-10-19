import pandas as pd, os
for v in "ABC":
    f = f"results/{v}_seed0/monitor.monitor.csv"
    try:
        d = pd.read_csv(f, skiprows=1)
        print(f"{v}: {len(d)} deneme, adim {int(d.l.sum())}, son100 gercek skor {d.r.tail(100).mean():.1f}, uzunluk {d.l.tail(100).mean():.0f}", flush=True)
    except Exception as e:
        print(v, "okunamadi", e, flush=True)
