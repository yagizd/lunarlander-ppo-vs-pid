# Roket İndirme — Yol Haritası (onaylandı: 15 Ekim 2026)
Hedef: 2-3 günde LunarLander + PPO + ödül kuralı deneyleri (hile ve düzeltme) + 5 seed + PID karşılaştırması + rapor.

| Aşama | İş | Bitti sayılır, eğer… |
|---|---|---|
| 0. Ölçüm (~1 saat) | Ortam kur, 50k adım ile süre ölç | 3 paket çalışıyor, süre STATUS.md'de |
| 1. Temel model (Gün 1) | Rastgele video, PPO eğitimi | 10+ denemede ort. skor 200+, iniş videosu |
| 2. Ödül kuralları (Gün 1-2) | Wrapper: A) zaman cezası, B) +1 hilesi, C) düzeltme | Her biri için eğitim + video, B'de roket asılı kalıyor |
| 3. Çoklu deneme (Gün 2) | Her ayar 5 seed, test wrapper kapalı | Ortalama ± yayılım tablosu, grafik |
| 4. PID yarışı (Gün 3) | PID yaz, PPO ile aynı testte karşılaştır | Tabloda yan yana, aynı ölçüt |
| 5. Teslim (Gün 3) | README, rapor, videolar | Temiz klasörde sonuç tekrar üretiliyor |

Riskler: süre tahmini (Aşama 0 ölçecek), Windows'ta Box2D/swig kurulumu, PID'in 4 ayrık eyleme çevrilmesi.
Kesme kuralı: Aşama 3 süresi ölçümün 2 katını aşarsa seed 5 -> 3.
