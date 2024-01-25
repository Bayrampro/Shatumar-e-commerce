from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Products(models.Model):
    title = models.CharField(max_length=255, verbose_name='Имя')
    content = models.TextField(verbose_name='Описания')
    per_package = models.CharField(max_length=255, verbose_name='Ед. в упаковке')
    per_box = models.IntegerField(default=0, verbose_name='Ед. в каробке')
    netto_weight = models.IntegerField(default=0, verbose_name='Вес нетто')
    brutto_weight = models.IntegerField(default=0, verbose_name='Вес брутто')
    cost = models.FloatField(default=0, verbose_name='Цена')
    cost_for_box = models.FloatField(default=0, verbose_name='Цена за каробку')
    img = models.ImageField(upload_to='photos/%Y/%m/')
    slug = models.SlugField(unique=True)
    category = models.ForeignKey('Category', on_delete=models.PROTECT, null=True)

    def get_absolute_url(self, slug):
        return reverse('product_detail', kwargs={'slug': slug})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name='Имя')
    img = models.ImageField(upload_to='photos/%Y/%m/', null=True)
    slug = models.SlugField(unique=True)

    def get_absolute_url(self, slug):
        return reverse('category_detail', kwargs={'slug': slug})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Feedback(models.Model):
    user = models.CharField(max_length=255, verbose_name='Ползователь')
    email = models.EmailField(null=True)
    subject = models.TextField(verbose_name='Сообщение')

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
