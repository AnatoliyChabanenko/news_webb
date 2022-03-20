from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy, reverse

from .forms import RegisterUserForm, LoginUserForm, AddCommentsForm
from .models import Category, News,  Tags, Comment

from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView, DeleteView

from .utils import DataMixin


# Create your views here.


class One_News(DetailView):
    model = News
    template_name = 'front/page_one_news.html'
    context_object_name = 'one_news'

    """ну например так """

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        comments_connected = Comment.objects.filter(post_id=self.get_object()).order_by('-created_on')

        data['comments'] = comments_connected
        if self.request.user.is_authenticated:
            data['comment_form'] = AddCommentsForm(instance=self.request.user)
        return data

    def post(self, request, *args, **kwargs):
        new_comment = Comment(body=request.POST.get('body'),
                                  author=self.request.user,
                                  post=self.get_object())
        new_comment.save()
        return self.get(self, request, *args, **kwargs)



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
#
# class PostCommentDeleteView(LoginRequiredMixin, DeleteView):
#     model = Comment
#     template_name = 'front/comments_delete.html'  # <app>/<model>_<viewtype>.html
#
#     def test_func(self):
#         comment = self.get_object()
#         if self.request.user == comment.user:
#             return True
#         return False
#
#     def form_invalid(self, form):
#         return HttpResponseRedirect(self.get_success_url())
#
#     def get_success_url(self):
#         return reverse('front/page_one_news.html', kwargs=dict(pk=self.kwargs['id']))


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

def logout_user(request):
    logout(request)
    return redirect('login')