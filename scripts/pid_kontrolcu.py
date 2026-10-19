"""Sıfırdan yazılmış PID kontrolcü (LunarLander-v3). gymnasium'un heuristic fonksiyonu KOPYALANMADI.

Ölçülmüş yönler (scripts/yon_testi.py):
  eylem 0 = hiçbir şey
  eylem 1 = yan motor: eğimi (obs[4]) ARTIRIR (+), dönme hızını (+) artırır, yatay hızı biraz sola (-) iter
  eylem 2 = ana motor: dikey hızı (obs[3]) artırır
  eylem 3 = diğer yan motor: eğimi AZALTIR (-), yatay hızı biraz sağa (+) iter
  obs[0] = 0 platformun tam ortası; obs[0] > 0 platformun SAĞINDA.
  Pozitif eğim + ana motor -> yatay hız sola (-) gider; negatif eğim -> sağa (+).
  Bu yüzden roket sağdaysa (x>0) pozitif eğim istenir.
"""
import numpy as np


class PID:
    """Klasik PID: P = şimdiki hata, I = biriken hata, D = hatanın değişimi."""

    def __init__(self, kp, ki, kd, cikis_min=-1.0, cikis_max=1.0):
        self.kp, self.ki, self.kd = kp, ki, kd
        self.cikis_min, self.cikis_max = cikis_min, cikis_max  # çıktıyı sınırla
        self.reset()

    def reset(self):
        self.toplam = 0.0      # biriken hata (I terimi için)
        self.onceki_hata = None  # bir önceki karedeki hata (D terimi için)

    def adim(self, hata, d_hata=None):
        """hata: hedef - gerçek. d_hata verilirse D terimi için onu kullan (örn. ölçülen dönme hızı)."""
        self.toplam += hata
        self.toplam = float(np.clip(self.toplam, -50.0, 50.0))  # birikim şişmesin
        if d_hata is None:  # verilmediyse hatanın kareler arası farkını al
            d_hata = 0.0 if self.onceki_hata is None else hata - self.onceki_hata
        self.onceki_hata = hata
        cikis = self.kp * hata + self.ki * self.toplam + self.kd * d_hata
        return float(np.clip(cikis, self.cikis_min, self.cikis_max))


VARSAYILAN = dict(
    vh0=0.10, vh1=0.50,        # hedef iniş hızı = -(vh0 + vh1*yükseklik): yüksekte hızlı, yerde yavaş
    kp_h=1.0, ki_h=0.0, kd_h=0.0, esik_ana=0.05,   # yükseklik döngüsü ve ana motor eşiği (ölü bölge)
    ax=0.5, avx=1.0, amax=0.4,                      # hedef eğim = ax*x + avx*vx, ±amax ile sınırlı
    kp_a=1.0, ki_a=0.0, kd_a=0.3, esik_yan=0.05,   # eğim döngüsü ve yan motor eşiği
    yan_oncelik=0.5,                                # eğim hatası bundan büyükse ana motor kapalı
)


class PIDKontrol:
    def __init__(self, p=None):
        self.p = dict(VARSAYILAN, **(p or {}))
        self.yuk = PID(self.p["kp_h"], self.p["ki_h"], self.p["kd_h"], -1.0, 1.0)
        self.egim = PID(self.p["kp_a"], self.p["ki_a"], self.p["kd_a"], -1.0, 1.0)

    def reset(self):
        self.yuk.reset(); self.egim.reset()

    def act(self, obs):
        p = self.p
        x, y, vx, vy, ang, w, sol, sag = [float(v) for v in obs]
        if sol and sag:           # iki bacak da yerde: motorları kapat, sakin dur
            return 0
        # --- 1) yükseklik / iniş hızı döngüsü (ana motor) ---
        hedef_vy = -(p["vh0"] + p["vh1"] * max(y, 0.0))        # yere yaklaştıkça yavaş
        hata_h = hedef_vy - vy                                   # >0: çok hızlı düşüyoruz, motor yak
        cikis_h = self.yuk.adim(hata_h)
        # --- 2) duruş (eğim) döngüsü (yan motorlar) ---
        hedef_ang = float(np.clip(p["ax"] * x + p["avx"] * vx, -p["amax"], p["amax"]))  # platforma doğru hafif yat
        hata_a = hedef_ang - ang
        # D terimi: hata türevi ~ -dönme hızı (hedef yavaş değişir), ölçülen w kullanılır
        cikis_a = self.egim.adim(hata_a, d_hata=-w)
        # --- 3) sürekli çıktıyı 4 ayrık eyleme çevir ---
        if cikis_a > p["esik_yan"]:     # eğimi artırmak lazım -> eylem 1
            return 1
        if cikis_a < -p["esik_yan"]:    # eğimi azaltmak lazım -> eylem 3
            return 3
        if abs(hata_a) > p["yan_oncelik"]:  # eğim çok bozuksa ana motoru yakma (zaten yukarıda yan motor çalışır)
            return 0
        if cikis_h > p["esik_ana"]:     # ana motor
            return 2
        return 0                        # ölü bölge: hiçbir şey yapma
