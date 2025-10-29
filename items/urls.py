from django.contrib import admin
from django.urls import path

from items import views
from items.views import ItemView

urlpatterns = [
    path('', ItemView.as_view()),
    path('<int:item_id>/', ItemView.as_view()),

    path('form/', views.create_form)
]