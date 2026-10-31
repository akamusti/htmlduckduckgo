# DuckDuckGo HTML Search

Chrome araç çubuğundaki eklenti popup'ından veya adres çubuğunda `ddg` yazıp **Tab**'a bastıktan sonra arama yap. Aramalar DuckDuckGo'nun hafif HTML arayüzünde açılır.

## Platforma göre indirme

Chrome'un `chrome_settings_overrides` özelliği yalnızca macOS ve Windows'ta desteklenir. Linux veya ChromeOS'ta bu anahtar eklentinin yüklenmesini engelleyebilir.

- **Linux / ChromeOS / platformdan bağımsız:** `htmlduckduckgo-chrome.zip` dosyasını indirip çıkar, `chrome://extensions` sayfasından **Geliştirici modu → Paketlenmemiş öğe yükle** ile klasörü seç. Arama popup'ı ve `ddg` adres çubuğu kısayolu çalışır.
- **macOS / Windows, DuckDuckGo'yu varsayılan yapmak için:** `htmlduckduckgo-chrome-desktop-search-override.zip` dosyasını indirip çıkar ve aynı şekilde klasörü yükle. Chrome varsayılan arama motoru değişikliğini onaylatabilir.

ChromeOS veya Linux'ta eklenti kurulduktan sonra DuckDuckGo'yu Chrome ayarlarından varsayılan yapmak için **Ayarlar → Arama motoru → Arama motorlarını ve site aramasını yönet → Site araması ekle** bölümünde aşağıdaki değerleri kullan:

- Arama motoru: `DuckDuckGo HTML`
- Kısayol: `duckduckgo.com`
- URL: `https://html.duckduckgo.com/html/?q=%s`

Ardından kaydı varsayılan yap. Bu adım Chrome'un platform kısıtlaması nedeniyle gereklidir; eklentiler Linux/ChromeOS'ta arama motoru ayarını manifest üzerinden değiştiremez.

Her iki pakette de popup araması ve `ddg` + **Tab** adres çubuğu araması kullanılabilir.

## Sürümü oluştur ve test et

Python 3 gereklidir; ek paket kurulumu gerekmez.

```sh
python3 scripts/package_extension.py
python3 -m unittest discover -s tests
```

Betik platform kısıtlı manifest anahtarını içermeyen taşınabilir ZIP'i ve sadece macOS/Windows için arama motoru override'ı eklenmiş ZIP'i oluşturur.
