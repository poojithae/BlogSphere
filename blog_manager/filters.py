import django_filters
from .models import BlogPost

class BlogPostFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search')
    created_at = django_filters.DateFilter(field_name='created_at', lookup_expr='exact') 
    author = django_filters.NumberFilter(field_name='author__id')
    tags = django_filters.CharFilter(method='filter_tags')

    class Meta:
        model = BlogPost
        fields = []

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            title__icontains=value
        ).filter(
            content__icontains=value
        )

    def filter_tags(self, queryset, name, value):
        return queryset.filter(tags__name__in=value.split(','))
