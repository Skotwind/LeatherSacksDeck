from rest_framework import generics, pagination

from .serializers import *


class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 1000


class ManagerAPIView(generics.ListAPIView):
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer
    pagination_class = StandardResultsSetPagination


class WorkerAPIView(generics.ListAPIView):
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer


class WorkerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer


class ManagerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer
