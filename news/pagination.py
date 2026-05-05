# backend/news/pagination.py
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class NewsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
    
    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })



























# from rest_framework.pagination import PageNumberPagination
# from rest_framework.response import Response

# class NewsPagination(PageNumberPagination):
#     page_size = 5
#     page_size_query_param = 'page_size'
#     max_page_size = 100
    
#     def get_paginated_response(self, data):
#         return Response({
#             'count': self.page.paginator.count,
#             'total_pages': self.page.paginator.num_pages,
#             'current_page': self.page.number,
#             'next': self.get_next_link(),
#             'previous': self.get_previous_link(),
#             'results': data
#         })












# from rest_framework.pagination import PageNumberPagination
# from rest_framework.response import Response
# from backend.settings import PAGINATION_NEWS_PAGE_SIZE as ps

# class NewsPagination(PageNumberPagination):
#     """Пагинация только для новостей"""
#     page_size = ps
#     page_size_query_param = 'page_size'
#     max_page_size = 100
    
#     def get_paginated_response(self, data):
#         return Response({
#             'links': {
#                 'next': self.get_next_link(),
#                 'previous': self.get_previous_link()
#             },
#             'count': self.page.paginator.count,
#             'total_pages': self.page.paginator.num_pages,
#             'current_page': self.page.number,
#             'results': data
#         })