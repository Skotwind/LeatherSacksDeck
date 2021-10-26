from django.urls import path
from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view
from rest_framework_swagger.views import get_swagger_view

from .views import *

schema_view = get_schema_view(title='Random User API')
swagger_view = get_swagger_view(title='Random User API')

urlpatterns = [
    path('managers/', ManagerAPIView.as_view()),
    path('workers/', WorkerAPIView.as_view()),
    path('managers/<int:pk>', ManagerDetail.as_view()),
    path('workers/<int:pk>', WorkerDetail.as_view()),
    path('docs', include_docs_urls(title='Random User API')),
    path('schema/', schema_view),
    path('', swagger_view),
]
