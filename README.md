# USOM-API-Converter (Firewall Tehdit İstihbaratı Otomasyonu) 🛡️🚀

[![USOM-API-Converter](https://github.com/beratcemzengin/USOM-API-Converter/actions/workflows/usom_job.yml/badge.svg)](https://github.com/beratcemzengin/USOM-API-Converter/actions/workflows/usom_job.yml)

> 💡 **Hızlı Kullanım (Hazır Liste):**
> Kendi GitHub altyapınızı kurmakla uğraşmak istemiyorsanız, bu deponun her gün otomatik ürettiği güncel listeleri doğrudan kullanabilirsiniz:
> 
> - 🔗 **IP Listesi:** `https://raw.githubusercontent.com/beratcemzengin/USOM-API-Converter/main/usom_ip.txt`
> - 🔗 **Domain Listesi:** `https://raw.githubusercontent.com/beratcemzengin/USOM-API-Converter/main/usom_domain.txt`

---

Siber Güvenlik Başkanlığı'nın (SGB) yeni API servisleri üzerinden sunduğu tehdit beslemesini, kurumsal güvenlik duvarlarının (Firewall - Palo Alto, FortiGate, Cisco vb.) doğrudan tüketebileceği formata dönüştüren otomatik bir projedir.

## 🌟 Neler Yeni?
* **Segmentasyon:** Tehditler artık IP (L3/L4) ve Domain (L7) olarak iki ayrı dosyada sunulur.
* **Yüksek Hız:** `per-page=1000` parametresi ile tüm veritabanı saniyeler içinde taranır.
* **Akıllı Filtreleme:** Cihaz limitlerini (RAM/TCAM) korumak için sadece **son 1 yılın** aktif tehditleri baz alınır.
* **Otomasyon:** GitHub Actions üzerinde serverless altyapıda, her gün otomatik güncellenir.

---

## 🔗 Firewall Entegrasyon Rehberi

### 🛡️ Palo Alto Networks (EDL)
1. **Objects > External Dynamic Lists** yoluna gidin ve iki ayrı liste ekleyin.
2. **IP Listesi:** `Type: IP List` seçin ve `usom_ip.txt` linkini girin.
3. **Domain Listesi:** `Type: Domain List` seçin ve `usom_domain.txt` linkini girin.
4. Güvenlik kurallarınızda bu nesneleri `Destination` (IP) ve `URL Category` (Domain) alanlarında `Drop/Block` aksiyonu ile tanımlayın.

### 🛡️ Fortinet (FortiGate)
1. **Security Fabric > Fabric Connectors > Threat Feeds** yoluna gidin.
2. IP'ler için `IP Address`, Domain'ler için `Domain` tipinde iki ayrı connector oluşturun.
3. RAW linklerini ekleyin ve `Refresh Rate` değerini `1440` (günlük) dakika olarak belirleyin.

---

## 🛠️ Kendi Altyapınıza Kurmak İsterseniz
1. Depoyu **Fork** edin.
2. **Settings > Actions > General** menüsünden **Workflow permissions** kısmını **"Read and write permissions"** olarak işaretleyip kaydedin.
3. **Actions** sekmesinden `Run workflow` diyerek sistemi manuel tetikleyin; sistem artık her sabah otomatik çalışacaktır.

---

## 📊 Teknik Detaylar
* **Limit Kontrolü:** 1 yıllık filtreleme, cihazlarınızın hafıza limitlerini aşmadan sadece "taze" tehditlere odaklanmanızı sağlar.
* **Güncelleme:** Script her gün `03:00 UTC` (Türkiye saatiyle 06:00) saatinde tetiklenir.
* **Lisans:** [MIT](LICENSE)

---

### 
