from django.db import models

class Kategori(models.Model):
    id_kategori = models.IntegerField(primary_key=True)
    nama_kategori = models.CharField(max_length=100)

    def __str__(self):
        return self.nama_kategori

class Status(models.Model):
    id_status = models.IntegerField(primary_key=True)
    nama_status = models.CharField(max_length=50)

    def __str__(self):
        return self.nama_status

class Produk(models.Model):
    id_produk = models.IntegerField(primary_key=True)
    nama_produk = models.CharField(max_length=255)
    # Poin 7: Harga harus angka
    harga = models.IntegerField()
    
    # Poin 2: Relasi ke Kategori dan Status
    kategori = models.ForeignKey(Kategori, on_delete=models.CASCADE, related_name='produk')
    status = models.ForeignKey(Status, on_delete=models.CASCADE, related_name='produk')

    def __str__(self):
        return self.nama_produk