# Özet (basit Türkçe)

**Ne yaptık?** Küçük bir roketi platforma indiren bir yapay zeka (PPO: deneme yanılmayla öğrenen yöntem) eğittik. Sonra onu elle yazdığımız bir PID kontrolcüyle (hatayı ölçüp düzelten klasik yöntem) yarıştırdık.

**Ne öğrendik?**
1. Hile: Ödül kuralını kötü yazınca (B: "dik ve yavaşsan her karede +1") yapay zeka inmek yerine yere yakın bekledi. 5 seed'in 3 tanesinde bu açıkça görüldü (100 denemenin 38, 71, 93 tanesi zaman aşımına uğradı).
2. Seed şansı (seed = rastgelelik tohumu): A kuralı seed 0'da çok iyi çıktı (267.6), ama 5 seed'de ortalama 190.5; kuralsız model 185.9. Fark belirsiz. Tek seed yanıltıcı.
3. Düzeltilmiş kural C hileyi çoğunlukla giderdi ama baseline'dan tutarlı olarak iyi değildi.
4. PID ortalama 248.7 aldı, PPO 174.0-190.5. Ama PID'e 200 ayar denettik, PPO varsayılan ayarda kaldı. Adil bir bütçe karşılaştırması değil.

**GÜNCELLEME (Aşama 6):** PPO'ya 16 farklı ayar (öğrenme ayarları: öğrenme hızı, ağ boyutu gibi) denettik. Ayarı seçerken sadece seed 0-99'a baktık, 1000-1099'a hiç bakmadık. En iyi ayar PID'i geçti: 275.7'ye karşı 248.7. Bu ayarı seçimde hiç kullanılmamış 5 yeni seed'le yeniden eğittik; sonuç yine yüksek ve seed'ler arasında az değişti (266.2 ile 281.6 arası). Yani **bu bütçeyle, bu 100 başlangıçta** ayarlı PPO'nun ortalaması PID'den yüksek çıktı. Önceki "PID daha iyi" sonucu, PID'e 200 ayar verilip PPO'nun ayarlanmamasından etkilenmiş görünüyor. Ama karşılaştırma yine tam eşit değil (PPO'ya 16, PID'e 200 ayar; PID'in iniş mantığını biz elle yazdık, PPO kendi öğrendi). Ayarlı PPO'nun neden iyi çıktığını ölçmedik.

**Başvuruda nasıl anlatırsın (3 cümle):** "LunarLander'da PPO ile ödül kurallarını denedim ve kasıtlı hileli bir kuralın yapay zekayı havada bekletmesini gösterdim. Sonucu tek seed'e güvenmeden 5 seed'le test ettim; tek seed'in yanıltıcı olduğunu gördüm. Elle yazdığım PID ile karşılaştırdım; PID'e 200 ayar verip PPO'yu ayarlamamak adaletsizdi, bu yüzden PPO'ya da 16 ayar verdim ve sonucun tersine döndüğünü (ayarlı PPO 275.7, PID 248.7) raporladım. Karşılaştırma yine de tam eşit değil ve bunu raporda açıkça yazdım."

(Eski, Aşama 5'teki cümle şuydu: "Elle yazdığım PID ile karşılaştırdım ve karşılaştırmanın hangi açılardan adil olmadığını raporda yazdım." Eski dosya: `OZET_TR_asama5.md`.)

**GitHub'a yüklemek için sana düşenler (ben yapmadım):**
1. Klasörü açıp bak: `.gitignore` bazı dosyaları dışarıda bırakıyor (`.venv`, `STATUS*.md`, `prompts/` vb.). İstersen değiştir. Dikkat: `README_asama5.md`, `REPORT_asama5.md`, `OZET_TR_asama5.md` eski sürüm yedekleri `.gitignore`'da DEĞİL; yüklemek istemiyorsan sil ya da `.gitignore`'a ekle.
2. Önce `STATUS.md` içindeki "kişisel bilgi taraması" bölümüne bak. Orada bulunan kişisel bilgileri istersen sil.
3. Klasörde `git init` çalıştır (depo = projenin sürüm geçmişi klasörü), `git add .`, `git commit`.
4. GitHub'da yeni boş depo oluştur, `git remote add origin ...` ve `git push` ile yükle. (Dikkat: `models/` ve `videos/` büyük olabilir, boyutlarına bak.)

**Yapmadıklarımız:** Tek ortam (LunarLander), sadece 5 seed, Windows bilgisayar. PPO'ya 16 ayar denendi, ama PID'e 200 ayar denmişti (eşit değil). Ayarlı PPO için ek 500 bölümlük kontrol yapılmadı. "Güzel durum" eşikleri (0,2 / 0,5 / 0,5) varsayım, ayarlanmadı. Sonuçlar başka oyun veya ödül için geçerli olmayabilir. README ve REPORT İngilizce yazıldı (varsayım; Türkçe istersen söyle). Tekrar üretilebilirlik testi sadece bu bilgisayarda yapıldı; Aşama 6 sonuçları temiz ortamda tekrar test edilmedi.
