"""Compares fresh evaluations with the saved CSVs. Run from a copy of the repo (it writes into ./results/)."""
import subprocess, sys, pandas as pd
ORIG = sys.argv[1]  # original results folder (read only)
ok = True
def kontrol(ad, yeni, eski):
    global ok
    a, b = pd.read_csv(yeni), pd.read_csv(eski)
    ayni = a.shape == b.shape and (a.skor.values == b.skor.values).all() and (a.uzunluk.values == b.uzunluk.values).all()
    print(f"{ad}: yeni ort {a.skor.mean():.2f} | kayitli ort {b.skor.mean():.2f} | deneme deneme birebir ayni: {ayni}", flush=True)
    ok &= bool(ayni)
for v in ("baseline", "A", "C"):
    subprocess.run([sys.executable, "scripts/degerlendir_v2.py", "--model", f"models/ppo_{v}_seed0.zip", "--etiket", f"tmp_{v}"], check=True, capture_output=True)
    kontrol(f"PPO {v} seed0", f"results/tmp_{v}_eval.csv", f"{ORIG}/{v}_eval.csv")
subprocess.run([sys.executable, "scripts/degerlendir_pid.py"], check=True, capture_output=True)
for v in ("pid", "heuristic"):
    kontrol(f"{v} (100)", f"results/{v}_eval.csv", f"{ORIG}/{v}_eval.csv")
    kontrol(f"{v} (ek500)", f"results/{v}_eval_ek500.csv", f"{ORIG}/{v}_eval_ek500.csv")
print("HEPSI_AYNI" if ok else "UYUSMAZLIK")
