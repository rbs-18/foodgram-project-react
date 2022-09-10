from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
    """ Custom page pagination with client limit. """

    page_size = 5
    page_size_query_param = 'limit'
