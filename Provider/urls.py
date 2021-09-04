from django.contrib import admin
from django.urls import path,include
from .views import ProviderView,EditProvider,loginView

urlpatterns = [
    path('',ProviderView.as_view()),
    path('login',loginView),
    path('<int:pk>',EditProvider.as_view())

]
