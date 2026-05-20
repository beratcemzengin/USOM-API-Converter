import requests
import time
import urllib3
import re
from datetime import datetime, timedelta

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# IP adresi olup olmadığını anlayan basit bir regex
def is_ip(address):
    # IPv4 veya IPv6 kontrolü
    return bool(re.match(r'^(?:\d{1,3}\.){3}\d{1,3}$|^([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$', address))

def main():
    base_url = "https://www.usom.gov.tr/api/address/index"
    ips = []
    domains = []
    
    one_year_ago = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
    
    print("Veriler çekiliyor ve ayrıştırılıyor... 🚀")
    
    page = 1
    while True:
        try:
            params = {'page': page, 'per-page': 1000, 'date_gte': one_year_ago}
            response = requests.get(base_url, params=params, timeout=20, verify=False)
            
            if response.status_code == 200:
                data = response.json()
                models = data.get('models', [])
                
                if not models: break
                    
                for item in models:
                    addr = item.get('url')
                    if addr:
                        addr = addr.strip()
                        # IP mi Domain mi?
                        if is_ip(addr):
                            ips.append(addr)
                        else:
                            domains.append(addr)
                
                print(f"Sayfa {page} işlendi. Toplam: {len(ips)} IP, {len(domains)} Domain.")
                if len(models) < 1000: break
                page += 1
                time.sleep(1.0)
            else:
                break
        except Exception as e:
            print(f"Hata: {e}")
            break

    # Dosyalara yaz
    with open("usom_ip.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(sorted(list(set(ips)))))
        
    with open("usom_domain.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(sorted(list(set(domains)))))
        
    print(f"\n[BAŞARILI] usom_ip.txt ve usom_domain.txt oluşturuldu.")

if __name__ == "__main__":
    main()
