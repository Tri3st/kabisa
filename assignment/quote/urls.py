from django.urls import path
from quote import views


urlpatterns = [
    path('', views.index, name='index'),
    path('quote/', views.quote_list, name='quote_list'),
    path('quote/<int:pk>/', views.quote_detail, name='quote_detail'),
]
