import requests
import time
import urllib3
from datetime import datetime, timedelta

# SSL uyarılarını gizlemek için
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def main():
    base_url = "https://www.usom.gov.tr/api/address/index"
    all_addresses = []
    
    # Bugünün tarihinden 365 gün (1 yıl) öncesini hesapla ve YYYY-MM-DD formatına çevir
    one_year_ago = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
    
    print(f"USOM API bağlantısı kuruluyor...")
    print(f"FİLTRE AKTİF: Sadece {one_year_ago} tarihinden sonra eklenen GÜNCEL tehditler çekilecek.")
    
    # 1. ADIM: API'ye bağlanıp filtrelenmiş verinin toplam sayfa sayısını öğreniyoruz
    try:
        params = {
            'page': 1,
            'date_gte': one_year_ago # Tarih filtresini API'ye iletiyoruz
        }
        first_req = requests.get(base_url, params=params, timeout=15, verify=False)
        if first_req.status_code == 200:
            total_pages = first_req.json().get('pageCount', 100)
            print(f"USOM veritabanında son 1 yıla ait toplam {total_pages} sayfa veri bulundu. Çekim başlıyor...")
        else:
            total_pages = 100 
    except Exception as e:
        print(f"Başlangıç bağlantı hatası: {e}")
        total_pages = 100

    # 2. ADIM: Maksimum 2000 sayfa (yaklaşık 40.000 IP/Domain) güvenlik sınırı
    max_limit = min(total_pages, 2000)
    
    # Bütün sayfaları tarayan dinamik döngü
    for page in range(1, max_limit + 1):
        try:
            params = {
                'page': page,
                'date_gte': one_year_ago # Her sayfa isteğinde filtreyi tekrar gönderiyoruz
            }
            response = requests.get(base_url, params=params, timeout=15, verify=False)
            
            if response.status_code == 200:
                data = response.json()
                models = data.get('models', [])
                
                if not models:
                    break # Sayfalar bittiyse döngüden çık
                    
                for item in models:
                    addr = item.get('url') 
                    if addr:
                        all_addresses.append(addr.strip())
                        
                # Logların daha temiz görünmesi için her 10 sayfada bir ekrana bilgi yazdırıyoruz
                if page % 10 == 0:
                    print(f"[{page}/{max_limit}] sayfa tarandı. Şu ana kadar toplanan güncel adres: {len(all_addresses)}")
            else:
                print(f"Sayfa {page} alınamadı. HTTP Status: {response.status_code}")
                break
                
            # USOM WAF tarafından engellenmemek için çok kısa bir bekleme
            time.sleep(0.3)
            
        except Exception as e:
            print(f"{page}. sayfa işlenirken kesinti yaşandı: {e}")
            break

    # 3. ADIM: Mükerrer kayıtları temizle ve txt dosyasına yaz
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
