from rest_framework.pagination import PageNumberPagination


class ArticlesPagination(PageNumberPagination):
    page_size = 50
    display_page_controls = True
    page_size_query_param = "size"
