"""README.md, REPORT.md ve OZET_TR.md'yi docs/sayilar.json (+ docs/tekrar_uretim.json) dosyalarindan uretir.
Metne elle sayi yazilmaz; sayilar `f"{...}"` ile JSON'dan gelir. (Sabit metindeki sayilar: seed/adim sayilari gibi protokol sabitleri,
bunlar scripts/rapor_dogrula.py'de beyaz listede.)"""
import json

S = json.load(open("docs/sayilar.json"))
T = json.load(open("docs/tekrar_uretim.json"))
P = S["ppo"]
f1 = lambda x: f"{x:.1f}"
f0 = lambda x: f"{x:.0f}"


def tz(v):  # seed basina zaman asimi listesi
    return [s["zaman_asimi"] for s in P[v]["seed"]]


def uz(v):
    return [s["uzunluk"] for s in P[v]["seed"]]


def sd(v):
    return [s["ort"] for s in P[v]["seed"]]


B_tz, B_uz, base_uz = tz("B"), uz("B"), uz("baseline")
hover = [i for i, x in enumerate(B_tz) if x >= 30]
nohover = [i for i in range(5) if i not in hover]
pid, heu = S["pid"], S["heuristic"]
sd_base, sd_A, sd_C = P["baseline"]["seedler_arasi_std"], P["A"]["seedler_arasi_std"], P["C"]["seedler_arasi_std"]
c_worst = min(range(5), key=lambda i: sd("C")[i])
wave1, wave2, a1, a2 = S["sure_dalga"]["dalga1"], S["sure_dalga"]["dalga2"], S["sure_dalga"]["asama1_baseline_seed0"], S["sure_dalga"]["asama2_ABC_seed0"]
rnd = S["rastgele"]
pa = S["pid_ayar"]


def satir_ppo(ad, v):
    p = P[v]
    return (f"| {ad} | {f1(p['ortalamalarin_ort'])} ± {f1(p['seedler_arasi_std'])} | {f1(p['en_dusuk'])} – {f1(p['en_yuksek'])} | "
            f"{f1(p['basari_toplam'])}% | {f0(p['uzunluk'])} | {p['toplam_zaman_asimi']} / {p['toplam_deneme']} |")


def satir_tek(ad, d):
    y = d["yuz"]
    return f"| {ad} | {f1(y['ort'])} (single controller) | – | {f1(y['basari'])}% | {f0(y['uzunluk'])} | {y['zaman_asimi']} / {y['n']} |"


TABLO = "\n".join([
    "| Method | Mean score (mean ± std across 5 seeds) | Lowest – highest seed mean | Success rate (score > 200) | Mean episode length (steps) | Timeouts |",
    "|---|---|---|---|---|---|",
    satir_ppo("PPO baseline (game's own reward)", "baseline"),
    satir_ppo("PPO + reward A (time penalty)", "A"),
    satir_ppo("PPO + reward B (deliberately hackable)", "B"),
    satir_ppo("PPO + reward C (potential-based + time penalty)", "C"),
    satir_tek("PID controller (hand-written, tuned on seeds 0-99)", pid),
    satir_tek("Gymnasium `heuristic` (reference, not written by us)", heu),
])

HEADLINE = f"""- **Reward hacking reproduced.** With reward B (+1 per frame while upright and slow), the agent learned to wait near the ground instead of landing. In the {len(hover)} of 5 seeds where this was clear, {', '.join(str(B_tz[i]) for i in hover)} of 100 test episodes timed out (seeds {', '.join(str(i) for i in hover)}). Baseline had {P['baseline']['toplam_zaman_asimi']} timeouts in 500 test episodes; B had {P['B']['toplam_zaman_asimi']} in 500.
- **One seed was misleading.** Reward A scored {f1(sd('A')[0])} on seed 0 (baseline seed 0: {f1(sd('baseline')[0])}), but over 5 seeds the means were {f1(P['A']['ortalamalarin_ort'])} (A) and {f1(P['baseline']['ortalamalarin_ort'])} (baseline), with seed-to-seed std {f1(sd_A)} and {f1(sd_base)}. In these 5 seeds the difference is unclear.
- **The fixed reward C removed most hovering but was not consistently better.** Timeouts dropped from {P['B']['toplam_zaman_asimi']} to {P['C']['toplam_zaman_asimi']} (out of 500). Its mean score ({f1(P['C']['ortalamalarin_ort'])}) was below baseline, and one seed (seed {c_worst}) collapsed to a mean of {f1(sd('C')[c_worst])}.
- **A tuned PID controller scored higher than default-settings PPO in this setup** ({f1(pid['yuz']['ort'])} vs {f1(P['baseline']['ortalamalarin_ort'])}-{f1(P['A']['ortalamalarin_ort'])} for the PPO runs without hack reward; the PPO C mean was {f1(P['C']['ortalamalarin_ort'])}). This is not a fair-budget comparison: the PID got {pa['denenen']} tuning candidates, PPO stayed at default settings."""

