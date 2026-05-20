import requests
import json
import time

def main():
    # Güncel USOM API adresi
    base_url = "https://www.usom.gov.tr/api/address/index"
    
    all_addresses = []
    page = 1
    max_pages = 5 # İlk etapta test için 5 sayfa çekiyoruz (Her sayfada 100 kayıt olacak)
    
    print("USOM API bağlantısı kuruluyor...")
    
    while page <= max_pages:
        try:
            # page-size parametresini 100 olarak zorunlu ekliyoruz
            # verify=False ile olası SSL sertifika hatalarını bypass ediyoruz
            params = {
                'page': page,
                'page-size': 100
            }
            
            response = requests.get(base_url, params=params, timeout=20, verify=False)
            
            if response.status_code != 200:
                print(f"Sayfa {page} alınamadı. Durum Kodu: {response.status_code}")
                break
                
            data = response.json()
            
            # API'den gelen 'models' listesini kontrol et
            if 'models' in data and data['models']:
                page_items = data['models']
                current_page_count = 0
                
                for item in page_items:
                    if 'address' in item and item['address']:
                        addr = item['address'].strip()
                        if addr:
                            all_addresses.append(addr)
                            current_page_count += 1
                
                print(f"Sayfa {page} başarıyla okundu. {current_page_count} adet adres alındı.")
                
                # Eğer sayfadan gelen veri 100'den azsa son sayfaya gelinmiştir
                if len(page_items) < 100:
                    print("Veritabanındaki son sayfaya ulaşıldı.")
                    break
            else:
                print(f"Sayfa {page} içeriği boş geldi.")
                break
                
            page += 1
            time.sleep(1) # Banlanmamak için güvenli bekleme süresi
            
        except Exception as e:
            print(f"Sayfa {page} çekilirken teknik bir hata oluştu: {e}")
            break

    # Çift kayıtları temizle ve sırala
    clean_addresses = sorted(list(set(all_addresses)))
    
    # Eğer listenin içi dolduysa dosyaya yaz
    if clean_addresses:
        with open("usom_list.txt", "w", encoding="utf-8") as f:
            for address in clean_addresses:
                f.write(f"{address}\n")
        print(f"\n[BAŞARILI] Toplam {len(clean_addresses)} benzersiz adres 'usom_list.txt' dosyasına kaydedildi!")
    else:
        print("\n[HATA] API'den hiçbir adres çekilemedi, liste hala boş.")

if __name__ == "__main__":
    main()
