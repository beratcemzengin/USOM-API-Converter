# USOM API to Palo Alto Networks EDL Converter 🛡️🚀

[![USOM API to Palo Alto EDL Converter](https://github.com/KULLANICI_ADINIZ/REPO_ADINIZ/actions/workflows/usom_job.yml/badge.svg)](https://github.com/KULLANICI_ADINIZ/REPO_ADINIZ/actions/workflows/usom_job.yml)

Siber Güvenlik Başkanlığı'nın 177 sayılı Cumhurbaşkanlığı Kararnamesi ve 7545 sayılı Siber Güvenlik Kanunu uyarınca yaptığı duyuru doğrultusunda, **1 Haziran 2026** tarihi itibariyle USOM üzerindeki eski `.txt` formatındaki zararlı bağlantı listesi paylaşımları sona ermektedir. Veri erişim süreçleri tamamen yeni API servisleri (`www.siberguvenlik.gov.tr`) üzerinden yürütülecektir.

Palo Alto Networks firewall cihazları (EDL mimarisi) ham JSON formatındaki API çıktılarını doğrudan işleyemediği için, bu proje **GitHub Actions** kullanarak USOM API'sindeki zararlı adresleri saat başı otomatik olarak çeker, temizler ve Palo Alto'nun anlayabileceği standart düz metin (`.txt`) formatına dönüştürür.

## 🌟 Avantajları
- **Sıfır Altyapı Maliyeti:** Kurum içinde ek bir Linux sunucu, script veya cron job barındırmanıza gerek kalmaz. Süreç tamamen GitHub'ın sunucusuz (serverless) altyapısında döner.
- **7/24 Güncel:** GitHub Actions her saat başı tetiklenerek listenin her zaman güncel kalmasını sağlar.
- **Yüksek Performans:** Palo Alto cihazınız karmaşık JSON ayrıştırma yüküyle uğraşmaz, doğrudan optimize edilmiş hafif bir text dosyasını okur.

---

## 🛠️ Kurulum ve Otomasyonun Devreye Alınması

### 1. Kendi Deponuzu Oluşturun (Fork veya Şablon)
1. Bu depoyu sağ üstteki **Fork** butonuna basarak kendi GitHub hesabınıza kopyalayın.
2. Deponuzun **Settings > Actions > General** menüsüne giderek **Workflow permissions** kısmını **"Read and write permissions"** olarak ayarlayın ve kaydedin (GitHub Actions'ın listeyi güncelleyip kaydedebilmesi için gereklidir).

### 2. GitHub Actions'ı Tetikleyin
- Deponuzun üst menüsündeki **Actions** sekmesine gelin.
- Sol taraftan **"USOM API to Palo Alto EDL Converter"** iş akışını (workflow) seçin.
- **Run workflow** butonuna basarak ilk çalıştırmayı manuel olarak başlatın.
- İşlem tamamlandığında ana dizinde `usom_list.txt` dosyasının oluştuğunu göreceksiniz.

---

## 🔒 Palo Alto Networks Firewall Entegrasyonu

### 1. Raw Linkini Alın
Deponuzda oluşan `usom_list.txt` dosyasına tıklayın ve sağ üstteki **Raw** butonuna basın. Tarayıcınızın adres satırındaki URL'yi kopyalayın. Linkiniz şuna benzeyecektir:
`https://raw.githubusercontent.com/KULLANICI_ADINIZ/REPO_ADINIZ/main/usom_list.txt`

### 2. EDL Nesnesini Tanımlayın
1. Palo Alto Web Arayüzünde **Objects > External Dynamic Lists** yolunu izleyin.
2. **Add** butonuna tıklayın:
   - **Name:** `USOM_Zarli_Baglantilar`
   - **Type:** `URL List` *(USOM verileri tam URL ve Domain içerdiği için URL List seçilmesi önerilir)*
   - **Source:** Yukarıda kopyaladığınız GitHub Raw linkini yapıştırın.
   - **Repeat:** `Hourly` (Saatlik) seçeneğini işaretleyin.
3. **Test Source URL** butonuna basarak erişimi doğrulayın.

### 3. Güvenlik Politikasını Oluşturun
1. **Policies > Security** sekmesine gidin ve yeni bir kural ekleyin.
2. **Source:** `Any` veya iç ağ bölgeleriniz (Trust).
3. **Destination:** **URL Category** kısmına gelin ve oluşturduğunuz `USOM_Zarli_Baglantilar` EDL nesnesini seçin.
4. **Actions:** İsteğe göre `Block`, `Drop` veya `Reset` olarak ayarlayın.
5. Sağ üstteki **Commit** butonuna basarak yapılandırmayı aktif hale getirin.

---

## 📊 Limitler ve Kontroller
Palo Alto Networks cihazlarında donanım modeline göre toplam EDL kapasite limitleri bulunmaktadır (Örn: Giriş seviyesi cihazlar için toplam 50.000 satır). USOM listesi genellikle bu limitlerin oldukça altında kalmaktadır. 

Cihazınızın güncel durumunu ve limitlerini kontrol etmek için Palo Alto CLI ekranından şu komutu çalıştırabilirsiniz:
```bash
show system state | match max-edl
