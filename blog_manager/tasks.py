from celery import shared_task
from .models import BlogPost, UserProfile
from django.core.cache import cache
from django.conf import settings

@shared_task
def cache_blog_post(blog_post_id):
    try:
        blog_post = BlogPost.objects.get(id=blog_post_id)
        cache_key = f"{settings.KEY_PREFIX}_blog_post_detail_{blog_post_id}"
        cache.set(cache_key, {
            'title': blog_post.title,
            'content': blog_post.content,
            'author': blog_post.author.username,
            'category': blog_post.category.name if blog_post.category else None,
            'created_at': blog_post.created_at,
            'updated_at': blog_post.updated_at,
        }, timeout=settings.CACHE_TTL)
        print(f"Cache updated for new blog post ID {blog_post_id}.")
    except BlogPost.DoesNotExist:
        print(f"Blog post with ID {blog_post_id} does not exist.")


@shared_task
def cache_user_profile(user_id):
    try:
        user_profile = UserProfile.objects.get(user_id=user_id)
        cache_key = f"{settings.KEY_PREFIX}_user_profile_{user_id}"
        cache.set(cache_key, {
            'first_name': user_profile.first_name,
            'last_name': user_profile.last_name,
            'bio': user_profile.bio,
            'profile_picture': user_profile.profile_picture.url if user_profile.profile_picture else None,
        }, timeout=settings.CACHE_TTL)
        print(f"Cache updated for new user profile ID {user_id}.")
    except UserProfile.DoesNotExist:
        print(f"User profile for user ID {user_id} does not exist.")
