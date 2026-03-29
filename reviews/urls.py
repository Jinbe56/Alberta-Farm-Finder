from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('farms/<slug:slug>/reviews/', views.review_list, name='list'),
    path('farms/<slug:slug>/reviews/new/', views.review_create, name='create'),
    path('farms/<slug:slug>/reviews/<int:pk>/respond/', views.review_respond, name='respond'),
]
