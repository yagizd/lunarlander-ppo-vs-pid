# Reward shaping on LunarLander-v3: PPO and a PID baseline

## Goal
Show how reward definitions change what PPO learns (including a reward that can be hacked), check whether single-seed results hold over 5 seeds, and compare against a classical PID controller that sees the same 8 numbers.

## Setup
- Environment: LunarLander-v3 (Gymnasium 1.4.0), discrete actions: 0 nothing, 1 and 3 side engines, 2 main engine. Observation: 8 numbers (position x and y, two velocities, tilt, rotation speed, two leg contacts). Game reward as provided by the environment.
- PPO: Stable-Baselines3, `MlpPolicy`, all default hyperparameters, CPU, one million steps per run, training seeds 0-4. No hyperparameter search.
  *Note: this describes Stages 1-5. In Stage 6 (Experiment 5) 16 PPO settings were searched, with the game's own reward only.*
- Evaluation protocol (same for every method): reward wrapper off, the game's own score, deterministic actions, 100 episodes with start seeds 1000-1099. Start seeds 1000+ were never used during training or PID tuning.
- Training logs record the game's real score because the monitor sits inside the reward wrapper.

## Experiment 1: baseline
A random agent scored -174.8 on average (std 108.9; 0 of 100 episodes above 200). The baseline PPO (seed 0) scored 190.4, with 72.0% of episodes above 200.

## Experiment 2: reward variants A, B, C (seed 0)
A: time penalty. B: +1 per frame in a "good state" (upright and slow). C: change in the good-state indicator plus time penalty. Seed 0 means: A 267.6, B 44.2, C 170.3. B timed out in 38 of 100 test episodes (baseline: 1). Frames of the B video show the lander waiting just above the ground, off the platform, with legs not touching until the end of the episode.

