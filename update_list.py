import requests
import time
import ipaddress
import sys
from datetime import datetime, timedelta

def is_ip(address):
    try:
        ipaddress.ip_address(address)
        return True
    except ValueError:
        return False

def main():
    base_url = "https://www.usom.gov.tr/api/address/index"
    ips = []
    domains = []
    
    # 1 yıl öncesini hesapla
    one_year_ago = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
    print(f"Baslatiliyor... Filtre: {one_year_ago} sonrasi.")
    
    page = 1
    while True:
        try:
            params = {'page': page, 'per-page': 1000, 'date_gte': one_year_ago}
            response = requests.get(base_url, params=params, timeout=20, verify=True)
            
            if response.status_code == 200:
                data = response.json()
                models = data.get('models', [])
                if not models:
                    break
                    
                for item in models:
                    addr = item.get('url', '').strip()
                    if addr:
                        if is_ip(addr):
                            ips.append(addr)
                        else:
                            domains.append(addr)
                
                print(f"Sayfa {page} tamamlandi. ({len(models)} kayit)")
                if len(models) < 1000:
                    break
                page += 1
                time.sleep(0.5) 
            else:
                print(f"API hatasi: HTTP {response.status_code}")
                sys.exit(1)
        except Exception as e:
            print(f"Hata: {e}")
            sys.exit(1)

    # Dosyaları yaz
    with open("usom_ip.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(sorted(list(set(ips)))))
    with open("usom_domain.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(sorted(list(set(domains)))))
    
    print("Dosyalar basariyla guncellendi.")

if __name__ == "__main__":
    main()
