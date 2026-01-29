import requests
import hashlib
from datetime import datetime
import pytz
from produk.models import Produk, Kategori, Status

def sync_fastprint_data():
    # 1. Setup Credentials (sesuai logic sebelumnya)
    url = "https://recruitment.fastprint.co.id/tes/api_tes_programmer"
    tz = pytz.timezone('Asia/Jakarta')
    now = datetime.now(tz)
    username = f"tesprogrammer{now.strftime('%d%m%y')}C{now.strftime('%H')}"
    password = hashlib.md5(f"bisacoding-{now.strftime('%d-%m-%y')}".encode()).hexdigest()

    try:
        # 2. Request ke API
        response = requests.post(
            url, 
            data={'username': username, 'password': password},
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        if response.status_code != 200:
            return False, "Gagal koneksi ke API"

        data_json = response.json()
        items = data_json.get('data', [])

        # 3. Simpan ke Database
        for item in items:
            # Handle ID Produk (Skip jika kosong)
            id_prod = item.get('id_produk')
            if not id_prod: continue

            # Handle Kategori (Cari atau Buat)
            # Karena API kasih nama, tapi kita butuh ID untuk relasi
            kat_nama = item.get('kategori') or "Umum"
            kat_id = item.get('kategori_id') or abs(hash(kat_nama)) % 100000
            
            kategori_obj, _ = Kategori.objects.get_or_create(
                id_kategori=int(kat_id),
                defaults={'nama_kategori': kat_nama}
            )

            # Handle Status
            stat_nama = item.get('status') or "Unknown"
            stat_id = item.get('status_id') or abs(hash(stat_nama)) % 100000
            
            status_obj, _ = Status.objects.get_or_create(
                id_status=int(stat_id),
                defaults={'nama_status': stat_nama}
            )

            # Bersihkan Harga (Hapus titik/koma)
            raw_harga = str(item.get('harga', '0'))
            clean_harga = ''.join(filter(str.isdigit, raw_harga))
            
            # Simpan Produk
            Produk.objects.update_or_create(
                id_produk=int(id_prod),
                defaults={
                    'nama_produk': item.get('nama_produk'),
                    'harga': int(clean_harga) if clean_harga else 0,
                    'kategori': kategori_obj,
                    'status': status_obj
                }
            )
        
        return True, f"Berhasil sinkronisasi {len(items)} data."

    except Exception as e:
        return False, f"Error System: {e}"