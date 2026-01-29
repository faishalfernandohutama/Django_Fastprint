from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Produk
from .forms import ProdukForm
from .services.fastprint_service import sync_fastprint_data

# --- FITUR TAMBAHAN: SYNC DATA ---
def run_sync(request):
    success, msg = sync_fastprint_data()
    if success:
        messages.success(request, msg)
    else:
        messages.error(request, msg)
    return redirect('index')

# --- POIN 4 & 5: TAMPILKAN DATA (FILTER BISA DIJUAL) ---
def index(request):
    # Filter Poin 5: Hanya status "bisa dijual"
    # Gunakan 'iexact' agar tidak sensitif huruf besar/kecil
    produk_list = Produk.objects.filter(
        status__nama_status__iexact='bisa dijual'
    ).select_related('kategori', 'status').order_by('id_produk')

    return render(request, 'produk/index.html', {'produk_list': produk_list})

# --- POIN 6 & 7: TAMBAH DATA ---
def tambah(request):
    if request.method == 'POST':
        form = ProdukForm(request.POST)
        if form.is_valid():
            # Generate ID Manual (karena id_produk bukan AutoIncrement di models)
            produk = form.save(commit=False)
            last_id = Produk.objects.order_by('-id_produk').first()
            produk.id_produk = (last_id.id_produk + 1) if last_id else 1
            produk.save()
            
            messages.success(request, "Produk berhasil ditambah.")
            return redirect('index')
    else:
        form = ProdukForm()
    
    return render(request, 'produk/form.html', {'form': form, 'title': 'Tambah Produk'})

# --- POIN 6 & 7: EDIT DATA ---
def edit(request, id_produk):
    produk = get_object_or_404(Produk, pk=id_produk)
    if request.method == 'POST':
        form = ProdukForm(request.POST, instance=produk)
        if form.is_valid():
            form.save()
            messages.success(request, "Produk berhasil diupdate.")
            return redirect('index')
    else:
        form = ProdukForm(instance=produk)
    
    return render(request, 'produk/form.html', {'form': form, 'title': 'Edit Produk'})

# --- POIN 6 & 8: HAPUS DATA ---
def hapus(request, id_produk):
    produk = get_object_or_404(Produk, pk=id_produk)
    produk.delete()
    messages.success(request, "Produk berhasil dihapus.")
    return redirect('index')