from django.contrib.syndication.views import Feed
from .models import BlogPost
from django.utils.feedgenerator import Atom1Feed
from django.urls import reverse

#RSS(Really Simple Syndicaion) Feed
class LatestBlogPostsFeed(Feed):
    title = "Latest Blog Posts"
    link = "/feeds/blogposts/"
    description = "Stay updated with the latest insights, trends, and discussions from our blog."

    def items(self):
        return BlogPost.objects.all().order_by('-created_at')[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content

    def item_link(self, item):
        return reverse('blogpost-detail', kwargs={'pk': item.pk})

#Atom Feed
class LatestBlogPostsAtomFeed(Feed):
    feed_type = Atom1Feed
    title = "Latest Blog Posts"
    link = "/feeds/blogposts/"
    description = "Stay updated with the latest insights, trends, and discussions from our blog. "

    def items(self):
        return BlogPost.objects.all().order_by('-created_at')[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content

    def item_link(self, item):
        return reverse('blogpost-detail', kwargs={'pk': item.pk})
