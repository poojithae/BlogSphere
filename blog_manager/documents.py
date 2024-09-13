from django_elasticsearch_dsl import Document, Index, fields
from django_elasticsearch_dsl.registries import registry
from .models import BlogPost, Category, Tag

post_index = Index('posts')


@post_index.document
class BlogPostDocument(Document):
    category = fields.ObjectField(properties={
        'name': fields.TextField()
    })
    tags = fields.ObjectField(properties={
        'name': fields.TextField()
    })

    class Index:
        name = 'blog_posts'

    class Django:
        model = BlogPost
        fields = [
            'title',
            'content',
            'created_at',
            'updated_at',
        ]

    class Meta:
        index = 'posts'

@registry.register_document
class CategoryDocument(Document):
    class Index:
        name = 'categories'

    class Django:
        model = Category
        fields = [
            'name',
        ]

@registry.register_document
class TagDocument(Document):
    class Index:
        name = 'tags'

    class Django:
        model = Tag
        fields = [
            'name',
        ]



    