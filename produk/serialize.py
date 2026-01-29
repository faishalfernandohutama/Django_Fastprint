from rest_framework import serializers
from .models import Produk, Kategori, Status

class ProdukSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produk
        fields = ['id_produk', 'nama_produk', 'harga', 'kategori', 'status']