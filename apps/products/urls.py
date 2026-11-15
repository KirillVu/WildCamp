from django.urls import path
from . import views
urlpatterns = [path('catalog/', views.catalog, name='catalog'), path('category/<str:slug>/', views.category, name='category'), path('product/<str:slug>/', views.product_detail, name='product_detail')]
