from django import forms
from .models import Produk

class ProdukForm(forms.ModelForm):
    class Meta:
        model = Produk
        fields = ['nama_produk', 'harga', 'kategori', 'status']
        widgets = {
            'nama_produk': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'harga': forms.NumberInput(attrs={'class': 'form-control', 'required': True}),
            'kategori': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    # Validasi Tambahan Poin 7
    def clean_harga(self):
        harga = self.cleaned_data.get('harga')
        if harga is None:
            raise forms.ValidationError("Harga wajib diisi angka.")
        if harga < 0:
            raise forms.ValidationError("Harga tidak boleh negatif.")
        return harga
    
    def clean_nama_produk(self):
        nama = self.cleaned_data.get('nama_produk')
        if not nama:
            raise forms.ValidationError("Nama produk wajib diisi.")
        return nama