# PID ve PPO karşılaştırması (hepsi: oyunun kendi ödülü, wrapper yok, seed 1000-1099)

| yöntem | ortalama skor | std (denemeler arası) | başarı oranı (skor>200) | ort. uzunluk | zaman aşımı |
|---|---|---|---|---|---|
| PPO baseline | 185.9 ± 31.8 (seed'ler arası) | 94.8 | %67.8 (500 denemede) | 413 | 19 / 500 |
| PPO A (zaman cezası) | 190.5 ± 55.9 (seed'ler arası) | 103.3 | %68.4 (500 denemede) | 370 | 18 / 500 |
| PPO C (düzeltilmiş) | 174.0 ± 102.2 (seed'ler arası) | 126.3 | %64.4 (500 denemede) | 376 | 35 / 500 |
| PID (dondurulmuş) | 248.7 (tek kontrolcü) | 31.2 | %97 (100 denemede) | 369 | 1 / 100 |
| Gymnasium heuristic (hazır referans) | 233.1 (tek kontrolcü) | 111.4 | %90 (100 denemede) | 235 | 0 / 100 |

Not: PPO satırları 5 seed (5 ayrı eğitim) × 100 deneme. PID ve heuristic tek kontrolcü × 100 deneme. PPO B (bilerek bozuk kural) tabloya konmadı; sonuçları Aşama 3'te.

## Ek güven (ana karşılaştırmayı değiştirmez)
- pid, ek 500 deneme (seed 1100-1599): ort 241.4, std 48.2, başarı %94.4, zaman aşımı 7
- heuristic, ek 500 deneme (seed 1100-1599): ort 235.4, std 110.9, başarı %89.2, zaman aşımı 7
