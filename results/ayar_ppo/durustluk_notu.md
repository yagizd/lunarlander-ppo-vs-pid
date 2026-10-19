# Dürüstlük notu (rapora eklenecek metin taslağı)

**Ne yaptık?** PPO'ya (öğrenen yapay zeka yöntemi) 16 farklı ayar denettik (aralıklar süpervizör tarafından sabitlendi, tohum 6001). Seçim sadece tuning seed'leri 0-99 ile yapıldı. Kazanan ayar (ayar 14), seçimde hiç kullanılmamış 5 yeni eğitim seed'iyle (10-14) yeniden eğitildi. Sonra tek sefer seed 1000-1099 ile değerlendirildi.

**Sonuç (ölçüldü):** Bu bütçeyle ayarlı PPO ortalaması 275,7 (seed'ler arası std 6,1; başarı %99,4). PID 248,7 (başarı %97,0). Varsayılan ayarlı PPO 185,9 (başarı %67,8). Yani bu denemede ayarlı PPO, PID'den yüksek çıktı. Önceki "PID, PPO'dan iyi" sonucu **ayar bütçesi eşitsizliğinden etkilenmişti**.

**Hâlâ eşit olmayan noktalar:**
- PPO'ya 16 ayar, PID'e 200 ayar denendi. Sayı olarak eşit değil. (Ama bir PPO ayarı = 1 milyon adımlık eğitim, bir PID ayarı = birkaç saniyelik simülasyon; "bütçe" türleri farklı.)
- PID'in ayarı 20 bölümle yapıldı (en iyi 5'i 100 bölümle), PPO'nun ayarı 100 bölümle yapıldı. Bütçe türleri farklı.
- PPO'nun ayar araması 1 eğitim seed'i (seed 0) ile yapıldı; kazanan ayarın seçimde şansı olabilir. Bunu kontrol etmek için 5 yeni seed kullandık: yeni seed'lerde ortalama 275,7, seçimde (seed 0, tuning seed'leri) 282,4 idi. Fark küçük; yine de bunun tek kontrol olduğunu not et.
- Tek ortam (LunarLander-v3), tek ödül (baseline), 5 seed. Başka oyun veya ödülde sonuç değişebilir.
- PID'in iniş mantığını elle biz yazdık (bilgi verdik). PPO bunu kendi öğrendi. Bu başka bir adaletsizlik türü.
- Değerlendirme başlangıçları (1000-1099) iki yöntemde de aynı; sonuçlar bu 100 başlangıca özgü olabilir. PID için ek 500 bölüm var (241,4), ayarlı PPO için çalıştırılmadı.
- Tek bilgisayar, CPU. Süreler başka işlerden etkilenmiş olabilir.

**Yorum kuralı:** "PPO PID'i yendi" gibi kesin söz kullanma. "Bu bütçeyle, bu 100 başlangıçta, ayarlı PPO'nun ortalaması PID'inkinden yüksekti" de. Sebebi ölçmedik: TAHMİN (ölçülmedi): 16 ayardan biri PPO'nun bu oyun için çok daha iyi çalışmasını sağlamış olabilir (ör. büyük n_steps ve küçük clip_range).
