from django.contrib import admin
from django.urls import path,include
from .views import PolygonApi,PolygonView

urlpatterns = [
    path('',PolygonView.as_view()),
    path('<int:pk>',PolygonApi.as_view())
]
