
from django.db import models
from django.contrib.auth.models import User



class Category(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('Category',blank=True , null=True, default=None, on_delete=models.PROTECT)
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name='URL')

    @property
    def news(self):
        return News.objects.filter(categori=self)

    @property
    def has_child(self):
        return Category.objects.filter(parent=self)

    @property
    def childs(self):
        return Category.objects.filter(parent=self).order_by('id')

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse('category', kwargs={'cat.slug':self.slag })


class Avtor(models.Model):

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=30)

    @property
    def name(self):
        return (self.last_name, self.first_name)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    def __repr__(self):
        return f"{self.last_name} {self.first_name}"


class Tags(models.Model):
    tags = models.CharField(max_length=100)

    @property
    def teg_news(self):
        return News.objects.filter(tags=self)

    def __str__(self):
        return f'{self.tags}'


class News(models.Model):
    name = models.CharField(max_length=255, verbose_name='Заголовок')
    text = models.TextField()
    categori = models.ForeignKey(Category, on_delete=models.PROTECT)
    tags = models.ManyToManyField(Tags)
    author = models.ForeignKey(Avtor, default=None, on_delete=models.CASCADE)
    img = models.ImageField(blank=True, null=True)
    time = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name_plural = 'Новости'
        ordering = ['time', 'name']

    @property
    def number_of_comments(self):
        return Comment.objects.filter(post_id=self).count()

    def __str__(self):
        return f'{self.name}'


class Comment(models.Model):
    post = models.ForeignKey(News, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True, null=True)




    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.author)