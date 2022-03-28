from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView

from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView, DeleteView

from .forms import RegisterUserForm, LoginUserForm, AddCommentsForm
from .models import  News, Tags, Comment


from .utils import DataMixin


# Create your views here.


class One_News(DetailView):
    model = News
    template_name = 'front/page_one_news.html'
    context_object_name = 'one_news'

    """ну например так """

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        comments_connected = Comment.objects.filter(post_id=self.get_object()).order_by('-created_on').select_related('post')

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



class News_list (DataMixin, ListView):
    model = News
    template_name = 'front/category_news.html'
    context_object_name = 'news_list'

    def get_queryset(self):
        return News.objects.filter(categori__name=self.kwargs['slug']).select_related('categori')


class FirsPage(DataMixin, ListView):
    model = News
    template_name = 'front/fist_page.html'
    context_object_name = 'category'

    def get_queryset(self):
        return News.objects.all().prefetch_related('tags')


class Tegs_news(DataMixin, ListView):
    model = Tags
    template_name = 'front/page_mytags.html'
    context_object_name = 'tegs_news'


    def get_queryset(self):
        tag = Tags.objects.get(pk=self.kwargs['pk'])
        return tag.teg_news


class PostCommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'front/page_one_news.html'  # <app>/<model>_<viewtype>.html
    success_message = "deleted..."

    def get_success_url(self):

        companyid = self.object.post_id
        return reverse_lazy('news', kwargs={'pk': companyid})


    def post(self, request, *args, **kwargs):

        self.object = self.get_object()
        if self.object.author == request.user:
            success_url = self.get_success_url()
            self.object.delete()
            return HttpResponseRedirect(success_url)

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
