from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['farm', 'author', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['text', 'farm__name', 'author__username']
