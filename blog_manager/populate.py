import os
import django
from random import *
from faker import Faker
from django.contrib.auth.models import User
from blog_manager.models import BlogPost, Comment, Category, Tag, Reaction, UserProfile  

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BlogSphere.settings')
django.setup()

fake = Faker()

def create_users(num_users):
    users = []
    for _ in range(num_users):
        user = User.objects.create_user(
            username=fake.user_name(),
            password=fake.password(),
            email=fake.email()
        )
        UserProfile.objects.create(
            user=user,
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            bio=fake.text()
        )
        users.append(user)
    return users

def create_categories_and_tags():
    categories = [Category.objects.create(name=fake.word()) for _ in range(5)]
    tags = [Tag.objects.create(name=fake.word()) for _ in range(10)]
    return categories, tags

def create_blog_posts(users, categories, tags, num_posts=10):
    for _ in range(num_posts):
        post = BlogPost.objects.create(
            title=fake.sentence(),
            content=fake.text(),
            author=choice(users),
            category=choice(categories) if choice([True, False]) else None
        )
        post.tags.set(sample(tags, k=randint(1, 3)))

def create_comments(posts, users, num_comments=20):
    for _ in range(num_comments):
        Comment.objects.create(
            post=choice(posts),
            author=choice(users),
            content=fake.text(),
            status=choice(['pending', 'approved'])
        )

def create_reactions(posts, users, num_reactions=30):
    reaction_types = ['like', 'love', 'angry', 'sad', 'wow']
    for _ in range(num_reactions):
        Reaction.objects.create(
            user=choice(users),
            post=choice(posts),
            reaction_type=choice(reaction_types)
        )

def populate(n):
    users = create_users(n)
    categories, tags = create_categories_and_tags()
    create_blog_posts(users, categories, tags)
    posts = BlogPost.objects.all()
    create_comments(posts, users)
    create_reactions(posts, users)

if __name__ == '__main__':
    populate(10)
