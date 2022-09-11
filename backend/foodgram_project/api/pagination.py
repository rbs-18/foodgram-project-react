from rest_framework.pagination import PageNumberPagination


class LimitPageNumberPagination(PageNumberPagination):
    """ Custom page pagination with client limit. """

    page_size_query_param = 'limit'
