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

    def get_queryset(self):
        """Not mandatory but useful for filtering or customizing queries."""
        return super().get_queryset().select_related('category').prefetch_related('tags')

    def prepare_category(self, instance):
        """Prepare data for category field"""
        return {
            'name': instance.category.name if instance.category else None
        }

    def prepare_tags(self, instance):
        """Prepare data for tags field"""
        return [{'name': tag.name} for tag in instance.tags.all()]


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



    