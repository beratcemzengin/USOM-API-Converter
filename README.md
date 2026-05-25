# USOM-API-Converter (Firewall Tehdit İstihbaratı Otomasyonu) 🛡️🚀

[![USOM-API-Converter](https://github.com/beratcemzengin/USOM-API-Converter/actions/workflows/main.yml/badge.svg)](https://github.com/beratcemzengin/USOM-API-Converter/actions/workflows/main.yml)

> 💡 **Hızlı Kullanım (Hazır Listeler):**
> Kendi GitHub altyapınızı kurmakla uğraşmak istemiyorsanız, bu deponun her gün otomatik ürettiği güncel listeleri doğrudan Firewall cihazlarınıza tanımlayabilirsiniz:
> 
> - 🔗 **IP Listesi:** `https://raw.githubusercontent.com/beratcemzengin/USOM-API-Converter/main/usom_ip.txt`
> - 🔗 **Domain Listesi:** `https://raw.githubusercontent.com/beratcemzengin/USOM-API-Converter/main/usom_domain.txt`

---

Bilgi Teknolojileri ve İletişim Kurumu (BTK) bünyesindeki Ulusal Siber Olaylara Müdahale Merkezi (USOM) API servisleri üzerinden sunduğu tehdit beslemesini; kurumsal güvenlik duvarlarının (Palo Alto, FortiGate, Cisco vb.) doğrudan tüketebileceği optimize edilmiş formatta sunan otomasyon projesidir.

## 🌟 Neler Yeni?
* **Segmentasyon:** Tehditler artık IP (L3/L4) ve Domain (L7) olarak iki ayrı dosyada sunulur.
* **Yüksek Hız:** `per-page=1000` parametresi ile tüm veritabanı saniyeler içinde taranır.
* **Akıllı Filtreleme:** Cihazlarınızı yormamak için sadece **son 1 yılın** aktif tehditleri baz alınır.
* **Tam Otomasyon:** GitHub Actions üzerinde serverless altyapıda, her gün otomatik güncellenir.

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

### 1. Depoyu Fork Edin
1. Deponun sağ üst köşesindeki **"Fork"** butonuna tıklayın.
2. **"Create fork"** butonuna basarak projeyi kendi profilinize kopyalayın. Artık `KullanıcıAdınız/USOM-API-Converter` adresinde projenin kendi kopyanız üzerinde tam yetkilisiniz.


### 2. GitHub Actions İzinlerini Yapılandırın
Deponun güncel dosyaları kaydedebilmesi (push atabilmesi) için yazma izni vermeniz gerekir:
1. Deponuzda **Settings > Actions > General** sekmesine gidin.
2. En aşağıya inin, **Workflow permissions** kısmında **"Read and write permissions"** seçeneğini işaretleyip **Save** deyin.

### 3. Otomasyonu Başlatın
1. Deponuzun üst menüsündeki **Actions** sekmesine tıklayın.
2. İş akışını seçip **"Run workflow"** butonuna basarak manuel tetikleyin.
3. İşlem bittiğinde `usom_ip.txt` ve `usom_domain.txt` dosyalarının deponuzda oluştuğunu göreceksiniz. Artık sistem her gün otomatik olarak çalışacaktır.

---

## 📊 Teknik Detaylar
* **Limit Kontrolü:** 1 yıllık filtreleme, cihazlarınızın hafıza limitlerini (RAM/TCAM) aşmadan sadece "taze" tehditlere odaklanmanızı sağlar.
* **Güncelleme:** Script her gün Türkiye saatiyle 06:00'da tetiklenir.

