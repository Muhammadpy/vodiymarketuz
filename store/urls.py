from django.urls import path
from .views import store
from . import views

urlpatterns = [
    path('', store, name= 'store'),
    path('category/<slug:category_slug>/', store, name= 'products_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>/', views.product_detail, name= 'product_detail'),
    path('search/', views.search, name='search'),
]