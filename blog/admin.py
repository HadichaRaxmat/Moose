from django.contrib import admin
from .models import Post, Contact, Comment, Category
from datetime import datetime
from django.utils.html import format_html


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


class PostInline(admin.TabularInline):
    model = Post
    extra = 0
    fields = ('title', 'is_published')


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'title', 'is_published', 'comments_count', 'view_count', 'created_at')
    list_display_links = ('id', 'author', 'title')
    inlines = (CommentInline,)
    search_fields = ('title', 'author')
    list_filter = ('author', 'is_published')


class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'email', 'subject', 'is_solved', 'days', 'created_at',)
    list_display_links = ('id', 'full_name', 'email')

    def days(self, obj):
        days_diff = (datetime.now() - obj.created_at).days
        if days_diff > 3:
            color = 'red'
        else:
            color = 'blue'
        if obj.is_solved:
            color = 'green'
        return format_html("<div style='color: {}'>{}</div>", color, days_diff)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'message', 'post', 'is_published', 'created_at')
    list_display_links = ('id', 'name', 'email',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    list_display_links = ('id', 'name')
    inlines = (PostInline,)


admin.site.register(Post, PostAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)
