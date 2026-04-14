from rest_framework.pagination import PageNumberPagination
from django.conf import settings


class ApiPagination(PageNumberPagination):
    """
    Кастомная пагинация.

    Позволяет управлять количеством объектов через параметр `limit`.
    Возвращает ответ в формате, соответствующем документации:
    count, next, previous, results.
    """

    page_size = settings.PAGE_SIZE
    page_size_query_param = 'limit'
