from django.contrib import admin
from django.urls import path

from items import views

urlpatterns = [
    path('', views.item_view),
    path('<int:item_id>/', views.item_view),
]