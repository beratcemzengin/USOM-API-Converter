import requests
from bs4 import BeautifulSoup
import re
import time

def main():
    # USOM'un API yerine doğrudan yayın yaptığı web sayfasını kullanıyoruz
    url = "https://www.usom.gov.tr/zararli-baglantilar"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    all_addresses = []
    
    print("USOM sayfasından zararlı bağlantılar toplanıyor...")
    
    try:
        # Sayfaya istek at
        response = requests.get(url, headers=headers, timeout=15, verify=False)
        response.raise_for_status()
        
        # Sayfa içeriğini BeautifulSoup ile parse et
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Tablodaki tüm satırları bul (USOM tablosundaki class veya tr yapısına göre)
        # Genellikle tablo içindeki <td> etiketlerinde veya belirli bir id'de bulunur
        table = soup.find('table', {'class': 'table'}) 
        
        if table:
            rows = table.find_all('tr')
            for row in rows[1:]: # Başlık satırını atla
                cols = row.find_all('td')
                if len(cols) > 0:
                    # Genellikle ilk veya ikinci sütunda URL bulunur
                    # Sayfa yapısına göre sütun indeksini ayarlayın (burada 1 varsayıyoruz)
                    address = cols[1].text.strip()
                    if address:
                        all_addresses.append(address)
            print(f"Tablodan {len(all_addresses)} adres başarıyla çekildi.")
        else:
             print("Sayfada tablo bulunamadı. Yapı değişmiş olabilir.")
             
    except Exception as e:
        print(f"Sayfa çekilirken hata oluştu: {e}")

    # Çift kayıtları temizle ve sırala
    clean_addresses = sorted(list(set(all_addresses)))
    
    # Eğer listenin içi dolduysa dosyaya yaz
    if clean_addresses:
        with open("usom_list.txt", "w", encoding="utf-8") as f:
            for address in clean_addresses:
                f.write(f"{address}\n")
        print(f"\n[BAŞARILI] Toplam {len(clean_addresses)} benzersiz adres 'usom_list.txt' dosyasına kaydedildi!")
    else:
        print("\n[HATA] API veya Web sayfasından hiçbir adres çekilemedi. Liste hala boş.")
        
        # Güvenlik ağı (Fallback): Eğer hiçbir şekilde veri alınamazsa, boş liste yerine
        # test amaçlı veya bilinen birkaç zararlı adresi listeye ekleyerek 
        # GitHub Actions'ın hata vermesini engelleyebiliriz (İsteğe bağlı).
        # with open("usom_list.txt", "w", encoding="utf-8") as f:
        #    f.write("test-zararli-domain.com\n")
        #    f.write("192.168.1.99\n")

if __name__ == "__main__":
    main()
