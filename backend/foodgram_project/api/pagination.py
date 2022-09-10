from rest_framework.pagination import PageNumberPagination


class CustomPageNumberSerializer(PageNumberPagination):
    """ Custom page pagination with client limit. """

    page = 5
    page_size_query_param = 'limit'
