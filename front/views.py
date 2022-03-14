from django.shortcuts import render
# from django.db.models import F, Max, Min, Sum, Count, Avg
from .models import Category, Comment, News, Avtor, Tags

from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, TemplateView
from django.forms import ModelForm


# Create your views here.

class One_News(DetailView):
    model = News
    template_name = 'front/one_news.html'
    context_object_name = 'one_news'


class News_list(ListView):
    model = News
    template_name = 'front/category_news.html'
    context_object_name = 'news_list'

    def get_queryset(self):
        return News.objects.filter(categori__name=self.kwargs['slug'])



class Category_list(ListView):
    model = Category
    template_name = 'front/first_page.html'
    context_object_name = 'category'

    def get_queryset(self):
        return Category.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news'] = News.objects.all()
        return context


    @property
    def has_child(self):
        return Category.objects.filter(parent=self).exists()

    @property
    def childs(self):
        return Category.objects.filter(parent=self).order_by('id')


class Tegs_news (ListView):
    model = Tags
    template_name = 'front/mytags.html'
    context_object_name = 'tegs'


    def get_queryset(self):
        return News.objects.filter(tags__tags=self.kwargs['slug'])

