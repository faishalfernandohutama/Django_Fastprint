from django.contrib import admin
from .models import Produk, Kategori, Status


@admin.register(Kategori)
class KategoriAdmin(admin.ModelAdmin):
    list_display = ('id_kategori', 'nama_kategori')


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('id_status', 'nama_status')


@admin.register(Produk)
class ProdukAdmin(admin.ModelAdmin):
    list_display = (
        'id_produk',
        'nama_produk',
        'harga',
        'kategori',
        'status',
    )
    list_filter = ('status', 'kategori')
    search_fields = ('nama_produk',)
    ordering = ('nama_produk',)
    list_per_page = 20

