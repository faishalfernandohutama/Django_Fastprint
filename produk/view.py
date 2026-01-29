from django import forms
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .services.fastprint_service import fetch_produk
from .models import Produk, Kategori, Status
from .serialize import ProdukSerializer


def sync_produk():
    data = fetch_produk()

    for item in data["data"]:
        kategori, _ = Kategori.objects.get_or_create(
            id_kategori=item["kategori_id"],
            defaults={"nama_kategori": item["kategori"]}
        )

        status, _ = Status.objects.get_or_create(
            id_status=item["status_id"],
            defaults={"nama_status": item["status"]}
        )

        Produk.objects.update_or_create(
            id_produk=item["id_produk"],
            defaults={
                "nama_produk": item["nama_produk"],
                "harga": item["harga"],
                "kategori": kategori,
                "status": status
            }
        )


def sync_produk_view(request):
    sync_produk()
    return JsonResponse({"message": "Sinkronisasi produk berhasil"})


@api_view(['GET'])
def produk_bisa_dijual(request):
    produk = Produk.objects.filter(status__nama_status__iexact="bisa dijual")
    serializer = ProdukSerializer(produk, many=True)
    return Response(serializer.data)


class ProdukForm(forms.ModelForm):
    class Meta:
        model = Produk
        fields = "__all__"

    def clean_harga(self):
        harga = self.cleaned_data.get('harga')
        if not isinstance(harga, int):
            raise forms.ValidationError("Harga harus berupa angka")
        if harga <= 0:
            raise forms.ValidationError("Harga harus lebih dari 0")
        return harga
