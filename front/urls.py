"""news URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from . import views
from django.urls import path



admin.site.site_header = 'Моя адмінка'
admin.site.index_title = 'супер адмінка'

urlpatterns = [
    path('', views.Category_list.as_view(), name='home'),
    path('<str:slug>', views.News_list.as_view(), name='category'),
    path('tag/<str:slug>', views.Tegs_news.as_view(), name='tag'),
    path('news/<int:pk>', views.One_News.as_view(), name='news'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.RegisterUser.as_view(), name='register'),
]
