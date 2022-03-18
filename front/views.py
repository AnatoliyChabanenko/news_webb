from django.contrib.auth import logout, login
# from django.db.models import F, Max, Min, Sum, Count, Avg
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

from .forms import RegisterUserForm, LoginUserForm
from .models import Category, Comment, News, Avtor, Tags

from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, TemplateView, CreateView
from django.forms import ModelForm
from .utils import DataMixin


# Create your views here.


class One_News(DetailView):
    model = News
    template_name = 'front/page_one_news.html'
    context_object_name = 'one_news'


class News_list(DataMixin, ListView):
    model = News
    template_name = 'front/category_news.html'
    context_object_name = 'news_list'

    def get_queryset(self):
        return News.objects.filter(categori__name=self.kwargs['slug'])


class Category_list(DataMixin, ListView):
    model = Category
    template_name = 'front/fist_page.html'
    context_object_name = 'category'

    def get_queryset(self):
        return News.objects.all()

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


class Tegs_news(DataMixin , ListView):
    model = Tags
    template_name = 'front/page_mytags.html'
    context_object_name = 'tegs_news'

    def get_queryset(self):
        return News.objects.filter(tags__tags=self.kwargs['slug'])


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'front/page_regiser.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'front/page_login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')
