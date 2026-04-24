from django.contrib import admin
from .models import Post, Comment

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'status','created_on')
    list_filter = ("status",)
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}

class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created_on')
    list_filter = ('created_on',)
    search_fields = ('author', 'content')

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
