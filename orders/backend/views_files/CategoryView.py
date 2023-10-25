from rest_framework.viewsets import ModelViewSet

from backend.models import Category
from backend.serializers import ProductSerializer


class CategoryView(ModelViewSet):
    """
    Класс для просмотра категорий
    """
    queryset = Category.objects.all()
    serializer_class = ProductSerializer
    http_method_names = ['get']