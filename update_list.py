import requests
import json
import time

def main():
    # Güncel ve resmi USOM API uç noktası
    base_url = "https://www.usom.gov.tr/api/address/index"
    
    all_addresses = []
    page = 1
    max_pages = 20  # Palo Alto limitlerini zorlamamak adına ilk etapta çekilecek maksimum sayfa adedi
    
    print("USOM API'den veriler çekiliyor, lütfen bekleyin...")
    
    while page <= max_pages:
        try:
            # API'den sayfa sayfa veriyi talep ediyoruz
            params = {'page': page}
            response = requests.get(base_url, params=params, timeout=15)
            
            # Eğer sayfa bulunamadıysa veya hata kodu döndüyse döngüden çık
            if response.status_code != 200:
                print(f"Sayfa {page} alınamadı (Status: {response.status_code}). Döngü sonlandırılıyor.")
                break
                
            data = response.json()
            
            # USOM Şemasına göre 'models' listesini kontrol et
            if 'models' in data and data['models']:
                page_items = data['models']
                current_page_count = 0
                
                for item in page_items:
                    # Resmi şemadaki alan adı: 'address'
                    if 'address' in item and item['address']:
                        addr = item['address'].strip()
                        if addr:
                            all_addresses.append(addr)
                            current_page_count += 1
                
                print(f"Sayfa {page} başarıyla işlendi. {current_page_count} adres eklendi.")
                
                # Eğer gelen sayfadaki eleman sayısı çok azsa, muhtemelen son sayfaya gelinmiştir
                if len(page_items) < 10:
                    print("Son sayfaya ulaşıldı.")
                    break
            else:
                # Veri boş geldiyse döngüyü bitir
                print(f"Sayfa {page} boş veya 'models' alanı içermiyor. İşlem tamamlandı.")
                break
                
            page += 1
            time.sleep(0.5) # USOM sunucularını yormamak ve banlanmamak için kısa bir bekleme
            
        except Exception as e:
            print(f"Sayfa {page} işlenirken hata oluştu: {e}")
            break

    # Mükerrer (tekrar eden) kayıtları temizle ve sırala
    clean_addresses = sorted(list(set(all_addresses)))
    
    # Palo Alto'nun okuyacağı düz metin dosyasına yaz
    with open("usom_list.txt", "w", encoding="utf-8") as f:
        for address in clean_addresses:
            f.write(f"{address}\n")
            
    print(f"\nİşlem Tamamlandı! Toplam {len(clean_addresses)} benzersiz adres 'usom_list.txt' dosyasına yazıldı.")

if __name__ == "__main__":
    main()
