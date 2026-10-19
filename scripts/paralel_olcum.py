import sys, time, subprocess

ADIM = 50_000


def tek(seed):
    import torch
    torch.set_num_threads(1)
    import gymnasium as gym
    from stable_baselines3 import PPO
    model = PPO("MlpPolicy", gym.make("LunarLander-v3"), seed=seed, device="cpu", verbose=0)
    t0 = time.perf_counter()
    model.learn(total_timesteps=ADIM)
    dt = time.perf_counter() - t0
    print(f"SONUC seed={seed} sure={dt:.1f} hiz={ADIM/dt:.1f}", flush=True)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "tek":
        tek(int(sys.argv[2]))
    else:
        n = int(sys.argv[1])
        t0 = time.perf_counter()
        ps = [subprocess.Popen([sys.executable, __file__, "tek", str(s)], stdout=subprocess.PIPE, text=True) for s in range(n)]
        for p in ps:
            out = p.communicate()[0]
            print([l for l in out.splitlines() if l.startswith("SONUC")][0], flush=True)
        print(f"TOPLAM_DUVAR_SURESI {time.perf_counter()-t0:.1f}")
