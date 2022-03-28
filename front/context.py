import os

from front.models import News, Category, Comment , Tags


def GA_context(req):

    return {
        'GA_CODE':os.getenv('GA','--=--')
    }

def top_5_news(req):
    return {
        'top4news': News.objects.all()[1:5],
        'topnews': News.objects.first(),
        'top3news' : News.objects.all()[:3]
    }

def top_category(req):
    return {
        'top_category': Category.objects.filter(parent=None),
        'all_category' : Category.objects.all()
    }


def tag_my (req):
    return  {
        'tag_my': Tags.objects.all()
    }
