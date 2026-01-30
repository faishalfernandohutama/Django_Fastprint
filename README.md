🖨️ Tes Teknis Programmer - FastPrint Indonesia
Repositori ini berisi solusi untuk Tes Teknis Programmer FastPrint. Aplikasi ini adalah sistem manajemen produk berbasis web yang dibangun menggunakan Django Framework. Sistem ini mengambil data dari API eksternal, menyimpannya ke database relasional, dan menyediakan fitur CRUD dengan validasi ketat.

📋 Fitur Utama
Aplikasi ini telah memenuhi seluruh poin persyaratan (1-11) yang diminta dalam soal tes:

Sinkronisasi API Otomatis 🔄

Mengambil data dari API FastPrint dengan autentikasi dinamis (Username & Password berbasis tanggal/jam).

Data dipetakan secara otomatis ke database lokal.

Struktur Database Relasional 🗂️

Menggunakan 3 tabel terpisah: Produk, Kategori, dan Status (Normalisasi Database).

Filtering Data 🔍

Hanya menampilkan produk dengan status "bisa dijual" pada halaman utama.

Manajemen Produk (CRUD) 📝

Create: Menambah produk baru dengan validasi.

Read: Menampilkan daftar produk.

Update: Mengedit data produk.

Delete: Menghapus produk dengan konfirmasi keamanan.

Validasi & Keamanan 🛡️

Validasi Form: Nama wajib diisi, Harga wajib angka dan tidak boleh negatif.

Javascript Confirm: Alert konfirmasi saat menghapus data.

Menggunakan Django REST Framework Serializer untuk validasi data API.

Desain 📱

Antarmuka menggunakan Css Polos yang rapi dan mudah digunakan.

🛠️ Teknologi yang Digunakan
Backend: Python 3.12, Django 5.x

Database: SQLite (Default) / Kompatibel dengan PostgreSQL & MySQL

API & Serializer: Django REST Framework (DRF), Requests Library

Frontend: HTML5, Bootstrap 5, JavaScript (SweetAlert/Native Confirm)

Utilities: Pytz (Timezone handling), Hashlib (MD5 Generation)


⚙️ Instalasi & Cara Menjalankan
Ikuti langkah-langkah berikut untuk menjalankan proyek ini di komputer lokal Anda:

1. Clone Repositori
Bash
git clone https://github.com/faishalfernandohutama/Django_Fastprint.git
cd Django_Fastprint
2. Buat Virtual Environment (Disarankan)
Bash
# Untuk Windows
python -m venv venv
venv\Scripts\activate

# Untuk Mac/Linux
python3 -m venv venv
source venv/bin/activate
3. Install Dependencies
Bash
pip install django djangorestframework requests pytz
(Atau jika ada file requirements.txt: pip install -r requirements.txt)

4. Migrasi Database
Siapkan struktur database (tabel Produk, Kategori, Status):

Bash
python manage.py makemigrations
python manage.py migrate
5. Jalankan Server
Bash
python manage.py runserver

📸 Panduan Penggunaan
1. Sinkronisasi Data (Sync)
Pada halaman utama, klik tombol kuning "🔄 Sync API". Sistem akan:

Membuat kredensial username/password sesuai format tanggal saat ini.

Menghubungi API recruitment.fastprint.co.id.

Menyimpan data Kategori dan Status baru jika belum ada.

Menyimpan/Update data Produk.

2. Menambah & Mengedit Data
Klik tombol "Tambah" untuk input manual.

Sistem akan menolak jika harga diisi huruf atau angka negatif.

3. Menghapus Data
Klik tombol "Hapus".

Akan muncul pop-up konfirmasi browser untuk mencegah penghapusan tidak sengaja.

📝 Catatan Pengembang
Proyek ini menggunakan library pytz untuk memastikan timestamp pembuatan password API sesuai dengan Waktu Indonesia Barat (Asia/Jakarta), menghindari kegagalan autentikasi server.

Sesuai instruksi Poin 9, proyek ini memanfaatkan serializers dari Django Rest Framework untuk memproses data yang masuk.


### 🗂️ Struktur Database (ERD)
Diagram ini dibuat berdasarkan `models.py` yang digunakan dalam proyek ini:

erDiagram
    PRODUK }|--|| KATEGORI : "Memiliki Kategori"
    PRODUK }|--|| STATUS : "Memiliki Status"

    PRODUK {
        int id_produk PK "Primary Key (Input Manual/API)"
        string nama_produk "Max 255 Char"
        int harga "Integer (Harus Angka)"
        int kategori_id FK "Relasi ke Tabel Kategori"
        int status_id FK "Relasi ke Tabel Status"
    }

    KATEGORI {
        int id_kategori PK
        string nama_kategori
    }

    STATUS {
        int id_status PK
        string nama_status
    }

**Penjelasan Teknis:**
* **PK (Primary Key):** Menandakan `id_produk`, `id_kategori`, dan `id_status` adalah kunci utama.
* **FK (Foreign Key):** Menandakan hubungan tabel Produk ke Kategori dan Status.
* **`}|--||`**: Simbol ini berarti "Banyak ke Satu" (Many-to-One). Artinya: Banyak Produk bisa memiliki Satu Kategori yang sama.

📋 Fitur Utama
Aplikasi ini telah memenuhi persyaratan 1-11:

Sinkronisasi API Otomatis: Mengambil data real-time dengan autentikasi dinamis (MD5 berdasarkan tanggal/jam server).
Database Relasional: Menggunakan ForeignKey untuk efisiensi data.
Filtering Cerdas: Hanya menampilkan produk dengan status "bisa dijual" di halaman utama.
CRUD Lengkap:
Create: Tambah produk baru.
Read: List produk dengan pagination (opsional).
Update: Edit data produk.
Delete: Hapus data produk.
Validasi Ketat (Poin 7):
Harga: Harus angka & tidak boleh negatif.
Nama: Wajib diisi.
Keamanan UX (Poin 8): Konfirmasi JavaScript Alert saat menghapus data.
Teknologi: Django + Django REST Framework Serializers.

🔌 Daftar Endpoint URL
Method,Endpoint,Deskripsi
GET,/produk/,"Halaman utama (Menampilkan produk ""bisa dijual"")"
GET,/produk/sync/,Memicu proses sinkronisasi API
GET/POST,/produk/tambah/,Form tambah produk baru
GET/POST,/produk/edit/<id>/,Form edit produk
POST,/produk/hapus/<id>/,Menghapus produk (Butuh Konfirmasi)

Author
Faishal Fernando Hutama GitHub: faishalfernandohutama
