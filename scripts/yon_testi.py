import numpy as np, gymnasium as gym
np.set_printoptions(precision=3, suppress=True)
env = gym.make("LunarLander-v3")
# Rüzgar/türbülans kapalı (varsayılan). Aynı başlangıç için seed sabit.
for eylem in (0, 1, 2, 3):
    obs, _ = env.reset(seed=5)
    print(f"--- eylem {eylem} ---  baslangic", obs)
    for k in range(8):
        obs, r, t, tr, _ = env.step(eylem)
        if k in (0, 3, 7): print(f" kare{k+1}", obs)
# Bayrak / platform konumu
u = env.unwrapped
print("helipad_x1, helipad_x2 (piksel/dunya):", u.helipad_x1, u.helipad_x2, "W:", 600/30)
print("platform ortasi gozlemde x = ", ((u.helipad_x1+u.helipad_x2)/2 - 600/30/2) / (600/30/2))
# Iki ayri baslangicta roketin x'i: pozitif x'te roket platformun neresinde?
for sd in (1, 2, 3):
    obs, _ = env.reset(seed=sd)
    print("seed", sd, "obs x =", round(float(obs[0]), 3), " govde x(dunya) =", round(u.lander.position.x, 2), " platform orta x(dunya) =", round((u.helipad_x1+u.helipad_x2)/2, 2))

# Ek olcum: once yan motorla egimi bozalim, sonra ana motoru yakip yatay hiz nereye gidiyor?
for yan in (1, 3):
    obs, _ = env.reset(seed=5)
    for _ in range(10): obs, *_ = env.step(yan)
    ang = float(obs[4]); vx0 = float(obs[2])
    for _ in range(10): obs, *_ = env.step(2)
    print(f"yan motor {yan}: egim={ang:+.3f}; sonra 10 kare ana motor: yatay hiz {vx0:+.3f} -> {float(obs[2]):+.3f}")
