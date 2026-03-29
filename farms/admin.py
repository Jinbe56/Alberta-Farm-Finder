from django.contrib import admin
from .models import Farm, Category, FarmPhoto, FarmersMarket, FarmProduct


class FarmPhotoInline(admin.TabularInline):
    model = FarmPhoto
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'icon', 'slug']
    list_filter = ['parent']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Farm)
class FarmAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'address_display', 'is_active', 'is_verified', 'updated_at']
    list_filter = ['is_active', 'is_verified', 'province']
    search_fields = ['name', 'description', 'address_display']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [FarmPhotoInline]
    filter_horizontal = ['categories']


class FarmProductInline(admin.TabularInline):
    model = FarmProduct
    extra = 1


@admin.register(FarmersMarket)
class FarmersMarketAdmin(admin.ModelAdmin):
    list_display = ['name', 'address_display', 'frequency', 'day_of_week', 'next_date', 'is_active']
    list_filter = ['is_active', 'frequency']
    search_fields = ['name', 'address_display']
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ['vendors']


@admin.register(FarmProduct)
class FarmProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'farm', 'category', 'is_available', 'is_seasonal', 'updated_at']
    list_filter = ['is_available', 'is_seasonal']
    search_fields = ['name', 'farm__name']
