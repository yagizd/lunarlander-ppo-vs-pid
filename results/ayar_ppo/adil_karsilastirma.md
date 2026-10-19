# Adil karşılaştırma (Bütçe A: PPO'ya 16 ayar)

Hepsi: wrapper kapalı, oyunun kendi skoru, deterministik, 100 bölüm, başlangıç seed 1000-1099.
PPO satırlarında 'ortalama ± std' = 5 seed'in ortalamalarının ortalaması ± seed'ler arası std (ddof=1). 'std (bölümler)' = tüm bölümlerin skor yayılımı.

| yöntem | ortalama skor | std (bölümler) | başarı (skor>200) | ort. uzunluk | zaman aşımı | en düşük – en yüksek seed ort. |
|---|---|---|---|---|---|---|
| PPO varsayılan ayar (seed 0-4) | 185.9 ± 31.8 | 94.8 | %67.8 | 413 | 19 / 500 | 132.0 – 213.1 |
| PPO ayarlı (16 ayardan seçilen, seed 10-14) | 275.7 ± 6.1 | 21.1 | %99.4 | 233 | 2 / 500 | 266.2 – 281.6 |
| PID (200 ayar) | 248.7 (tek kontrolcü) | 31.2 | %97.0 | 369 | 1 / 100 | – |
| Gymnasium heuristic | 233.1 (tek kontrolcü) | 111.4 | %90.0 | 235 | 0 / 100 | – |
| Rastgele ajan | -174.8 (tek ölçüm) | 108.9 | %0.0 | – | – | – |

PID ek 500 bölüm (seed 1100-1599, ayrı dosya): ort 241.4. Ayarlı PPO için ek 500 bölüm çalıştırılmadı.

Seçim: ayar 14 (tuning seed 0-99'da ortalama 282.4). Eski/yeni sonuç dosyaları: results/baseline*_eval.csv, results/ayar_ppo/kazanan_seed*_eval.csv.
