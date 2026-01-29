from django.urls import path
from . import view

urlpatterns = [
    path('', view.index, name='index'),
    path('sync/', view.run_sync, name='run_sync'),
    path('tambah/', view.tambah, name='tambah'),
    path('edit/<int:id_produk>/', view.edit, name='edit'),
    path('hapus/<int:id_produk>/', view.hapus, name='hapus'),
]