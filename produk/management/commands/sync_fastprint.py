import json
from django.core.management.base import BaseCommand
from django.db import transaction
from produk.services.fastprint_service import fetch_produk
from produk.models import Produk, Kategori, Status

class Command(BaseCommand):
    help = "Sync produk dari API FastPrint"

    def handle(self, *args, **kwargs):
        self.stdout.write("🔄 Connecting to FastPrint API...")

        # 1. Ambil Data
        response_data = fetch_produk()

        if not response_data:
            self.stdout.write(self.style.ERROR("❌ Gagal: Tidak ada respon dari API"))
            return

        # Handle jika data dibungkus dalam key 'data' atau berupa list langsung
        data_list = response_data if isinstance(response_data, list) else response_data.get('data', [])

        if not data_list:
            self.stdout.write(self.style.WARNING("⚠️ Login Berhasil, tapi data kosong."))
            return

        self.stdout.write(f"📦 Ditemukan {len(data_list)} data.")

        # Mlihat contoh data
        if len(data_list) > 0:
            self.stdout.write(self.style.WARNING("\n=== [DEBUG] CONTOH DATA DARI API ==="))
            # Print 1 data saja biar tidak nyepam
            self.stdout.write(json.dumps(data_list[0], indent=4)) 
            self.stdout.write(self.style.WARNING("====================================\n"))

        self.stdout.write("💾 Mulai menyimpan ke database...")

        try:
            with transaction.atomic():
                counter = 0
                for item in data_list:
                    # Parsing Data
                    
                    # --- A. ID PRODUK ---
                    # Cari key 'id_produk' atau 'no_id'
                    id_prod = item.get('id_produk') or item.get('no_id')
                    if not id_prod:
                        continue # Skip jika tidak ada ID

                    # --- B. KATEGORI ---
                    # Cari ID Kategori (prioritas: kategori_id -> id_kategori -> kategori)
                    raw_cat_id = item.get('kategori_id') or item.get('id_kategori')
                    nama_cat = item.get('nama_kategori') or item.get('kategori') or "Umum"
                    
                    # Jika ID Kategori tidak ada di API, kita buat ID unik dari nama-nya
                    if not raw_cat_id:
                        if isinstance(item.get('kategori'), int):
                             cat_id = item.get('kategori')
                        else:
                             cat_id = abs(hash(nama_cat)) % 100000 
                    else:
                        cat_id = int(raw_cat_id)

                    kategori_obj, _ = Kategori.objects.get_or_create(
                        id_kategori=cat_id, 
                        defaults={'nama_kategori': nama_cat}
                    )

                    # --- C. STATUS ---
                    raw_stat_id = item.get('status_id') or item.get('id_status')
                    nama_stat = item.get('nama_status') or item.get('status') or "Unknown"

                    if not raw_stat_id:
                        if isinstance(item.get('status'), int):
                            stat_id = item.get('status')
                        else:
                            stat_id = abs(hash(nama_stat)) % 100000
                    else:
                        stat_id = int(raw_stat_id)

                    status_obj, _ = Status.objects.get_or_create(
                        id_status=stat_id,
                        defaults={'nama_status': nama_stat}
                    )

                    # --- D. HARGA ---
                    # Bersihkan format "10.000" atau "Rp 10.000"
                    raw_harga = str(item.get('harga', '0'))
                    # Hapus semua karakter yang bukan angka
                    clean_harga_str = ''.join(filter(str.isdigit, raw_harga))
                    harga_final = int(clean_harga_str) if clean_harga_str else 0

                    # --- E. SIMPAN PRODUK ---
                    Produk.objects.update_or_create(
                        id_produk=int(id_prod),
                        defaults={
                            'nama_produk': item.get('nama_produk', 'Tanpa Nama'),
                            'harga': harga_final,
                            'kategori': kategori_obj,
                            'status': status_obj
                        }
                    )
                    counter += 1

                self.stdout.write(self.style.SUCCESS(f"✅ SUKSES! {counter} Data Produk telah tersimpan."))

        except Exception as e:
            # Print error detail baris berapa
            import traceback
            traceback.print_exc()
            self.stdout.write(self.style.ERROR(f"❌ Error Database: {e}"))