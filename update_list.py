import requests
import json

def main():
    # 2026 standartlarına uygun güncel USOM API adresi
    url = "https://www.usom.gov.tr/api/address/index"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Sadece IP ve Domain/URL bilgilerini ayıklıyoruz
        lines = []
        if 'models' in data:
            for item in data['models']:
                if 'url_veya_ip_alani' in item and item['url_veya_ip_alani']:
                    lines.append(item['url_veya_ip_alani'].strip())
        
        # Mükerrer (tekrar eden) kayıtları temizle ve sırala
        clean_lines = sorted(list(set(lines)))
        
        # Palo Alto'nun okuyacağı düz metin dosyasına yaz
        with open("usom_list.txt", "w", encoding="utf-8") as f:
            for line in clean_lines:
                f.write(f"{line}\n")
                
        print(f"Başarılı: {len(clean_lines)} adet adres listelendi.")
        
    except Exception as e:
        print(f"Hata oluştu: {e}")

if __name__ == "__main__":
    main()
