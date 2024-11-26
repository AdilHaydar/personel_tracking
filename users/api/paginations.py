from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

# class DataTablePagination(PageNumberPagination):
#     page_size = 10
#     page_size_query_param = 'length'
#     max_page_size = 100
#     page_query_param = 'start'

    # def get_paginated_response(self, data):
    #     return Response({
    #         'recordsTotal': self.page.paginator.count,
    #         'recordsFiltered': self.page.paginator.count,
    #         'data': data, 
    #     })

class DataTablePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'length'
    max_page_size = 100
    page_query_param = 'start'

    def get_paginated_response(self, data):
        return Response({
            "recordsTotal": self.page.paginator.count,
            "recordsFiltered": self.page.paginator.count,
            "data": data,
        })
