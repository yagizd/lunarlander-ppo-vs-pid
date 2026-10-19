import sys, pandas as pd
for v in sys.argv[1:]:
    for s in range(1, 5):
        f = f"results/{v}_seed{s}/monitor.monitor.csv"
        try:
            d = pd.read_csv(f, skiprows=1)
            print(f"{v} s{s}: adim {int(d.l.sum())}, son100 gercek {d.r.tail(100).mean():.1f}", flush=True)
        except Exception as e:
            print(v, s, "okunamadi", flush=True)
