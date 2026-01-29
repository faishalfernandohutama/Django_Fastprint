from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from ..models.models import Produk
from ..models.serialize import ProdukSerializer

class ProdukViewSet(ModelViewSet):
    queryset = Produk.objects.all()
    serializer_class = ProdukSerializer

    #ENDPOINT (bisa dijual)
    @action(detail=False, methods=['get'], url_path='bisa-dijual')
    def bisa_dijual(self, request):
        produk = Produk.objects.filter(status__nama_status='bisa dijual')
        serilizer = self.get_serializer(produk, many=True)
        return Response(serilizer.data)