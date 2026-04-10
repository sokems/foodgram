from rest_framework.views import exception_handler
from rest_framework import status


def custom_exception_handler(exc, context):
    """
    Перехватывает ВСЕ 404 ошибки и меняет сообщение.
    Работает для User, Tag, Recipe, Ingredient и любых других моделей.
    """
    response = exception_handler(exc, context)

    if (response is not None
            and response.status_code == status.HTTP_404_NOT_FOUND):
        response.data = {
            'detail': 'Страница не найдена.'
        }

    return response
