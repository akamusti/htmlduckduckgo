# DuckDuckGo HTML Search

Chrome adres çubuğundaki aramaları DuckDuckGo'nun hafif HTML arayüzüne yönlendirir. Eklenti simgesine tıklayarak açılan arama penceresinden de yeni bir arama sekmesi açabilirsin.

## Chrome'a yükle

1. `dist/htmlduckduckgo-chrome.zip` dosyasını indirip bir klasöre çıkar.
2. Chrome'da `chrome://extensions` adresini aç ve **Geliştirici modu**'nu etkinleştir.
3. **Paketlenmemiş öğe yükle**'ye tıkla ve çıkardığın klasörü seç.
4. Chrome varsayılan arama motorunu değiştirmek için onay isterse onayla.

Yükledikten sonra adres çubuğuna aramanı yazıp Enter'a basabilir veya araç çubuğundaki eklenti simgesinden hızlı arama yapabilirsin. Chrome'un izin/onay ekranı tarayıcı tarafından yönetilir; eklenti ayarı sessizce değiştirmez.

## Varsayılanı geri al

`chrome://extensions` sayfasından eklentiyi kaldır. Gerekirse Chrome **Ayarlar → Arama motoru** bölümünden önceki arama motorunu yeniden seç.

## Sürümü oluştur ve test et

Python 3 gereklidir; ek paket kurulumu gerekmez.

```sh
python3 scripts/package_extension.py
python3 -m unittest discover -s tests
```

Üretilen ZIP, Chrome Web Store'a yüklenebilir ve **Paketlenmemiş öğe yükle** ile kurulabilir. Arşiv yalnızca eklentinin çalışması için gereken manifest, popup dosyaları ve simgeleri içerir.
