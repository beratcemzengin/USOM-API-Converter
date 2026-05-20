import requests
import time
import urllib3
from datetime import datetime, timedelta

# SSL uyarılarını gizlemek için
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def main():
    base_url = "https://www.usom.gov.tr/api/address/index"
    all_addresses = []
    
    # 1 yıl öncesini hesapla
    one_year_ago = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
    
    print(f"USOM API bağlantısı kuruluyor...")
    print(f"FİLTRE AKTİF: Sadece {one_year_ago} tarihinden sonra eklenen GÜNCEL tehditler çekilecek.")
    
    try:
        params = {'page': 1, 'date_gte': one_year_ago}
        first_req = requests.get(base_url, params=params, timeout=15, verify=False)
        if first_req.status_code == 200:
            total_pages = first_req.json().get('pageCount', 100)
            print(f"USOM veritabanında son 1 yıla ait toplam {total_pages} sayfa veri bulundu. Çekim başlıyor...")
        else:
            total_pages = 100 
    except Exception as e:
        total_pages = 100

    # Palo Alto limitlerine yaklaşmak için sayfa limitini biraz daha esnetiyoruz
    max_limit = min(total_pages, 4000)
    
    page = 1
    retry_count = 0
    
    # Tüm sayfaları taramak için while döngüsü (Hata alınca aynı sayfadan devam edebilmek için)
    while page <= max_limit:
        try:
            params = {'page': page, 'date_gte': one_year_ago}
            response = requests.get(base_url, params=params, timeout=15, verify=False)
            
            if response.status_code == 200:
                data = response.json()
                models = data.get('models', [])
                
                if not models:
                    break 
                    
                for item in models:
                    addr = item.get('url') 
                    if addr:
                        all_addresses.append(addr.strip())
                        
                if page % 50 == 0:
                    print(f"[{page}/{max_limit}] sayfa tarandı. Şu ana kadar toplanan adres: {len(all_addresses)}")
                
                # Başarılı olunca bir sonraki sayfaya geç, hata sayacını sıfırla
                page += 1
                retry_count = 0 
                # WAF'ı kızdırmamak için bekleme süresini 1 saniyeye çıkardık
                time.sleep(1.0) 
                
            # İŞTE KRİTİK NOKTA: WAF Bizi Engellerse (429 Hatası)
            elif response.status_code == 429:
                retry_count += 1
                if retry_count > 3:
                    print("Üst üste 3 kez 429 hatası alındı. Güvenlik için işlem sonlandırılıyor.")
                    break
                
                print(f"[UYARI] USOM WAF Engeli (HTTP 429) - {retry_count}. kez denenecek. 30 saniye dinleniliyor...")
                time.sleep(30) # 30 saniye bekle ve sayfa sayısını (page) artırmadan döngüyü tekrarla
                
            else:
                print(f"Sayfa {page} alınamadı. HTTP Status: {response.status_code}")
                break
                
        except Exception as e:
            print(f"{page}. sayfa işlenirken hata oluştu: {e}")
            break

    # Mükerrer kayıtları temizle
    clean_addresses = sorted(list(set(all_addresses)))
    
    if clean_addresses:
        with open("usom_list.txt", "w", encoding="utf-8") as f:
            for address in clean_addresses:
                f.write(f"{address}\n")
        print(f"\n[BAŞARILI] İşlem tamamlandı! Toplam {len(clean_addresses)} güncel ve benzersiz adres listeye kaydedildi.")
    else:
        print("\n[HATA] Liste doldurulamadı.")

if __name__ == "__main__":
    main()