LIMITS = """- One environment (LunarLander-v3), one reward definition set, one PPO setting (library defaults), 5 seeds.
- The "good state" thresholds (0.2 / 0.5 / 0.5 for tilt, horizontal speed, vertical speed) are an assumption and were not tuned. The B and C results may depend on them.
- All methods are evaluated on the same 100 start seeds (1000-1099). This makes the comparison fair, but the numbers may be specific to these 100 starts.
- PPO was not given the tuning budget that the PID received.
- One computer (Windows, CPU only). Training times may have been affected by other processes.
- The Gymnasium `heuristic` reference was not written by us."""

REPRO = ""
if T["eval_hepsi_ayni"] and T["egitim_ayni"]:
    REPRO = (f"Saved models and the frozen PID were re-evaluated in a fresh virtual environment built from `requirements-min.txt` and matched the stored CSVs episode by episode "
             f"(PPO baseline, A, C seed 0, PID, heuristic). Two separate {T['egitim_adim']}-step baseline trainings (seed 0, one thread) produced "
             f"{'bit-for-bit identical weights and identical scores on 20 start seeds' if T['agirlik_ayni'] else 'identical scores on 20 start seeds'}. "
             f"This was checked on one machine only (Windows 11, CPU).")
else:
    REPRO = "Reproduction check found differences. See STATUS notes; do not describe this project as reproducible."

