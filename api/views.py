from rest_framework import generics, pagination
from rest_framework.response import Response

from .serializers import *


class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def get_paginated_response(self, data):
        return Response({
            'count': len(data),
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })


class ManagerAPIView(generics.ListAPIView):
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer
    pagination_class = StandardResultsSetPagination


class WorkerAPIView(generics.ListAPIView):
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer
    pagination_class = StandardResultsSetPagination


class WorkerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer


class ManagerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer
