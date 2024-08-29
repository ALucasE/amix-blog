from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown

from ..models import Post


register = template.Library()


# Etiqueta simple que devuelve el número de publicaciones publicadas
@register.simple_tag
def total_posts():
    return Post.published.count()


# Etiqueta para mostrar las últimas publicaciones
@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


# Etiqueta  para  mostrar  las  publicaciones  más  comentadas
@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]


# Filtro personalizado para permitirle utilizar la sintaxis de Markdown
@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
