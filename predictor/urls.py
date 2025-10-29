from django.urls import path
from .views import index, predict

urlpatterns = [
    path('', index),
    path('predict/', predict, name='predict'),
]