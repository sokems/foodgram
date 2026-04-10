from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.conf import settings


class CustomPagination(PageNumberPagination):
    """
    Кастомная пагинация.

    Позволяет управлять количеством объектов через параметр `limit`.
    Возвращает ответ в формате, соответствующем документации:
    count, next, previous, results.
    """

    page_size = settings.PAGE_SIZE
    page_size_query_param = 'limit'
    max_page_size = settings.MAX_PAGE_SIZE

    def get_paginated_response(self, data):
        """
        Формирует ответ с пагинацией в требуемом формате.
        """
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
        })
