from django.contrib import admin
from ads.models import Ad, Comment


class AdAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'price', 'created_at')
    list_filter = ('created_at', 'author')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)

admin.site.register(Ad, AdAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'ad', 'created_at')
    list_filter = ('created_at', 'author')
    search_fields = ('author__email', 'ad__title')

admin.site.register(Comment, CommentAdmin)
