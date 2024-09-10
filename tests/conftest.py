# conftest.py
import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from blog_manager.models import BlogPost, Category, Tag, Reaction, Comment, UserProfile

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user(api_client):
    user = User.objects.create_user(username='pooji', password='pooji123')
    return user
# @pytest.fixture
# def admin_user(api_client):
#     user = User.objects.create_superuser(username='djangoadmin', password='django123')
#     return user

@pytest.fixture
def auth_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client

@pytest.fixture
def admin_client(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    return api_client

@pytest.fixture
def category():
    return Category.objects.create(name='Tech')

@pytest.fixture
def tag():
    return Tag.objects.create(name='Python')

@pytest.fixture
def blog_post(category, tag, user):
    post = BlogPost.objects.create(
        title='How to Learn Django',
        content='Django is a high-level Python web framework that encourages rapid development...',
        author=user,
        category=category
    )
    post.tags.add(tag)
    return post

@pytest.fixture
def comment(category, user):
    return Comment.objects.create(
        post=BlogPost.objects.create(title='Test Post', content='Content', author=user, category=category),
        author=user,
        content='Great post! Very informative.',
        status='approved'
    )

@pytest.fixture
def reaction(blog_post, user):
    return Reaction.objects.create(
        post=blog_post,
        user=user,
        reaction_type='like'
    )