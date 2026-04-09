from rest_framework.pagination import PageNumberPagination

from foodgram.constants import MAX_LIMIT_PAGE_SIZE


class UserPagination(PageNumberPagination):
    """Пагинация пользователей."""

    page_size_query_param = 'limit'
    max_page_size = MAX_LIMIT_PAGE_SIZE
