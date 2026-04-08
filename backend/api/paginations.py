from rest_framework.pagination import PageNumberPagination

from django.conf import settings


class RecipePagination(PageNumberPagination):
    """Пагинация рецептов."""
    page_size_query_param = 'limit'
    max_page_size = settings.MAX_LIMIT_PAGE_SIZE


class UserPagination(PageNumberPagination):
    """Пагинация пользователей."""

    page_size_query_param = 'limit'
    max_page_size = settings.MAX_LIMIT_PAGE_SIZE
