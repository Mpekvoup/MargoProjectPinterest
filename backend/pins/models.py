from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse


class Board(models.Model):
    """Доска для организации пинов"""
    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='boards', verbose_name='Пользователь')
    is_private = models.BooleanField(default=False, verbose_name='Приватная')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создана')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлена')
    slug = models.SlugField(max_length=120, unique=True, blank=True)

    class Meta:
        verbose_name = 'Доска'
        verbose_name_plural = 'Доски'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name) + '-' + str(self.user.id)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('board_detail', kwargs={'slug': self.slug})

    def pin_count(self):
        return self.pins.count()


class Pin(models.Model):
    """Пин - изображение с описанием"""
    title = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    image = models.ImageField(upload_to='pins/%Y/%m/%d/', verbose_name='Изображение')
    source_url = models.URLField(blank=True, verbose_name='Ссылка на источник')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pins', verbose_name='Пользователь')
    board = models.ForeignKey(Board, on_delete=models.SET_NULL, null=True, blank=True, related_name='pins', verbose_name='Доска')
    tags = models.CharField(max_length=200, blank=True, verbose_name='Теги', help_text='Разделяйте теги запятыми')
    likes = models.ManyToManyField(User, related_name='liked_pins', blank=True, verbose_name='Лайки')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлен')

    class Meta:
        verbose_name = 'Пин'
        verbose_name_plural = 'Пины'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('pin_detail', kwargs={'pk': self.pk})

    def like_count(self):
        return self.likes.count()

    def is_liked_by(self, user):
        return self.likes.filter(id=user.id).exists()

    def get_tags_list(self):
        """Возвращает список тегов"""
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',')]
        return []


class Comment(models.Model):
    """Комментарий к пину"""
    pin = models.ForeignKey(Pin, on_delete=models.CASCADE, related_name='comments', verbose_name='Пин')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name='Пользователь')
    text = models.TextField(verbose_name='Текст')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['created_at']

    def __str__(self):
        return f'Комментарий от {self.user.username} к {self.pin.title}'
