from django.db import models
from django.urls import reverse


class Blog(models.Model):
    """
    title - заголовок статьи
    slug - заголовок статьи переведенный на англ.язык (db_index - для лучшего поиска статей)
    content - содержимое статьи (может быть пустым)
    photo - какая-либо фотография статьи(располагается в определенной папке с помощью upoload_to)
    time_created - время создания (создается автоматически текущая дата и время в момент добавленния в БД)
    time_update - время публикации (фиксирует текущее время при изменении)
    is_published - опубликована ли запись (по умолчанию опубликована)
    cat - внешний "ключ один ко многим" К одной Category - много записей (2 арг: модель, с которой связываем и
     ограничение при удаление внешних записей. в данном случае: PROTECT - запрет на удаление записи из первичной модели,
     если она используется во вторичной)
    """

    title = models.CharField(max_length=255, verbose_name='Название')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    content = models.TextField(blank=True, verbose_name='Контент')
    photo = models.ImageField(upload_to='photos/%Y/%m/d', blank=True, verbose_name='Фото')
    time_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категория')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-time_created']


class Category(models.Model):
    """
    name - название категории
    slug - ее название на английском
    """

    name = models.CharField(max_length=100, db_index=True, verbose_name='Категория')
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name='URL')

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

