import requests
import time
import ipaddress
import sys
from datetime import datetime, timedelta
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def is_ip(address):
    try:
        ipaddress.ip_address(address)
        return True
    except ValueError:
        return False


def create_session():
    """Retry mekanizmali bir requests session olusturur."""
    session = requests.Session()
    retry_strategy = Retry(
        total=5,
        backoff_factor=2,  # 2, 4, 8, 16, 32 saniye bekler
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
    })
    return session


def fetch_page(session, base_url, params, attempt=1, max_attempts=3):
    """Tek bir sayfayi cekmek icin retry mekanizmali fonksiyon."""
    try:
        response = session.get(base_url, params=params, timeout=30, verify=True)

        if response.status_code != 200:
            print(f"  API hatasi: HTTP {response.status_code}")
            if attempt < max_attempts:
                wait_time = 5 * attempt
                print(f"  {wait_time} saniye sonra tekrar denenecek... (Deneme {attempt}/{max_attempts})")
                time.sleep(wait_time)
                return fetch_page(session, base_url, params, attempt + 1, max_attempts)
            return None

        # Yanit body kontrolu
        body = response.text.strip()
        if not body:
            print(f"  Uyari: API bos yanit dondu.")
            if attempt < max_attempts:
                wait_time = 5 * attempt
                print(f"  {wait_time} saniye sonra tekrar denenecek... (Deneme {attempt}/{max_attempts})")
                time.sleep(wait_time)
                return fetch_page(session, base_url, params, attempt + 1, max_attempts)
            return None

        # JSON parse
        try:
            data = response.json()
        except ValueError:
            print(f"  Uyari: Yanit JSON formatinda degil. Ilk 300 karakter:")
            print(f"  {body[:300]}")
            if attempt < max_attempts:
                wait_time = 10 * attempt
                print(f"  {wait_time} saniye sonra tekrar denenecek... (Deneme {attempt}/{max_attempts})")
                time.sleep(wait_time)
                return fetch_page(session, base_url, params, attempt + 1, max_attempts)
            return None

        return data

    except requests.exceptions.Timeout:
        print(f"  Zaman asimi hatasi.")
        if attempt < max_attempts:
            wait_time = 10 * attempt
            print(f"  {wait_time} saniye sonra tekrar denenecek... (Deneme {attempt}/{max_attempts})")
            time.sleep(wait_time)
            return fetch_page(session, base_url, params, attempt + 1, max_attempts)
        return None

    except requests.exceptions.ConnectionError as e:
        print(f"  Baglanti hatasi: {e}")
        if attempt < max_attempts:
            wait_time = 15 * attempt
            print(f"  {wait_time} saniye sonra tekrar denenecek... (Deneme {attempt}/{max_attempts})")
            time.sleep(wait_time)
            return fetch_page(session, base_url, params, attempt + 1, max_attempts)
        return None

    except requests.exceptions.RequestException as e:
        print(f"  Istek hatasi: {e}")
        if attempt < max_attempts:
            wait_time = 10 * attempt
            print(f"  {wait_time} saniye sonra tekrar denenecek... (Deneme {attempt}/{max_attempts})")
            time.sleep(wait_time)
            return fetch_page(session, base_url, params, attempt + 1, max_attempts)
        return None


def main():
    base_url = "https://siberguvenlik.gov.tr/api/address/index"
    ips = []
    domains = []
    consecutive_failures = 0
    max_consecutive_failures = 3

    # 1 yil oncesini hesapla
    one_year_ago = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
    print(f"Baslatiliyor... Filtre: {one_year_ago} sonrasi.")

    session = create_session()

    # Baglanti testi
    print("API baglanti testi yapiliyor...")
    test_data = fetch_page(session, base_url, {'page': 1, 'per-page': 1})
    if test_data is None:
        print("HATA: API'ye baglanilamadi. Islem iptal ediliyor.")
        sys.exit(1)

    total_count = test_data.get('totalCount', 'Bilinmiyor')
    print(f"API baglantisi basarili. Toplam kayit: {total_count}")

    page = 1
    while True:
        params = {'page': page, 'per-page': 1000, 'date_gte': one_year_ago}
        data = fetch_page(session, base_url, params)

        if data is None:
            consecutive_failures += 1
            print(f"Sayfa {page} alinamadi. (Ardisik basarisizlik: {consecutive_failures}/{max_consecutive_failures})")
            if consecutive_failures >= max_consecutive_failures:
                print(f"HATA: {max_consecutive_failures} ardisik sayfa basarisiz oldu. Islem durduruluyor.")
                # Eger daha onceden veri toplanabildiyse, mevcut veriyi yaz
                if ips or domains:
                    print(f"Uyari: Kismi veri yaziliyor. ({len(ips)} IP, {len(domains)} domain)")
                    break
                else:
                    sys.exit(1)
            # Basarisiz sayfayi atla ve sonrakine gec
            page += 1
            time.sleep(5)
            continue

        consecutive_failures = 0  # Basarili istek, sayaci sifirla

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
        time.sleep(1)  # API'yi yormamak icin 1 saniye bekle

    # Sonuclari kontrol et
    unique_ips = sorted(set(ips))
    unique_domains = sorted(set(domains))

    if not unique_ips and not unique_domains:
        print("HATA: Hicbir kayit alinamadi. Dosyalar guncellenmedi.")
        sys.exit(1)

    # Dosyalari yaz
    with open("usom_ip.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(unique_ips))
    with open("usom_domain.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(unique_domains))

    print(f"\nTamamlandi!")
    print(f"  Benzersiz IP adresi : {len(unique_ips)}")
    print(f"  Benzersiz domain    : {len(unique_domains)}")
    print("Dosyalar basariyla guncellendi.")


if __name__ == "__main__":
    main()

