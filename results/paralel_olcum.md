# Paralel hız ölçümü (hepsi ÖLÇÜLDÜ)
Her süreç: PPO MlpPolicy, LunarLander-v3, 50.000 adım, torch.set_num_threads(1), CPU. Script: scripts/paralel_olcum.py
Karşılaştırma: Aşama 0 tek süreç = 740,4 adım/sn (torch varsayılan thread sayısı). Aşama 1 ana eğitim (1M adım, tek süreç, arka planda başka proje çalışırken) = 332,2 adım/sn.

## 4 eşzamanlı süreç (toplam duvar süresi 152,0 sn)
| seed | süre (sn) | adım/sn |
|---|---|---|
| 0 | 103,9 | 481,0 |
| 1 | 105,3 | 474,7 |
| 2 | 113,0 | 442,6 |
| 3 | 131,5 | 380,3 |
Toplam hız ≈ 1778 adım/sn.

## 8 eşzamanlı süreç (toplam duvar süresi 123,0 sn)
| seed | süre (sn) | adım/sn |
|---|---|---|
| 0 | 98,4 | 507,9 |
| 1 | 98,7 | 506,6 |
| 2 | 103,5 | 483,0 |
| 3 | 98,3 | 508,4 |
| 4 | 98,0 | 510,2 |
| 5 | 99,5 | 502,3 |
| 6 | 97,9 | 510,9 |
| 7 | 107,6 | 464,7 |
Toplam hız ≈ 3994 adım/sn.

## Yorum
- 8 süreçte her biri ~500 adım/sn. Tek süreç 740 adım/sn'den yavaş ama toplam çok daha hızlı.
- 4 süreç testi 8 süreçten YAVAŞ çıktı. Bunun sebebini BİLMİYORUM. Ölçüm sırasında bilgisayarda başka işler (başka bir proje) çalışıyor olabilir, kontrol etmedim. Tek tekrar var, gürültü olabilir.
- 16+ süreç denenmedi. BİLMİYORUM.
