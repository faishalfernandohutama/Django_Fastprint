from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django import forms
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Import Logic yang sudah disatukan tadi
from .services.fastprint_service import sync_and_save_products
from .models import Produk, Kategori, Status
from .serialize import ProdukSerializer # Pastikan file serialize.py ada

# --- VIEW 1: UNTUK TRIGGER SYNC ---
def trigger_sync(request):
    success, message = sync_and_save_products()
    if success:
        return JsonResponse({"status": "success", "message": message})
    else:
        return JsonResponse({"status": "error", "message": message}, status=500)

# --- VIEW 2: HALAMAN UTAMA (HTML - Sesuai Soal) ---
def index(request):
    # Filter hanya "bisa dijual"
    produk_list = Produk.objects.filter(status__nama_status__iexact="bisa dijual")
    
    context = {
        'produk_list': produk_list
    }
    return render(request, 'produk/index.html', context)

# --- VIEW 3: API ENDPOINT (DRF - Opsional/Bonus) ---
@api_view(['GET'])
def api_produk_list(request):
    produk = Produk.objects.filter(status__nama_status__iexact="bisa dijual")
    serializer = ProdukSerializer(produk, many=True)
    return Response(serializer.data)

# --- FORM & CRUD (Untuk Edit/Tambah) ---
class ProdukForm(forms.ModelForm):
    class Meta:
        model = Produk
        fields = ['nama_produk', 'harga', 'kategori', 'status']

    def clean_harga(self):
        harga = self.cleaned_data.get('harga')
        # Tidak perlu check isinstance(int), Django form field sudah handle itu.
        # Cukup check logic bisnis:
        if harga is not None and harga < 0:
            raise forms.ValidationError("Harga tidak boleh negatif")
        return harga

# Contoh View Edit (Bonus CRUD)
def edit_produk(request, id_produk):
    produk = get_object_or_404(Produk, pk=id_produk)
    if request.method == "POST":
        form = ProdukForm(request.POST, instance=produk)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ProdukForm(instance=produk)
    
    return render(request, 'produk/form_produk.html', {'form': form})
