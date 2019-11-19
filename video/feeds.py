from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Rss201rev2Feed, rfc2822_date
from django.shortcuts import resolve_url
from .models import Movie
from django.urls import reverse_lazy

class LatestPostFeed(Feed):
    title = "しこるおまとめ"
    link = reverse_lazy('video:feed')
    description = "しこるおまとめから、記事の最新情報をお届けします。"

    def items(self):
        return Movie.objects.all().order_by('-created_at')[:30]

    def item_title(self, item):
        return item.title
    
    def item_description(self, item):
        return item.thumb.url

    def item_link(self, item):
        return resolve_url('video:movie', pk=item.pk)
    
    def item_categories(self, item):
        return item.tag.split(',')