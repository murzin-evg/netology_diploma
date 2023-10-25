from rest_framework.viewsets import ModelViewSet

from backend.models import Shop
from backend.serializers import ShopSerializer


class ShopView(ModelViewSet):
    """
    Класс для просмотра магазинов.
    """
    queryset = Shop.objects.filter(status=True)
    serializer_class = ShopSerializer
    http_method_names = ['get']