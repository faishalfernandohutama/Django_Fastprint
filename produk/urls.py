from django.urls import path
from .view import produk_bisa_dijual

urlpatterns = [
    path('', produk_bisa_dijual, name='produk-list'),
]