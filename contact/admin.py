from django.contrib import admin
from contact import models

# Register your models here.

@admin.register(models.Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = 'id', 'first_name', 'last_name', 'email', 'phone', 'show', 'category', 'owner'
    ordering = '-id',
    list_filter = 'created_date',
    list_editable = 'show',
    search_fields = 'id', 'first_name', 'last_name',
    list_per_page = 10
    list_max_show_all = 200
    # list_editable = 'first_name', 'last_name',
    list_display_links = 'id', 'first_name',
    # prepopulated_fields = ''

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = 'id', 'name'
    ordering = 'id',
    search_fields = 'id', 'name',
    list_per_page = 10
    list_max_show_all = 200
    list_display_links = 'id', 'name',