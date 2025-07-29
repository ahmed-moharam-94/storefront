from rest_framework.pagination import PageNumberPagination

class DefaultPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'size'  # Allow ?page_size=60
    max_page_size = 100  # Optional: Limit maximum page size