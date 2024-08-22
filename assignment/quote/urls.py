from django.urls import path
from quote import views


urlpatterns = [
    path('', views.index, name='index'),
    path('quote/', views.quote_list, name='quote_list'),
    path('quote/<int:pk>/', views.quote_detail, name='quote_detail'),
    path('quote/xml/<int:pk>/', views.quote_detail_xml, name='quote_detail_xml'),
    path('quote/<int:pk>/like', views.quote_detail_like, name='quote_detail_like'),
    path('quote/random/', views.random_quote, name='random_quote'),
]