README = f"""# Reward shaping on LunarLander: PPO vs. a hand-written PID controller

I trained PPO agents on LunarLander-v3 with several reward definitions (including a deliberately hackable one), ran each for 5 seeds, and compared the results with a hand-written PID controller and Gymnasium's built-in `heuristic`.

![Demo: random agent, PPO baseline, PPO with hackable reward B, PID. Same start (seed 1000).](docs/demo.gif)

*Same start (seed 1000). Top left: random agent. Top right: PPO baseline (seed 0). Bottom left: PPO with hackable reward B (seed 0): it hovers near the ground. Bottom right: PID.*

## Headline results (honest version)

{HEADLINE}

All numbers: 100 test episodes per trained model, start seeds 1000-1099, the game's own score (no reward wrapper), deterministic actions. Observations about 5 seeds show a direction; they do not prove anything.

## Results table

{TABLO}

Seed-level numbers: `results/ozet_seed_tablosu.md`. PID and heuristic extra check on 500 more start seeds (1100-1599): PID mean {f1(pid['ek500']['ort'])}, heuristic mean {f1(heu['ek500']['ort'])}. A random agent scored {f1(rnd['ort'])} on average (std {f1(rnd['std'])}, {rnd['ustu200']} of {rnd['n']} above 200).

![Evaluation score per variant](docs/degerlendirme_kutu.png)
![Training curves](docs/egitim_egrileri.png)
![Timeouts per variant and seed](docs/zaman_asimi.png)
![PID vs PPO](docs/pid_vs_ppo.png)

## Quick start

Tested on Windows 11 with Python 3.13 (PowerShell). The Linux/macOS commands below are the same steps but were **not tested**.

```powershell
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
pip install -r requirements-min.txt
python scripts/ortam_testi.py
python scripts/degerlendir_v2.py --model models/ppo_baseline_seed0.zip --etiket my_check
python scripts/degerlendir_pid.py
```

```bash
# Linux / macOS (not tested)
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-min.txt
python scripts/ortam_testi.py
python scripts/degerlendir_v2.py --model models/ppo_baseline_seed0.zip --etiket my_check
python scripts/degerlendir_pid.py
```

`degerlendir_v2.py` writes `results/my_check_eval.csv`. `degerlendir_pid.py` re-evaluates the frozen PID and the heuristic and **overwrites** `results/pid_eval*.csv` and `results/heuristic_eval*.csv` with identical numbers (back them up first if you want to keep the originals). Train one model: `python scripts/egit_ppo_v2.py --varyant baseline --seed 0 --adim 1000000`. The one-million-step trainings took {f0(wave1['sn_min'])}-{f0(wave1['sn_max'])} s each when {wave1['n']} ran in parallel on this machine (measured).

**Reproducibility.** {REPRO}

## Project structure

```
scripts/
  odul_wrapper.py        reward variants A, B, C (wrapper around the game's reward)
  egit_ppo_v2.py         train PPO (variants baseline, A, B, C; any seed)
  degerlendir_v2.py      evaluate a model: 100 episodes, seeds 1000-1099, no wrapper
  pid_kontrolcu.py       hand-written PID controller
  ayar_pid.py            PID tuning (random search, only seeds 0-99)
  degerlendir_pid.py     evaluate frozen PID and Gymnasium heuristic
  ozet.py, karsilastir.py   tables and plots
  rapor_sayilari.py, rapor_olustur.py, rapor_dogrula.py   numbers -> docs/sayilar.json -> README/REPORT, with a number check
  yon_testi.py           measures what each action does (used before writing the PID)
  (older scripts: egit_ppo.py, degerlendir.py, kayit*.py, ...: earlier stages)
models/    trained PPO models (.zip)
results/   monitor logs, evaluation CSVs, tables, plots
videos/    recorded episodes
docs/      demo.gif, plots, sayilar.json (every number in README/REPORT)
```

## How the reward variants work

Observation (8 numbers): x, y, horizontal speed, vertical speed, tilt, rotation speed, left leg contact, right leg contact. "Good state" = tilt < 0.2, horizontal speed < 0.5, vertical speed < 0.5 in absolute value (**assumption**: reasonable values, not tuned).

- **A:** game reward − 0.05 every frame (time penalty).
- **B (hackable):** game reward + 1 every frame while in the good state. Waiting in the good state pays forever.
- **C (fixed):** game reward + (good-state indicator now − before) − 0.05 per frame. Only *getting into* the good state pays, and waiting costs.

The training logs record the game's real score, not the shaped one.

## Limitations

{LIMITS}

## Credits

- [Gymnasium](https://gymnasium.farama.org/) (LunarLander-v3) and [Stable-Baselines3](https://stable-baselines3.readthedocs.io/) (PPO).
- PPO: Schulman et al., "Proximal Policy Optimization Algorithms", 2017.
- Idea inspired by the post "Training an AI to land a rocket with reward shaping" by Hari (@harixganesh).
- The `heuristic` function in `gymnasium.envs.box2d.lunar_lander` was **not written by us**. It is a hand-tuned controller from the Gymnasium authors, used here only as a reference. The PID code in this repo was written from scratch.
"""

