from rest_framework.pagination import PageNumberPagination

class RoomPagination(PageNumberPagination):
    page_size = 5
    page_query_param = 'page_size'
    max_page_size = 100

class RatingPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page_size'
    max_page_size = 300

class CommentPagination(PageNumberPagination):
    page_size = 20
    page_query_param = 'page_size'
    max_page_size = 100
