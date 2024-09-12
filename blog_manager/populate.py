import os
import django
from faker import Faker
from random import *
from django.contrib.auth.models import User
from .models import BlogPost, Comment, Category, Tag, Reaction, UserProfile

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BlogSphere.settings')
django.setup()

faker = Faker()

def create_categories(num):
    categories = []
    for _ in range(num):
        category = Category.objects.create(name=faker.word())
        categories.append(category)
    return categories

def create_tags(num):
    tags = []
    for _ in range(num):
        tag = Tag.objects.create(name=faker.word())
        tags.append(tag)
    return tags

def create_users(num):
    users = []
    for _ in range(num):
        user = User.objects.create_user(
            username=faker.user_name(),
            password=faker.password(),
            email=faker.email()
        )
        UserProfile.objects.create(
            user=user,
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            bio=faker.text(),
            profile_picture=faker.image_url()
        )
        users.append(user)
    return users

def create_blog_posts(num, users, categories, tags):
    for _ in range(num):
        blog_post = BlogPost.objects.create(
            title=faker.sentence(),
            content=faker.text(),
            author=choice(users),
            category=choice(categories) if categories else None
        )
        blog_post.tags.set(choice(tags) for _ in range(randint(1, 5)))

def create_comments(num, blog_posts, users):
    for _ in range(num):
        Comment.objects.create(
            post=choice(blog_posts),
            author=choice(users),
            content=faker.text(),
            status=choice(['pending', 'approved'])
        )

def create_reactions(num, blog_posts, users):
    for _ in range(num):
        Reaction.objects.create(
            post=choice(blog_posts),
            user=choice(users),
            reaction_type=choice(['like', 'love', 'angry', 'sad', 'wow'])
        )

def populate_db():
    num_categories = 10
    num_tags = 10
    num_users = 20
    num_blog_posts = 50
    num_comments = 100
    num_reactions = 200

    categories = create_categories(num_categories)
    tags = create_tags(num_tags)
    users = create_users(num_users)
    create_blog_posts(num_blog_posts, users, categories, tags)
    blog_posts = list(BlogPost.objects.all())
    create_comments(num_comments, blog_posts, users)
    create_reactions(num_reactions, blog_posts, users)
    print("Database populated with fake data.")

if __name__ == '__main__':
    populate_db()
