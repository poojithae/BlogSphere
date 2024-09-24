from django.contrib.syndication.views import Feed
from django.db.models.base import Model
from django.template.defaultfilters import truncatewords
from django.urls import reverse_lazy
from django.utils.safestring import SafeText
from .models import BlogPost

class LastPostFeed(Feed):
    title = 'blog_post'
    link = reverse_lazy('blog:blogpost-list-create')
    description = 'New Post of my Blog'

    def item(self):
        return BlogPost.objects.all()[:5]
    
    def item_title(self, item):
        return item.title
    
    def item_description(self, item):
        return truncatewords(item.body,30)