from django.contrib import admin
from django.urls import path

from items import views

urlpatterns = [
    path('', views.index),
    path('create/', views.create),
    path('read/', views.read),
    path('read/<int:item_id>/', views.read),
    path('delete/<int:item_id>/', views.delete),
    path('update/<int:item_id>/', views.update),
]