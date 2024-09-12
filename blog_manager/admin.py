from django.contrib import admin
from .models import BlogPost, Comment, Category, Tag, Reaction, UserProfile

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'category', 'created_at', 'updated_at')
    search_fields = ('title', 'content', 'author__username', 'category__name')
    list_filter = ('author', 'category', 'created_at')
    ordering = ('-created_at',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'author', 'status', 'created_at')
    search_fields = ('content', 'author__username', 'post__title')
    list_filter = ('status', 'post', 'author')
    ordering = ('-created_at',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Reaction)
class ReactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'reaction_type')
    search_fields = ('user__username', 'post__title', 'reaction_type')
    list_filter = ('reaction_type', 'post', 'user')
    ordering = ('-post',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name')
    search_fields = ('user__username', 'first_name', 'last_name')
    ordering = ('user__username',)