## Experiment 3: five seeds
| Method | Mean score (mean ± std across 5 seeds) | Lowest – highest seed mean | Success rate (score > 200) | Mean episode length (steps) | Timeouts |
|---|---|---|---|---|---|
| PPO baseline (game's own reward) | 185.9 ± 31.8 | 132.0 – 213.1 | 67.8% | 413 | 19 / 500 |
| PPO + reward A (time penalty) | 190.5 ± 55.9 | 112.0 – 267.6 | 68.4% | 370 | 18 / 500 |
| PPO + reward B (deliberately hackable) | 36.4 ± 64.7 | -29.7 – 111.7 | 2.2% | 811 | 210 / 500 |
| PPO + reward C (potential-based + time penalty) | 174.0 ± 102.2 | 1.7 – 266.1 | 64.4% | 376 | 35 / 500 |
| PID controller (hand-written, tuned on seeds 0-99) | 248.7 (single controller) | – | 97.0% | 369 | 1 / 100 |
| Gymnasium `heuristic` (reference, not written by us) | 233.1 (single controller) | – | 90.0% | 235 | 0 / 100 |

In these 5 seeds we observed:
- B was below baseline in all 5 seeds. In 3 seeds (seeds 0, 1, 4) there was clear hovering (38, 71, 93 timeouts out of 100). In the other 2 seeds (seeds 2, 3) timeouts were few (5, 3) but episodes were long (765, 677 steps; baseline on the same seeds: 386, 351).
- C removed most hovering (timeouts 210 → 35 of 500) but did not beat baseline consistently. Seed 1 collapsed (mean 1.7).
- A scored 267.6 on seed 0 but 190.5 on average over 5 seeds (baseline 185.9); seed-to-seed std 55.9 and 31.8. The difference is unclear. Looking at one seed would have been misleading.
- Baseline itself varied between seeds: 132.0 to 213.1.
- Training time (measured): 3 runs in parallel took 1361-1379 s each; 8 runs in parallel took 1595-1603 s (first wave) and 1461-1472 s (second wave). The very first single-run baseline took 3010 s (332.2 steps/s). A slowdown from other processes on the machine is possible but not proven.

## Experiment 4: PID vs PPO
The PID controller was written from scratch with two loops: descent speed → main engine, tilt → side engines, plus a dead zone and engines off when both legs touch. Directions of each action were measured before writing it. Gains and thresholds were tuned only on start seeds 0-99: 200 candidate settings scored on 20 episodes, the best 5 re-scored on 100, the best frozen (seed 0-99 mean 246.8). Setting the integral gains to zero on the same 5 candidates gave seed 0-99 means of 251.0, 214.4, 238.5, 271.0, 162.3 (not re-tuned), so the integral term does not look necessary here.

On seeds 1000-1099: PID mean 248.7 (std 31.2, 97.0% above 200); Gymnasium heuristic mean 233.1 (std 111.4, 90.0%). On 500 further seeds: PID 241.4, heuristic 235.4. PPO (5 seeds): 185.9 baseline, 190.5 A, 174.0 C.

The two kinds of uncertainty differ: the PID is deterministic but its settings were chosen by us; PPO has training randomness (5 runs). The PID got 200 tuning candidates while PPO stayed at defaults, so this is not an equal-budget comparison.

*Superseded by Experiment 5 below: in Stage 6 PPO also got a tuning budget (16 settings), and the result changed.*

## Experiment 5: fairer comparison (Stage 6)
**Why.** In Experiment 4 the PID had 200 tuning candidates and PPO had none. Equal numbers are not possible (200 PPO settings of one million steps each would take about 83 hours, an estimate, not measured), so PPO got a limited budget of 16 settings.

**Method.**
- 16 settings were drawn at random with `numpy.random.default_rng(6001)` from fixed ranges chosen by the project supervisor (not taken from a source; wide on purpose). Only the game's own reward was used (no reward wrapper). Default values below are read from the installed Stable-Baselines3 2.9.0.

| Setting | Range | SB3 default |
|---|---|---|
| learning_rate | 1e-4 to 2e-3, log-uniform | 0.0003 |
| n_steps | 512, 1024, 2048, 4096 | 2048 |
| batch_size | 64, 128, 256, 512 (must divide n_steps) | 64 |
| n_epochs | 5, 10, 20 | 10 |
| gamma | 0.98, 0.99, 0.995, 0.999 | 0.99 |
| gae_lambda | 0.9, 0.95, 0.98 | 0.95 |
| ent_coef | 0, 1e-4, 1e-3, 1e-2 | 0.0 |
| clip_range | 0.1, 0.2, 0.3 | 0.2 |
| net_arch | [64,64], [128,128], [256,256] | [64,64] |

- Each setting: one million steps, training seed 0. The 16 settings are in `results/ayar_ppo/ayarlar.json`.
- **Selection used only tuning seeds 0-99** (100 episodes, wrapper off, deterministic). The selection script asserts that seeds stay in 0-99. Start seeds 1000-1099 were not looked at during selection.
- The winner was retrained with **5 new training seeds (10-14)** (so the choice made with seed 0 does not bias the final numbers) and evaluated **once** on seeds 1000-1099 (100 episodes each, wrapper off, deterministic).

**Selection results (seeds 0-99, training seed 0):**

| setting | mean score | std | success % (>200) | timeouts |
|---|---|---|---|---|
| 0 | 118.5 | 79.6 | 7 | 16 |
| 1 | 216.6 | 68.3 | 89 | 2 |
| 2 | 115.6 | 92.4 | 10 | 24 |
| 3 | 87.9 | 117.0 | 17 | 9 |
| 4 | -92.1 | 68.4 | 0 | 32 |
| 5 | 184.6 | 64.2 | 47 | 14 |
| 6 | 261.1 | 54.4 | 92 | 3 |
| 7 | 41.0 | 128.6 | 10 | 5 |
| 8 | 40.9 | 113.1 | 13 | 1 |
| 9 | 221.7 | 46.1 | 78 | 7 |
| 10 | 88.9 | 126.2 | 28 | 20 |
| 11 | 219.5 | 73.3 | 81 | 12 |
| 12 | 175.4 | 104.9 | 69 | 0 |
| 13 | 165.7 | 95.8 | 56 | 9 |
| **14** | **282.4** | 22.0 | 100 | 0 |
| 15 | 232.8 | 61.9 | 80 | 16 |

**Chosen setting 14:** learning_rate 0.00102, n_steps 4096, batch_size 128, n_epochs 10, gamma 0.995, gae_lambda 0.98, ent_coef 0.001, clip_range 0.1, net_arch [64,64].

**Final evaluation (start seeds 1000-1099, 100 episodes per model):**

| Method | Mean score (mean ± std across seeds) | Success rate (score > 200) | Mean episode length | Timeouts |
|---|---|---|---|---|
| PPO default settings (5 seeds, 0-4) | 185.9 ± 31.8 | 67.8% | 413 | 19 / 500 |
| PPO tuned (setting 14, 5 new seeds 10-14) | 275.7 ± 6.1 (seed means 266.2 – 281.6) | 99.4% | 233 | 2 / 500 |
| PID (200 candidates) | 248.7 (single controller) | 97.0% | 369 | 1 / 100 |
| Gymnasium `heuristic` (reference) | 233.1 (single controller) | 90.0% | 235 | 0 / 100 |
| Random agent | -174.8 | 0.0% | – | – |

Training time (measured from log timestamps and `sure.txt`): the 16 tuning runs (two waves of 8) took 82 min 10 s in total; single runs 1228-2663 s. The 5 retrainings took about 1488 s each (5 in parallel).

**Cautions.**
- The budgets are still not equal: 16 PPO settings vs. 200 PID settings, and different kinds of budget (a PPO setting is a one-million-step training, a PID setting is a short simulation).
- The PID settings were scored on 20 episodes (the best 5 on 100), PPO settings on 100 episodes.
- The PPO search used one training seed, so the winner may have been lucky. On the 5 new seeds its mean was 275.7 (282.4 in selection): a small drop, but only one check.
- The PID's landing logic was written by hand; PPO learned its own.
- The result is for one environment, one reward (game's own), 5 seeds, and these 100 start seeds. No 500-episode extra check was run for tuned PPO (the PID has one: 241.4).
- Why setting 14 works well was not measured. Interpretation (not measured): a large n_steps (4096) and a small clip_range (0.1) may matter.

## Findings
- In these 5 seeds, reward B (hackable) was worse than baseline in every seed and showed clear hovering in 3 of 5.
- Reward C reduced hovering but did not improve the score reliably.
- The advantage of reward A seen on seed 0 did not appear on average over 5 seeds.
- In this setup a tuned PID scored higher with a smaller spread than default-settings PPO. Interpretation (not measured): one million steps may be too few for PPO here, and the PID's landing logic was supplied by hand.
  *Superseded by Experiment 5: with 16 tuning settings, PPO's mean was higher than the PID's (see the next finding).*
- In Stage 6, in this setup, with this budget, on these 100 start seeds, tuned PPO's mean score (275.7 ± 6.1 over 5 new seeds) was higher than the PID's (248.7) and the heuristic's (233.1), and its spread across seeds was small. The comparison is still not equal (16 vs. 200 settings, different budget types). The reason was not measured.

## Limitations
- One environment (LunarLander-v3), one reward definition set, one PPO setting (library defaults), 5 seeds.
  *Stages 1-5. Stage 6 later added a 16-setting search for PPO with the game's own reward only.*
- The "good state" thresholds (0.2 / 0.5 / 0.5 for tilt, horizontal speed, vertical speed) are an assumption and were not tuned. The B and C results may depend on them.
- All methods are evaluated on the same 100 start seeds (1000-1099). This makes the comparison fair, but the numbers may be specific to these 100 starts.
- PPO was not given the tuning budget that the PID received.
  *Superseded by Experiment 5: PPO later got 16 tuning settings.*
- Stage 6 budgets are still not equal: PPO got 16 settings, the PID 200 (different kinds of budget).
- The PID's settings were scored on 20 episodes (the best 5 on 100); PPO's settings on 100 episodes.
- The PPO setting search used one training seed (seed 0), so the chosen setting may have been lucky (5 new seeds were used as a check).
- The PID's landing logic was written by hand; PPO learned its own.
- Stage 6 numbers may be specific to the 100 start seeds (1000-1099); no extra 500-episode check was run for tuned PPO (the PID has one: 241.4).
- Why the tuned PPO setting works well was not measured.
- One computer (Windows, CPU only). Training times may have been affected by other processes.
- The Gymnasium `heuristic` reference was not written by us.

## Reproduction
Saved models and the frozen PID were re-evaluated in a fresh virtual environment built from `requirements-min.txt` and matched the stored CSVs episode by episode (PPO baseline, A, C seed 0, PID, heuristic). Two separate 50000-step baseline trainings (seed 0, one thread) produced bit-for-bit identical weights and identical scores on 20 start seeds. This was checked on one machine only (Windows 11, CPU). Commands are in `README.md` (Quick start). All numbers in this report come from `docs/sayilar.json`, which is generated from the files in `results/` by `scripts/rapor_sayilari.py`. The Stage 6 numbers (Experiment 5) are **not** in `docs/sayilar.json`; they were recomputed by hand-checked script from `results/ayar_ppo/` files.

**Stage 6 commands** (all scripts and options exist; `--help` was checked for the two scripts that take options). All commands use the project virtual environment:

```
python scripts/ayar_ppo_uret.py          # draws the 16 settings (seed 6001); no options; OVERWRITES results/ayar_ppo/ayarlar.json
python scripts/dalga_surucu_ayar.py      # trains settings 0-15 (1M steps, seed 0), two waves of 8, stops after 90 min
python scripts/ayar_sec_ppo.py           # scores models on seeds 0-99 only, writes secim_tablosu.md and the winner
python scripts/egit_ppo_ayar.py --ayar_id 14 --seed 10 --adim 1000000 --cikti kazanan_seed10   # repeat for seeds 11-14
python scripts/degerlendir_v2.py --model models/ayar_ppo/kazanan_seed10.zip --etiket ayar_ppo/kazanan_seed10   # repeat for 11-14
python scripts/adil_karsilastir.py       # final table and plot in results/ayar_ppo/
```

The Stage 6 results were **not re-verified in a fresh environment** (only Stages 1-5 were).
