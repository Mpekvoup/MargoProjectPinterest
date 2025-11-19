from django.contrib import admin
from .models import Pin, Board, Comment


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'is_private', 'pin_count', 'created_at']
    list_filter = ['is_private', 'created_at']
    search_fields = ['name', 'description', 'user__username']
    prepopulated_fields = {'slug': ('name',)}
    date_hierarchy = 'created_at'


@admin.register(Pin)
class PinAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'board', 'like_count', 'created_at']
    list_filter = ['created_at', 'board']
    search_fields = ['title', 'description', 'tags', 'user__username']
    date_hierarchy = 'created_at'
    raw_id_fields = ['user', 'board']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'pin', 'text', 'created_at']
    list_filter = ['created_at']
    search_fields = ['text', 'user__username', 'pin__title']
    date_hierarchy = 'created_at'
