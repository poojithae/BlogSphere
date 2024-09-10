import pytest
from rest_framework import status
from django.contrib.auth.models import User
from django.urls import reverse
from blog_manager.models import BlogPost, Comment, Category, Tag, Reaction, UserProfile
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.mark.django_db
def test_blog_post_list(auth_client, blog_post):
    url = reverse('blogpost-list-create')
    response = auth_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) > 0
    assert response.data[0]['title'] == blog_post.title

@pytest.mark.django_db
def test_blog_post_create(auth_client, user, category, tag):
    url = reverse('blogpost-list-create')
    data = {
        'title': 'How to Learn Django',
        'content': 'Django is a high-level Python web framework that encourages rapid development...',
        'author': user.id, 
        'category': category.id,
        'tags': [tag.id]
    }
    response = auth_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert BlogPost.objects.count() == 1
    assert BlogPost.objects.last().title == 'How to Learn Django'

@pytest.mark.django_db
def test_blog_post_detail(auth_client, blog_post):
    url = reverse('blogpost-detail', kwargs={'pk': blog_post.id})
    response = auth_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['title'] == blog_post.title

@pytest.mark.django_db
def test_blog_post_update(auth_client, blog_post):
    url = reverse('blogpost-detail', kwargs={'pk': blog_post.id})
    data = {'title': 'How to Learn Django Framework',}
    response = auth_client.patch(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    blog_post.refresh_from_db()
    assert blog_post.title == 'How to Learn Django Framework'

@pytest.mark.django_db
def test_blog_post_delete(auth_client, blog_post):
    url = reverse('blogpost-detail', kwargs={'pk': blog_post.id})
    response = auth_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert BlogPost.objects.count() == 0

@pytest.mark.django_db
def test_comment_list(auth_client, comment):
    url = reverse('comment-list-create')
    response = auth_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) > 0
    assert response.data[0]['content'] == comment.content

@pytest.mark.django_db
def test_comment_create(auth_client, blog_post, user):
    url = reverse('comment-list-create')
    data = {
        'post': blog_post.id,  
        'author': user.id,  
        'content': 'Great post! Very informative.',
        'status': 'approved'
    }
    response = auth_client.post(url, data, format='json')
    print(response.content)
    assert response.status_code == status.HTTP_201_CREATED
    assert Comment.objects.count() == 1  
    assert Comment.objects.last().content == 'Great post! Very informative.'

@pytest.mark.django_db
def test_comment_detail(auth_client, comment):
    url = reverse('comment-detail', kwargs={'pk': comment.id})
    response = auth_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['content'] == comment.content

@pytest.mark.django_db
def test_comment_update(auth_client, comment):
    url = reverse('comment-detail', kwargs={'pk': comment.id})
    data = {'content': 'that is great, With using Django makes it easier to build web pages using Python.'}
    response = auth_client.patch(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    comment.refresh_from_db()
    assert comment.content == 'that is great, With using Django makes it easier to build web pages using Python.'

@pytest.mark.django_db
def test_comment_delete(auth_client, comment):
    url = reverse('comment-detail', kwargs={'pk': comment.id})
    response = auth_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Comment.objects.count() == 0 

@pytest.mark.django_db
def test_category_list(auth_client, category):
    url = reverse('category-list-create')
    response = auth_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) > 0
    assert response.data[0]['name'] == category.name

@pytest.mark.django_db
def test_category_create(auth_client):
    url = reverse('category-list-create')
    data = {'name': 'Programming'}
    response = auth_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Category.objects.count() == 1 
    assert Category.objects.last().name == 'Programming'

@pytest.mark.django_db
def test_tag_list(auth_client, tag):
    url = reverse('tag-list-create')
    response = auth_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) > 0
    assert response.data[0]['name'] == tag.name

@pytest.mark.django_db
def test_tag_create(auth_client):
    url = reverse('tag-list-create')
    data = {'name': 'Django'}
    response = auth_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Tag.objects.count() == 1  
    assert Tag.objects.last().name == 'Django'

@pytest.mark.django_db
def test_reaction_list_create(auth_client, blog_post, user ):
    url = reverse('reaction-list-create')
    data = {
        'post': blog_post.id,
        'user' :user.id,
        'reaction_type': 'love'
    }
    response = auth_client.post(url, data, format='json')
    print(response.content) 
    assert response.status_code == status.HTTP_201_CREATED
    assert Reaction.objects.count() == 1  
    assert Reaction.objects.last().reaction_type == 'love'

@pytest.mark.django_db
def test_reaction_create_as_admin(admin_client, blog_post, user):
    url = reverse('reaction-list-create')
    data = {
        'post': blog_post.id,
        'user' :user.id,
        'reaction_type': 'wow'
    }
    response = admin_client.post(url, data, format='json')
    print(response.content) 
    assert response.status_code == status.HTTP_201_CREATED
    assert Reaction.objects.count() == 1  
    assert Reaction.objects.last().reaction_type == 'wow'

@pytest.mark.django_db
def test_reaction_detail_retrieve(auth_client, reaction):
    url = reverse('reaction-detail', kwargs={'pk': reaction.id})
    response = auth_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['reaction_type'] == reaction.reaction_type

@pytest.mark.django_db
def test_reaction_detail_delete(auth_client, reaction):
    url = reverse('reaction-detail', kwargs={'pk': reaction.id})
    response = auth_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Reaction.objects.count() == 0  

@pytest.mark.django_db
def test_reaction_detail_delete_as_admin(admin_client, reaction):
    url = reverse('reaction-detail', kwargs={'pk': reaction.id})
    response = admin_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Reaction.objects.count() == 0  

@pytest.mark.django_db
def test_register_user_success():
    client = APIClient()  
    url = reverse('register')
    data = {
        'username': 'Adrian',
        'password': 'Adrian123',
        'email': 'Adria@gmail.com'
    }
    response = client.post(url, data, format='json')
    print(response.content)
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_register_user_missing_fields():
    client = APIClient()  
    url = reverse('register')
    data = {
        'username': 'Adrian',
        # Missing password and email
    }
    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_register_user_invalid_data():
    client = APIClient() 
    url = reverse('register')
    data = {
        'username': 'existinguser', 
        'password': 'Invalidpassword',
        'email': 'not-an-email'
    }
    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST




@pytest.mark.django_db
def test_retrieve_user_profile_success():
    
    user = User.objects.create_user(username='pooji', password='pooji123')
    UserProfile.objects.create(user=user, first_name='Adrian', last_name='Holovaty')

    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse('userprofile')  

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data['first_name'] == 'Adrian'
    assert response.data['last_name'] == 'Holovaty'

@pytest.mark.django_db
def test_retrieve_user_profile_not_found():
    user = User.objects.create_user(username='pooji', password='pooji123')

    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse('userprofile') 

    response = client.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data['detail'] == 'User profile not found.'

@pytest.mark.django_db
def test_update_user_profile_success():
    user = User.objects.create_user(username='pooji', password='pooji123')
    UserProfile.objects.create(user=user, first_name='Adrian', last_name='Holovaty')

    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse('userprofile')  

    data = {'first_name': 'Holovaty', 'last_name': 'Adrian'}
    response = client.put(url, data, format='json')

    assert response.status_code == status.HTTP_200_OK
    assert response.data['first_name'] == 'Holovaty'
    assert response.data['last_name'] == 'Adrian'





















