# USOM-API-Converter (Firewall Tehdit İstihbaratı Otomasyonu) 🛡️🚀

[![USOM-API-Converter](https://github.com/KULLANICI_ADINIZ/REPO_ADINIZ/actions/workflows/usom_job.yml/badge.svg)](https://github.com/KULLANICI_ADINIZ/REPO_ADINIZ/actions/workflows/usom_job.yml)

Siber Güvenlik Başkanlığı'nın 177 sayılı Cumhurbaşkanlığı Kararnamesi ve 7545 sayılı Siber Güvenlik Kanunu uyarınca yaptığı duyuru doğrultusunda, **1 Haziran 2026** tarihi itibariyle USOM üzerindeki eski `.txt` formatındaki zararlı bağlantı listesi paylaşımları sona ermektedir. Veri erişim süreçleri tamamen yeni API servisleri (`www.siberguvenlik.gov.tr`) üzerinden yürütülecektir.

Piyasada yaygın olarak kullanılan **Fortinet (FortiGate), Palo Alto Networks, Cisco ve Check Point** gibi kurumsal güvenlik duvarları (Firewall), ham JSON formatındaki API çıktılarını External Dynamic List (Harici Dinamik Liste) olarak doğrudan işleyememektedir. Bu proje, **GitHub Actions** kullanarak USOM API'sindeki zararlı adresleri her gün otomatik olarak çeker, ayrıştırır ve tüm güvenlik duvarlarının kolayca okuyabileceği standart düz metin (`.txt`) formatına dönüştürür.

## 🌟 Avantajları
- **Sıfır Altyapı Maliyeti:** Kurum içinde ek bir Linux sunucu, script veya cron job barındırmanıza gerek kalmaz. Süreç tamamen GitHub'ın sunucusuz (serverless) altyapısında döner.
- **Otomatik Güncelleme:** GitHub Actions belirlediğiniz periyotlarda (örn. günde bir kez) tetiklenerek listenin her zaman güncel kalmasını sağlar.
- **Evrensel Uyumluluk:** Üretilen `.txt` dosyası; FortiGate (Fabric Connectors), Palo Alto (EDL), Cisco (Security Intelligence) ve open-source (pfSense/OPNsense) sistemlerle %100 uyumludur.
- **Yüksek Performans:** Güvenlik cihazlarınız karmaşık JSON ayrıştırma yüküyle uğraşmaz, doğrudan optimize edilmiş hafif bir text dosyasını okur.

---

## 🛠️ Kurulum ve Otomasyonun Devreye Alınması

### 1. Kendi Deponuzu Oluşturun (Fork veya Şablon)
1. Bu depoyu sağ üstteki **Fork** butonuna basarak kendi GitHub hesabınıza kopyalayın.
2. Deponuzun **Settings > Actions > General** menüsüne giderek **Workflow permissions** kısmını **"Read and write permissions"** olarak ayarlayın ve kaydedin (GitHub Actions'ın listeyi güncelleyip kaydedebilmesi için gereklidir).

### 2. GitHub Actions'ı Tetikleyin
- Deponuzun üst menüsündeki **Actions** sekmesine gelin.
- Sol taraftan **"USOM API to Palo Alto EDL Converter"** (veya yml dosyasındaki adıyla) iş akışını seçin.
- **Run workflow** butonuna basarak ilk çalıştırmayı manuel olarak başlatın.
- İşlem tamamlandığında ana dizinde `usom_list.txt` dosyasının oluştuğunu göreceksiniz.

---

## 🔗 Firewall Entegrasyon Rehberi

### Ortak Adım: Raw Linkini Alın
Deponuzda oluşan `usom_list.txt` dosyasına tıklayın ve sağ üstteki **Raw** butonuna basın. Tarayıcınızın adres satırındaki URL'yi kopyalayın. Linkiniz şuna benzeyecektir:
`https://raw.githubusercontent.com/KULLANICI_ADINIZ/REPO_ADINIZ/main/usom_list.txt`

### 🛡️ Fortinet (FortiGate) Entegrasyonu
1. FortiGate arayüzünde **Security Fabric > Fabric Connectors** (veya External Connectors) menüsüne gidin.
2. **Create New** diyerek **Threat Feeds** altından **Domain Name** veya **IP Address** seçeneğini tıklayın.
3. **Name:** `USOM_Zararli_Liste`
4. **URL of external resource:** Kopyaladığınız Raw linkini yapıştırın.
5. **Refresh Rate:** 60 veya 1440 (Günlük) dakika olarak belirleyin ve kaydedin.
6. **Policy & Objects > DNS Filter** (veya Web Filter) profillerinde bu listeyi `Block` olarak ayarlayın.

### 🛡️ Palo Alto Networks Entegrasyonu
1. Palo Alto Web Arayüzünde **Objects > External Dynamic Lists** yolunu izleyin ve **Add** deyin.
2. **Name:** `USOM_Zarli_Baglantilar`
3. **Type:** `URL List` veya `Domain List` seçin.
4. **Source:** Kopyaladığınız Raw linkini yapıştırın.
5. **Repeat:** `Hourly` veya `Daily` olarak ayarlayıp kaydedin.
6. **Policies > Security** kuralınızda `Destination` olarak bu listeyi seçip `Drop/Block` aksiyonu verin.

### 🛡️ Cisco (Firepower / FMC) Entegrasyonu
1. FMC arayüzünde **Objects > Object Management** menüsüne gidin.
2. **Security Intelligence > Network Lists and Feeds** sekmesini açıp **Add Network Feed** deyin.
3. Kopyaladığınız listeyi URL üzerinden beslenecek şekilde tanımlayın.
4. Access Control Policy (ACP) içindeki **Security Intelligence** tabında bu listeyi Block listesine sürükleyip bırakın.

---

## 📊 Limitler ve Kontroller
Her üreticinin donanım modeline göre (RAM ve CPU kapasitesi) dışarıdan alabileceği maksimum satır sayısı farklıdır:
- **Palo Alto:** Giriş seviyesi modellerde toplam ~50.000 satır limiti vardır (`show system state | match max-edl` komutuyla kontrol edilebilir).
- **FortiGate:** Cihaz modeline göre (Örn: 60F, 100F, 200F) External Block List (EBL) limitleri 100.000 ila milyonlarca kayıt arasında değişir. Cihaz limitlerinizi aşmamaya özen gösterin.

## ⚖️ Lisans
Bu proje [MIT Lisansı](LICENSE) altında açık kaynak olarak sunulmuştur. Ticari veya bireysel olarak serbestçe değiştirilebilir ve kullanılabilir.
