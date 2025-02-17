from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class VideoPagination(PageNumberPagination):
    page_size = 10  # Set the number of results per page
    page_size_query_param = 'page_size'
    max_page_size = 50

    def get_paginated_response(self, data):
        return Response({
            'total_count': self.page.paginator.count,
            'next_page': self.get_next_link(),
            'prev_page': self.get_previous_link(),
            'results': data
        })
