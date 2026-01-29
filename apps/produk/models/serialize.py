from rest_framework import serializers
from .models import Produk, Kategori, Status

class KategoriSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kategori
        fields = ['id', 'nama_kategori']

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ['id', 'nama_status']

class ProdukSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produk
        fields = ['id', 'nama_produk', 'harga', 'Kategori', 'status']

def validate_nama_produk(self, value):
        if  not value or value.strip() == "":
            raise serializers.ValidationError("Nama produk tidak boleh kosong.")
        
def validate_harga(self, value):
     if not isinstance(value, int):
          raise serializers.ValidationError("Harus berupa angka.")
     if value <= 0:
          raise serializers.ValidationError("Harga harus lebih dari nol.")
     return value