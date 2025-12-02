from django.contrib import admin
from .models import User, Chat

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Admin configuration for the User model.
    """
    list_display = ('id', 'email', 'name', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('email', 'name')
    list_filter = ('is_active', 'is_staff', 'date_joined')
    ordering = ('-date_joined',)

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Chat model.
    """
    list_display = ('id', 'user', 'created_at')
    search_fields = ('user__email', 'user__name')
    list_filter = ('created_at', 'user')
    ordering = ('-created_at',)
