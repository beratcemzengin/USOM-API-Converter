import requests
import time
import urllib3
from datetime import datetime, timedelta

# SSL uyarılarını gizlemek için
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def main():
    base_url = "https://www.usom.gov.tr/api/address/index"
    all_addresses = []
    
    # Bugünün tarihinden 365 gün (1 yıl) öncesini hesapla
    one_year_ago = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
    
    print("USOM API bağlantısı kuruluyor... 🚀")
    print(f"FİLTRE AKTİF: {one_year_ago} tarihinden sonraki tehditler çekilecek.")
    print("OPTİMİZASYON: 'per-page=1000' kullanılarak yüksek hızda veri toplanacak.")
    
    page = 1
    retry_count = 0
    
    # Sayfa sayısını önceden sormamıza gerek kalmadı, 1000'er 1000'er çekeceğimiz için 
    # gelen veri 1000'in altına düştüğünde son sayfada olduğumuzu anlayacağız.
    while True:
        try:
            # İşte sihirli parametrelerin birleşimi
            params = {
                'page': page,
                'per-page': 1000, 
                'date_gte': one_year_ago
            }
            
            response = requests.get(base_url, params=params, timeout=20, verify=False)
            
            if response.status_code == 200:
                data = response.json()
                models = data.get('models', [])
                
                if not models:
                    print("Veritabanının sonuna ulaşıldı.")
                    break 
                    
                for item in models:
                    addr = item.get('url') 
                    if addr:
                        all_addresses.append(addr.strip())
                        
                print(f"Sayfa {page} başarıyla çekildi ({len(models)} kayıt). Toplam toplanan: {len(all_addresses)}")
                
                # Eğer dönen kayıt sayısı 1000'den azsa, USOM'daki son sayfaya gelmişiz demektir!
                if len(models) < 1000:
                    print("Tüm güncel veriler başarıyla alındı.")
                    break
                
                # Başarılı olunca bir sonraki sayfaya geç
                page += 1
                retry_count = 0 
                # WAF'ı hiç uyandırmamak için saniyede sadece 1 istek (1 rps) atıyoruz
                time.sleep(1.0) 
                
            # WAF Bizi Engellerse (Artık çok düşük bir ihtimal ama güvenlik ağı olarak kalmalı)
            elif response.status_code == 429:
                retry_count += 1
                if retry_count > 3:
                    print("Üst üste 3 kez 429 hatası alındı. Güvenlik için işlem sonlandırılıyor.")
                    break
                
                print(f"[UYARI] USOM WAF Engeli (HTTP 429) - 15 saniye dinleniliyor...")
                time.sleep(15) 
                
            else:
                print(f"Sayfa {page} alınamadı. HTTP Status: {response.status_code}")
                break
                
        except Exception as e:
            print(f"{page}. sayfa işlenirken hata oluştu: {e}")
            break

    # Mükerrer kayıtları temizle ve Palo Alto'nun sevdiği gibi alfabetik sırala
    clean_addresses = sorted(list(set(all_addresses)))
    
    if clean_addresses:
        with open("usom_list.txt", "w", encoding="utf-8") as f:
            for address in clean_addresses:
                f.write(f"{address}\n")
        print(f"\n[BAŞARILI] İşlem 1 dakikadan kısa sürede bitti! Toplam {len(clean_addresses)} güncel adres kaydedildi.")
    else:
        print("\n[HATA] Liste doldurulamadı.")

if __name__ == "__main__":
    main()
