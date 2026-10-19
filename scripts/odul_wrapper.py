import gymnasium as gym


def guzel_mi(obs):
    # "Guzel durum" = dik ve yavas. [VARSAYIM: esikler makul secildi, ayar yapilmadi]
    # obs: 0 x, 1 y, 2 yatay hiz, 3 dikey hiz, 4 egim, 5 donme hizi, 6 sol bacak, 7 sag bacak
    return abs(obs[4]) < 0.2 and abs(obs[2]) < 0.5 and abs(obs[3]) < 0.5


class OdulWrapper(gym.Wrapper):
    """Oyunun kendi odulune ekleme yapar.
    A: her karede -0.05 (zaman cezasi)
    B: her karede guzel durumsa +1 (HILE KURALI: beklemek odullendirilir)
    C: phi = 1 (guzel) / 0; ekleme = phi_yeni - phi_eski, ve her karede -0.05
    """

    def __init__(self, env, varyant):
        super().__init__(env)
        assert varyant in ("A", "B", "C")
        self.varyant = varyant
        self.phi_eski = 0.0

    def reset(self, **kw):
        obs, info = self.env.reset(**kw)
        self.phi_eski = 1.0 if guzel_mi(obs) else 0.0  # ilk karede ekleme 0
        return obs, info

    def step(self, action):
        obs, r, term, trunc, info = self.env.step(action)
        if self.varyant == "A":
            r += -0.05
        elif self.varyant == "B":
            r += 1.0 if guzel_mi(obs) else 0.0
        else:
            phi = 1.0 if guzel_mi(obs) else 0.0
            r += (phi - self.phi_eski) - 0.05
            self.phi_eski = phi
        return obs, r, term, trunc, info
