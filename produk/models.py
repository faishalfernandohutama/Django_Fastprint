from django.db import models

class Kategori(models.Model):
    id_kategori = models.IntegerField(primary_key=True)
    nama_kategori = models.CharField(max_length=100)

    class Meta:
        db_table = 'kategori'

    def __str__(self):
        return self.nama_kategori


class Status(models.Model):
    id_status = models.IntegerField(primary_key=True)
    nama_status = models.CharField(max_length=50)

    class Meta:
        db_table = 'status'

    def __str__(self):
        return self.nama_status


class Produk(models.Model):
    id_produk = models.IntegerField(primary_key=True)
    nama_produk = models.CharField(max_length=255)
    harga = models.PositiveIntegerField()
    kategori = models.ForeignKey(Kategori, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)

    class Meta:
        db_table = 'produk'

    def __str__(self):
        return self.nama_produk
