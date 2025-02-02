from django.http import JsonResponse
from rest_framework.views import APIView

from backend.models import ConfirmEmailToken


class ConfirmAccount(APIView):
    """
    Класс для подтверждения почтового адреса
    """

    # Регистрация методом POST
    def post(self, request, *args, **kwargs):

        # проверяем обязательные аргументы
        if {'email', 'token'}.issubset(request.data):

            token = ConfirmEmailToken.objects.filter(user__email=request.data['email'],
                                                     key=request.data['token']).first()
            if token:
                token.user.is_active = True
                token.user.save()
                token.delete()
                return JsonResponse({'Status': True})
            else:
                return JsonResponse({'Status': False, 'Errors': 'Неправильно указан токен или email'},
                                    json_dumps_params={'ensure_ascii': False},
                                    safe=False)
        return JsonResponse({
            'Status': False,
            'Errors': 'Не указаны все необходимые аргументы'
        },
            json_dumps_params={'ensure_ascii': False},
            safe=False)