REPORT = f"""# Reward shaping on LunarLander-v3: PPO and a PID baseline

## Goal
Show how reward definitions change what PPO learns (including a reward that can be hacked), check whether single-seed results hold over 5 seeds, and compare against a classical PID controller that sees the same 8 numbers.

## Setup
- Environment: LunarLander-v3 (Gymnasium {'1.4.0'}), discrete actions: 0 nothing, 1 and 3 side engines, 2 main engine. Observation: 8 numbers (position x and y, two velocities, tilt, rotation speed, two leg contacts). Game reward as provided by the environment.
- PPO: Stable-Baselines3, `MlpPolicy`, all default hyperparameters, CPU, one million steps per run, training seeds 0-4. No hyperparameter search.
- Evaluation protocol (same for every method): reward wrapper off, the game's own score, deterministic actions, 100 episodes with start seeds 1000-1099. Start seeds 1000+ were never used during training or PID tuning.
- Training logs record the game's real score because the monitor sits inside the reward wrapper.

## Experiment 1: baseline
A random agent scored {f1(rnd['ort'])} on average (std {f1(rnd['std'])}; {rnd['ustu200']} of {rnd['n']} episodes above 200). The baseline PPO (seed 0) scored {f1(sd('baseline')[0])}, with {f1(P['baseline']['seed'][0]['basari'])}% of episodes above 200.

## Experiment 2: reward variants A, B, C (seed 0)
A: time penalty. B: +1 per frame in a "good state" (upright and slow). C: change in the good-state indicator plus time penalty. Seed 0 means: A {f1(sd('A')[0])}, B {f1(sd('B')[0])}, C {f1(sd('C')[0])}. B timed out in {B_tz[0]} of 100 test episodes (baseline: {tz('baseline')[0]}). Frames of the B video show the lander waiting just above the ground, off the platform, with legs not touching until the end of the episode.

## Experiment 3: five seeds
{TABLO}

In these 5 seeds we observed:
- B was below baseline in all 5 seeds. In {len(hover)} seeds (seeds {', '.join(str(i) for i in hover)}) there was clear hovering ({', '.join(str(B_tz[i]) for i in hover)} timeouts out of 100). In the other {len(nohover)} seeds (seeds {', '.join(str(i) for i in nohover)}) timeouts were few ({', '.join(str(B_tz[i]) for i in nohover)}) but episodes were long ({', '.join(f0(B_uz[i]) for i in nohover)} steps; baseline on the same seeds: {', '.join(f0(base_uz[i]) for i in nohover)}).
- C removed most hovering (timeouts {P['B']['toplam_zaman_asimi']} → {P['C']['toplam_zaman_asimi']} of 500) but did not beat baseline consistently. Seed {c_worst} collapsed (mean {f1(sd('C')[c_worst])}).
- A scored {f1(sd('A')[0])} on seed 0 but {f1(P['A']['ortalamalarin_ort'])} on average over 5 seeds (baseline {f1(P['baseline']['ortalamalarin_ort'])}); seed-to-seed std {f1(sd_A)} and {f1(sd_base)}. The difference is unclear. Looking at one seed would have been misleading.
- Baseline itself varied between seeds: {f1(P['baseline']['en_dusuk'])} to {f1(P['baseline']['en_yuksek'])}.
- Training time (measured): {a2['n']} runs in parallel took {f0(a2['sn_min'])}-{f0(a2['sn_max'])} s each; 8 runs in parallel took {f0(wave1['sn_min'])}-{f0(wave1['sn_max'])} s (first wave) and {f0(wave2['sn_min'])}-{f0(wave2['sn_max'])} s (second wave). The very first single-run baseline took {f0(a1['sn'])} s ({f1(a1['sps'])} steps/s). A slowdown from other processes on the machine is possible but not proven.

## Experiment 4: PID vs PPO
The PID controller was written from scratch with two loops: descent speed → main engine, tilt → side engines, plus a dead zone and engines off when both legs touch. Directions of each action were measured before writing it. Gains and thresholds were tuned only on start seeds 0-99: {pa['denenen']} candidate settings scored on 20 episodes, the best 5 re-scored on 100, the best frozen (seed 0-99 mean {f1(pa['secilen_seed0_99'])}). Setting the integral gains to zero on the same 5 candidates gave seed 0-99 means of {', '.join(f1(x) for x in pa['ilk5_ki0_seed0_99'])} (not re-tuned), so the integral term does not look necessary here.

On seeds 1000-1099: PID mean {f1(pid['yuz']['ort'])} (std {f1(pid['yuz']['std'])}, {f1(pid['yuz']['basari'])}% above 200); Gymnasium heuristic mean {f1(heu['yuz']['ort'])} (std {f1(heu['yuz']['std'])}, {f1(heu['yuz']['basari'])}%). On 500 further seeds: PID {f1(pid['ek500']['ort'])}, heuristic {f1(heu['ek500']['ort'])}. PPO (5 seeds): {f1(P['baseline']['ortalamalarin_ort'])} baseline, {f1(P['A']['ortalamalarin_ort'])} A, {f1(P['C']['ortalamalarin_ort'])} C.

The two kinds of uncertainty differ: the PID is deterministic but its settings were chosen by us; PPO has training randomness (5 runs). The PID got {pa['denenen']} tuning candidates while PPO stayed at defaults, so this is not an equal-budget comparison.

## Findings
- In these 5 seeds, reward B (hackable) was worse than baseline in every seed and showed clear hovering in {len(hover)} of 5.
- Reward C reduced hovering but did not improve the score reliably.
- The advantage of reward A seen on seed 0 did not appear on average over 5 seeds.
- In this setup a tuned PID scored higher with a smaller spread than default-settings PPO. Interpretation (not measured): one million steps may be too few for PPO here, and the PID's landing logic was supplied by hand.

## Limitations
{LIMITS}

## Reproduction
{REPRO} Commands are in `README.md` (Quick start). All numbers in this report come from `docs/sayilar.json`, which is generated from the files in `results/` by `scripts/rapor_sayilari.py`.
"""

