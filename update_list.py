import requests
import time
import urllib3

# SSL uyarılarını gizlemek için
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def main():
    base_url = "https://www.usom.gov.tr/api/address/index"
    all_addresses = []
    
    print("USOM API'den veriler çekiliyor, lütfen bekleyin...")
    
    # İlk 15 sayfayı çekiyoruz (İsterseniz bu sayıyı artırabilirsiniz)
    for page in range(1, 16):
        try:
            params = {'page': page}
            # verify=False ile SSL takılmalarını önlüyoruz
            response = requests.get(base_url, params=params, timeout=15, verify=False)
            
            if response.status_code == 200:
                data = response.json()
                models = data.get('models', [])
                
                if not models:
                    print(f"Sayfa {page} boş veya son sayfaya gelindi.")
                    break
                    
                added_count = 0
                for item in models:
                    # DOKÜMANA GÖRE DOĞRU ANAHTAR KELİME: 'url'
                    addr = item.get('url') 
                    
                    if addr:
                        all_addresses.append(addr.strip())
                        added_count += 1
                        
                print(f"Sayfa {page} başarıyla okundu. {added_count} adres alındı.")
            else:
                print(f"Sayfa {page} alınamadı. HTTP Status: {response.status_code}")
                break
                
            # USOM sunucusunu yormamak için kısa bir bekleme
            time.sleep(0.5)
            
        except Exception as e:
            print(f"Sayfa {page} işlenirken hata oluştu: {e}")
            break

    # Mükerrer (tekrar eden) kayıtları temizle ve sırala
    clean_addresses = sorted(list(set(all_addresses)))
    
    # Dosyaya yaz
    if clean_addresses:
        with open("usom_list.txt", "w", encoding="utf-8") as f:
            for address in clean_addresses:
                f.write(f"{address}\n")
        print(f"\n[BAŞARILI] Toplam {len(clean_addresses)} benzersiz adres 'usom_list.txt' dosyasına kaydedildi!")
    else:
        print("\n[HATA] Liste boş kaldı, adres bulunamadı.")

if __name__ == "__main__":
    main()
