from django.conf import settings
from django.db import models
from django.utils import timezone
from django.urls import reverse


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


# Create your models here.
class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Borrador'
        PUBLISHED = 'PB', 'Publicado'

    title = models.CharField(max_length=250)
    slug = models.SlugField(
        max_length=250,
        unique_for_date='publish',
    )
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog_post')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creacion')
    updated = models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT, verbose_name='Estado')
    # Post.Status.choices > para obtener las opciones disponibles
    # Post.Status.names > para obtener los nombres de las opciones
    # Post.Status.labels > para obtener los nombres legibles por humanos
    # Post.Status.values > para obtener los valores reales de las opciones
    objects = models.Manager()  # The default manager.
    published = PublishedManager()  # The manager  personalizado.

    class Meta:
        verbose_name = 'Publicación'
        verbose_name_plural = 'Publicaciones'
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year, self.publish.month, self.publish.day, self.slug])
