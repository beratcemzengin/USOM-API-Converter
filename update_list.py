import requests
import time
import urllib3
import re
import subprocess
from datetime import datetime, timedelta

# SSL uyarılarını gizle
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# IP kontrolü
def is_ip(address):
    return bool(re.match(r'^(?:\d{1,3}\.){3}\d{1,3}$|^([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$', address))

def main():
    base_url = "https://www.usom.gov.tr/api/address/index"
    ips = []
    domains = []
    
    # 1 yıl öncesini hesapla
    one_year_ago = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
    print(f"Başlatılıyor... Filtre: {one_year_ago} sonrası.")
    
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
                    addr = item.get('url', '').strip()
                    if addr:
                        if is_ip(addr): ips.append(addr)
                        else: domains.append(addr)
                
                print(f"Sayfa {page} tamamlandı. ({len(models)} kayıt)")
                if len(models) < 1000: break
                page += 1
                time.sleep(0.5) 
            else:
                break
        except Exception as e:
            print(f"Hata: {e}")
            break

    # Dosyaları yaz
    with open("usom_ip.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(sorted(list(set(ips)))))
    with open("usom_domain.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(sorted(list(set(domains)))))
    
    print("Dosyalar oluşturuldu, GitHub'a gönderiliyor...")

    # GİT OTOMASYONU (Dosyaları depoya kaydeder)
    try:
        subprocess.run(["git", "config", "--global", "user.name", "GitHub Action"], check=True)
        subprocess.run(["git", "config", "--global", "user.email", "action@github.com"], check=True)
        subprocess.run(["git", "add", "usom_ip.txt", "usom_domain.txt"], check=True)
        # Sadece değişiklik varsa commit at
        result = subprocess.run(["git", "diff", "--staged", "--quiet"], capture_output=True)
        if result.returncode != 0:
            subprocess.run(["git", "commit", "-m", "Otomatik guncel liste - $(date)"], check=True)
            subprocess.run(["git", "push"], check=True)
            print("Push başarılı.")
        else:
            print("Değişiklik yok, push atılmadı.")
    except Exception as e:
        print(f"Git hatası: {e}")

if __name__ == "__main__":
    main()
