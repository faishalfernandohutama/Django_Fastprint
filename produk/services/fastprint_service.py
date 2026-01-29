import requests
import hashlib
from datetime import datetime
import pytz

def fetch_produk():
    url = "https://recruitment.fastprint.co.id/tes/api_tes_programmer"
    
    # --- 1. SETUP CREDENTIALS (SAMA SEPERTI SEBELUMNYA) ---
    tz = pytz.timezone('Asia/Jakarta')
    now = datetime.now(tz)

    username_str = f"tesprogrammer{now.strftime('%d%m%y')}C{now.strftime('%H')}"
    
    # Generate Password
    raw_password = f"bisacoding-{now.strftime('%d-%m-%y')}"
    password_md5 = hashlib.md5(raw_password.encode()).hexdigest()

    print(f"[*] Credentials -> User: {username_str} | Pass: {raw_password}")

    # --- 2. SETUP SESSION & HEADERS ---
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://recruitment.fastprint.co.id",
        "Referer": "https://recruitment.fastprint.co.id/tes/api_tes_programmer",
    }

    session = requests.Session()

    # --- 3. EKSEKUSI (REVISI DISINI) ---
    try:
        # payload login
        payload = {
            "username": username_str,
            "password": password_md5
        }

        # Requests Session otomatis menangani cookies jika server memberikannya di respon ini
        response = session.post(url, headers=headers, data=payload)
        
        print(f"[*] Status Code: {response.status_code}")

        # Cek jika status bukan 200
        if response.status_code != 200:
            print("❌ Gagal Login. Response Server:")
            print(response.text)
            return None

        # Cek JSON
        try:
            data = response.json()
            
            # Cek Error dari API (misal username salah)
            if isinstance(data, dict) and (data.get('error') or data.get('status') == 'error'):
                print(f"❌ API Error: {data}")
                return None
            
            return data

        except ValueError:
            print("❌ Gagal decode JSON. Kemungkinan response berupa HTML error.")
            print("Isi Response (100 karakter awal):", response.text[:100])
            return None

    except Exception as e:
        print(f"❌ Error System: {e}")
        return None
    
def sync_and_save_products():
   # --- PANGGIL FETCH PRODUK ---
    data_api = fetch_produk()
    
    if not data_api:
        return False, "Gagal koneksi ke API"

    data_list = data_api if isinstance(data_api, list) else data_api.get('data', [])
    
    if not data_list:
        return False, "Data API Kosong"

    try:
        with transaction.atomic():
            for item in data_list:
                # --- LOGIC ROBUST (Sama persis dengan Command tadi) ---
                
                # 1. ID Produk
                id_prod = item.get('id_produk') or item.get('no_id')
                if not id_prod: continue

                # 2. Kategori
                raw_cat_id = item.get('kategori_id') or item.get('id_kategori')
                nama_cat = item.get('nama_kategori') or item.get('kategori') or "Umum"
                cat_id = int(raw_cat_id) if raw_cat_id else abs(hash(nama_cat)) % 100000

                kategori_obj, _ = Kategori.objects.get_or_create(
                    id_kategori=cat_id, 
                    defaults={'nama_kategori': nama_cat}
                )

                # 3. Status
                raw_stat_id = item.get('status_id') or item.get('id_status')
                nama_stat = item.get('nama_status') or item.get('status') or "Unknown"
                stat_id = int(raw_stat_id) if raw_stat_id else abs(hash(nama_stat)) % 100000

                status_obj, _ = Status.objects.get_or_create(
                    id_status=stat_id,
                    defaults={'nama_status': nama_stat}
                )

                # 4. Harga
                raw_harga = str(item.get('harga', '0'))
                clean_harga_str = ''.join(filter(str.isdigit, raw_harga))
                harga_final = int(clean_harga_str) if clean_harga_str else 0

                # 5. Simpan
                Produk.objects.update_or_create(
                    id_produk=int(id_prod),
                    defaults={
                        'nama_produk': item.get('nama_produk', 'Tanpa Nama'),
                        'harga': harga_final,
                        'kategori': kategori_obj,
                        'status': status_obj
                    }
                )
            return True, f"Sukses sinkronisasi {len(data_list)} data."
            
    except Exception as e:
        return False, f"Error Database: {str(e)}"
    
    