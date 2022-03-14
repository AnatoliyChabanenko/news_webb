from django.contrib import admin
from  django.db.models import QuerySet
# Register your models here.


from .models import *

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',  'slug','parent')
    # list_display_links = ('name',) стандартно 1 в линк дисплей  можно менять
    list_editable = ['slug', 'parent']
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}
    ordering =['-name']
    actions = ['set_chtoto']



    @admin.action(description='установить новую главную категорию ')
    def set_chtoto(self, request , qs: QuerySet):
        count_update = qs.update(parent=Category.objects.first())
        self.message_user(request ,
                          message=f'було змінено {count_update} записи')


# class Rating(admin.SimpleListFilter):
#     title = 'фильтр по рейтингу'
#     parameter_name = 'raiting'
#
#     def lookups(self, request, model_admin):
#         return [
#             ('<40', 'Низкий '),
#             ('от 40 до 59 ', 'средний'),
#             ('от 60 до 79 ', 'высокий'),
#             ('>=80', 'Высочайший  '),
#
#  '''сюда пишем что будет в админке '''
#         ]
#
#     def queryset(self, request, queryset: QuerySet):
#         if self.value() == '<40':
#             return  queryset.filter()
#         return queryset

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_per_page = 3
    list_filter = ['name', 'tags', 'author',] #'Rating'
# можно так и декоратором admin.site.register(Category, CategoryAdmin)


admin.site.register(Avtor)
admin.site.register(Tags)
admin.site.register(Comment)
