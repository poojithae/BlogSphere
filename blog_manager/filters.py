from django_filters import rest_framework as filters
from .models import BlogPost

class BlogPostFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')
    author = filters.CharFilter(lookup_expr='icontains')
    created_at = filters.DateFromToRangeFilter()
    tags = filters.CharFilter(method='filter_tags')

    # search = filters.CharFilter(method='^search_filter')
    # created_at = filters.DateFilter(field_name='created_at', lookup_expr='exact') 
    # author = filters.NumberFilter(field_name='author__id')
    # tags = filters.CharFilter(method='filter_tags')

    class Meta:
        model = BlogPost
        fields = ['title', 'author', 'created_at', 'tags']

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            title__icontains=value
        ).filter(
            content__icontains=value
        )

    def filter_tags(self, queryset, name, value):
        return queryset.filter(tags__name__in=value.split(','))
