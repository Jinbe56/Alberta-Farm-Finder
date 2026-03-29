from django.urls import path
from . import views

app_name = 'farms'

urlpatterns = [
    path('', views.search, name='search'),
    path('farms/new/', views.farm_create, name='create'),
    path('farms/<slug:slug>/', views.farm_detail, name='detail'),
    path('farms/<slug:slug>/edit/', views.farm_edit, name='edit'),
    path('farms/<slug:slug>/products/', views.manage_products, name='manage_products'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('markets/', views.market_list, name='market_list'),
    path('markets/<slug:slug>/', views.market_detail, name='market_detail'),
    path('markets/<slug:slug>/join/', views.market_join, name='market_join'),
    path('api/farms/search/', views.search, name='search_api'),
    path('api/farms/map-data/', views.map_data, name='map_data'),
]
