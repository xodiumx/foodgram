from rest_framework.pagination import PageNumberPagination


class PagePaginationWithLimit(PageNumberPagination):
    """Доп. параметр для пагинации."""
    page_size_query_param = ('limit')