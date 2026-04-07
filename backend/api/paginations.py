from rest_framework.pagination import PageNumberPagination

from foodgram.settings import REST_FRAMEWORK


class CustomPagination(PageNumberPagination):
    """
    Пагинатор для вывода кастомного
    количества элементов на странице.
    """

    page_size_query_param = 'limit'
    page_size = REST_FRAMEWORK['PAGE_SIZE']
