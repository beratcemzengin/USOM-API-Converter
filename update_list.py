import requests
import time
import urllib3

# SSL uyarılarını gizlemek için
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def main():
    base_url = "https://www.usom.gov.tr/api/address/index"
    all_addresses = []
    
    print("USOM API bağlantısı kuruluyor...")
    
    # 1. ADIM: API'ye bağlanıp toplam sayfa sayısını (pageCount) öğreniyoruz
    try:
        first_req = requests.get(base_url, params={'page': 1}, timeout=15, verify=False)
        if first_req.status_code == 200:
            total_pages = first_req.json().get('pageCount', 500)
            print(f"USOM veritabanında toplam {total_pages} sayfa veri bulundu. Çekim başlıyor...")
        else:
            total_pages = 500 # API sayfa sayısını vermezse varsayılan 500 sayfa (10.000 kayıt) çek
    except Exception as e:
        print(f"Başlangıç bağlantı hatası: {e}")
        total_pages = 500

    # 2. ADIM: Güvenlik için maksimum 2000 sayfa (yaklaşık 40.000 IP/Domain) sınırı koyuyoruz
    # Palo Alto cihazınızın limitlerini (min 50.000) aşmaması için bu güvenlik ağı önemlidir.
    max_limit = min(total_pages, 2000)
    
    # Bütün sayfaları tarayan dinamik döngü
    for page in range(1, max_limit + 1):
        try:
            response = requests.get(base_url, params={'page': page}, timeout=15, verify=False)
            
            if response.status_code == 200:
                data = response.json()
                models = data.get('models', [])
                
                if not models:
                    break # Sayfalar bittiyse döngüden çık
                    
                for item in models:
                    addr = item.get('url') 
                    if addr:
                        all_addresses.append(addr.strip())
                        
                # GitHub loglarını çok doldurmamak için sadece her 50 sayfada bir ekrana yazdırıyoruz
                if page % 50 == 0:
                    print(f"[{page}/{max_limit}] sayfa tarandı. Şu ana kadar toplanan adres: {len(all_addresses)}")
            else:
                break
                
            # USOM WAF (Güvenlik Duvarı) tarafından bot olarak algılanıp engellenmemek için 
            # her sayfa arası çok hafif bir bekleme süresi koyuyoruz
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
        print(f"\n[BAŞARILI] İşlem tamamlandı! Toplam {len(clean_addresses)} benzersiz adres listeye kaydedildi.")
    else:
        print("\n[HATA] Liste doldurulamadı.")

if __name__ == "__main__":
    main()
