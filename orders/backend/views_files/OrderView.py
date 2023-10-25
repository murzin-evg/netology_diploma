from django.db import IntegrityError
from django.db.models import Sum, F
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView

from backend.models import Order
from backend.serializers import OrderSerializer
from backend.signals import new_order


class OrderView(APIView):
    """
    Класс для получения и размещения заказов пользователями
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    http_method_names = ['get', 'post']

    # получить мои заказы
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)
        order = Order.objects.filter(
            user_id=request.user.id).exclude(status='BASKET').prefetch_related(
            'ordered_items__product_info__product__category',
            'ordered_items__product_info__product_parameters__parameter').select_related('contact').annotate(
            total_sum=Sum(F('ordered_items__quantity') * F('ordered_items__product_info__price'))).distinct()

        serializer = OrderSerializer(order, many=True)
        return Response(serializer.data)

    # разместить заказ из корзины
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)

        if {'id', 'contact'}.issubset(request.data):
            if request.data['id'].isdigit():
                try:
                    is_updated = Order.objects.filter(
                        user_id=request.user.id, id=request.data['id']).update(
                        contact_id=request.data['contact'],
                        status='NEW')
                except IntegrityError as error:
                    print(error)
                    return JsonResponse({'Status': False, 'Errors': 'Неправильно указаны аргументы'},
                                        json_dumps_params={'ensure_ascii': False})
                else:
                    if is_updated:
                        new_order.send(sender=self.__class__, user_id=request.user.id)
                        return JsonResponse({'Status': True})
        return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'},
                            json_dumps_params={'ensure_ascii': False})