OZET = f"""# Özet (basit Türkçe)

**Ne yaptık?** Küçük bir roketi platforma indiren bir yapay zeka (PPO: deneme yanılmayla öğrenen yöntem) eğittik. Sonra onu elle yazdığımız bir PID kontrolcüyle (hatayı ölçüp düzelten klasik yöntem) yarıştırdık.

**Ne öğrendik?**
1. Hile: Ödül kuralını kötü yazınca (B: "dik ve yavaşsan her karede +1") yapay zeka inmek yerine yere yakın bekledi. 5 seed'in {len(hover)} tanesinde bu açıkça görüldü (100 denemenin {', '.join(str(B_tz[i]) for i in hover)} tanesi zaman aşımına uğradı).
2. Seed şansı (seed = rastgelelik tohumu): A kuralı seed 0'da çok iyi çıktı ({f1(sd('A')[0])}), ama 5 seed'de ortalama {f1(P['A']['ortalamalarin_ort'])}; kuralsız model {f1(P['baseline']['ortalamalarin_ort'])}. Fark belirsiz. Tek seed yanıltıcı.
3. Düzeltilmiş kural C hileyi çoğunlukla giderdi ama baseline'dan tutarlı olarak iyi değildi.
4. PID ortalama {f1(pid['yuz']['ort'])} aldı, PPO {f1(P['C']['ortalamalarin_ort'])}-{f1(P['A']['ortalamalarin_ort'])}. Ama PID'e {pa['denenen']} ayar denettik, PPO varsayılan ayarda kaldı. Adil bir bütçe karşılaştırması değil.

**Başvuruda nasıl anlatırsın (3 cümle):** "LunarLander'da PPO ile ödül kurallarını denedim ve kasıtlı hileli bir kuralın yapay zekayı havada bekletmesini gösterdim. Sonucu tek seed'e güvenmeden 5 seed'le test ettim; tek seed'in yanıltıcı olduğunu gördüm. Elle yazdığım PID ile karşılaştırdım ve karşılaştırmanın hangi açılardan adil olmadığını raporda yazdım."

**GitHub'a yüklemek için sana düşenler (ben yapmadım):**
1. Klasörü açıp bak: `.gitignore` bazı dosyaları dışarıda bırakıyor (`.venv`, `STATUS*.md`, `prompts/` vb.). İstersen değiştir.
2. Önce `STATUS.md` içindeki "kişisel bilgi taraması" bölümüne bak. Orada bulunan kişisel bilgileri istersen sil.
3. Klasörde `git init` çalıştır (depo = projenin sürüm geçmişi klasörü), `git add .`, `git commit`.
4. GitHub'da yeni boş depo oluştur, `git remote add origin ...` ve `git push` ile yükle. (Dikkat: `models/` ve `videos/` büyük olabilir, boyutlarına bak.)

**Yapmadıklarımız:** Tek ortam (LunarLander), tek PPO ayarı, sadece 5 seed, Windows bilgisayar. "Güzel durum" eşikleri (0,2 / 0,5 / 0,5) varsayım, ayarlanmadı. Sonuçlar başka oyun veya ödül için geçerli olmayabilir. README ve REPORT İngilizce yazıldı (varsayım; Türkçe istersen söyle). Tekrar üretilebilirlik testi sadece bu bilgisayarda yapıldı.
"""

open("README.md", "w", encoding="utf-8").write(README)
open("REPORT.md", "w", encoding="utf-8").write(REPORT)
open("OZET_TR.md", "w", encoding="utf-8").write(OZET)
print("README.md, REPORT.md, OZET_TR.md yazildi")
