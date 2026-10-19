"""Adim 2: 16 ayar x 1M adim, 2 dalga x 8 paralel surec. 90 dk toplam sinir: asilirsa surecleri durdurur ve yazar."""
import subprocess, sys, time, os
SINIR = 90 * 60
t0 = time.time()
def log(m): print(time.strftime("%H:%M:%S"), m, flush=True)
for dalga, idler in enumerate([range(0, 8), range(8, 16)], start=1):
    log(f"DALGA {dalga} basladi: ayar {list(idler)}")
    ps = []
    for i in idler:
        os.makedirs(f"results/ayar_ppo/ayar{i}_seed0", exist_ok=True)
        ps.append((i, subprocess.Popen([sys.executable, "scripts/egit_ppo_ayar.py", "--ayar_id", str(i), "--seed", "0", "--adim", "1000000", "--cikti", f"ayar{i}_seed0"],
                   stdout=open(f"results/ayar_ppo/ayar{i}_seed0.log", "w"), stderr=open(f"results/ayar_ppo/ayar{i}_seed0.err", "w"))))
    while any(p.poll() is None for _, p in ps):
        if time.time() - t0 > SINIR:
            log("90 DAKIKA SINIRI ASILDI: surecler durduruluyor"); [p.kill() for _, p in ps if p.poll() is None]; sys.exit(2)
        time.sleep(10)
    log(f"DALGA {dalga} bitti; cikis kodlari {[p.returncode for _, p in ps]}")
log("TUM DALGALAR BITTI")
