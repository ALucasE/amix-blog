from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from django.db.models import Count, Q
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity

from taggit.models import Tag

from .models import Post, Comment
from .forms import EmailPostForm, CommentForm, SearchForm


def post_list(request, tag_slug=None):
    """
    Lista publicaciones publicadas, con la opción de filtrar por etiqueta.
    Parámetros:
        request (HttpRequest): Objeto de solicitud HTTP entrante.
        tag_slug (str, opcional): Nombre corto (slug) de la etiqueta para filtrar.
        Si no se proporciona, se muestran todas las publicaciones.
    Retorna:
        HttpResponse: Objeto HttpResponse renderizado con la plantilla y contexto.
    Plantilla: 'blog/post/list.html'
    Contexto:
        - posts (QuerySet): Lista paginada de publicaciones publicadas.
        - tag (Tag, opcional): Objeto Tag si se proporcionó un slug, de lo contrario None.
    """
    post_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    # Paginacion con 3 posts por pagina
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # Si page_number no es un entero, entregue la primera página
        posts = paginator.page(1)
    except EmptyPage:
        # Si page_number está fuera de rango, entregue la última página de resultados
        posts = paginator.page(paginator.num_pages)
    context = {'posts': posts, 'tag': tag}
    return render(request, 'blog/post/list.html', context)


def post_detail(request, year, month, day, post):
    """
    Muestra una vista detallada de una publicación publicada del blog, incluyendo comentarios, un formulario de comentarios y publicaciones similares.
    Parámetros:
        request (HttpRequest): Objeto de solicitud HTTP entrante.
        year (int): Año de publicación de la entrada del blog.
        month (int): Mes de publicación de la entrada del blog.
        day (int): Día de publicación de la entrada del blog.
        post (str): Slug de la publicación a recuperar.
    Retorna:
        HttpResponse: Objeto HttpResponse renderizado con la plantilla y contexto.
    Levanta:
        Http404: Si la publicación solicitada no se encuentra o no está publicada.
    Plantilla: 'blog/post/detail.html'
    Contexto:
        - post (Post): Objeto del Post recuperado.
        - comments (QuerySet): Lista de comentarios activos para la publicación.
        - form (CommentForm): Instancia del formulario CommentForm para la entrada de datos del usuario.
        - similar_posts (QuerySet): Lista de publicaciones similares basadas en etiquetas (máximo 4).
    """
    post = get_object_or_404(
        Post, status=Post.Status.PUBLISHED, slug=post, publish__year=year, publish__month=month, publish__day=day
    )
    comments = post.comments.filter(active=True)
    # Fomulario de comentarios
    form = CommentForm()

    # Lista de publicaicones similares
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]

    context = {'post': post, 'comments': comments, 'form': form, 'similar_posts': similar_posts}
    return render(request, 'blog/post/detail.html', context)


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_share(request, post_id):
    """
    Comparte una publicación del blog por correo electrónico.
    Parámetros:
        request (HttpRequest): Objeto de solicitud HTTP entrante.
        post_id (int): Identificador de la publicación a compartir.
    Retorna:
        HttpResponse: Objeto HttpResponse renderizado con la plantilla y contexto.
    Levanta:
        Http404: Si la publicación solicitada no se encuentra o no está publicada.
    Plantilla: 'blog/post/share.html'
    Contexto:
        - post (Post): Objeto del Post recuperado.
        - form (EmailPostForm): Instancia del formulario EmailPostForm.
        - sent (bool): Indica si el correo electrónico se envió correctamente.
    """
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{form_data['name']} te recomienda leer {post.title}"
            message = f"Puedes leer {post.title} en {post_url}\n\n \
                comentario de {form_data['name']} - {form_data['email']}: {form_data['comments']}"
            send_mail(subject, message, 'f39dceba809abd@inbox.mailtrap.io', [form_data['to']])
            sent = True
    else:
        form = EmailPostForm()
    context = {'post': post, 'form': form, 'sent': sent}
    return render(request, 'blog/post/share.html', context)


# Comentario de publicacion
@require_POST
def post_comment(request, post_id):
    """
    Procesa y guarda un nuevo comentario para una publicación.

    Parámetros:
        request (HttpRequest): Objeto de solicitud HTTP entrante.
        post_id (int): Identificador de la publicación a la que pertenece el comentario.

    Retorna:
        HttpResponse: Objeto HttpResponse renderizado con la plantilla y contexto.

    Levanta:
        Http404: Si la publicación solicitada no se encuentra o no está publicada.

    Plantilla: 'blog/post/comment.html'
    Contexto:
        - post (Post): Objeto del Post recuperado.
        - form (CommentForm): Instancia del formulario CommentForm procesada con los datos del POST.
        - comment (Comment, opcional): Objeto del comentario guardado (si el formulario es válido).
    """
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    context = {'post': post, 'form': form, 'comment': comment}
    return render(request, 'blog/post/comment.html', context)


def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('title', 'body', config='spanish')
            search_query = SearchQuery(query, config='spanish')
            results = (
                Post.published.annotate(search=search_vector, rank=SearchRank(search_vector, search_query))
                .filter(search=search_query)
                .order_by('-rank')
            )
    context = {'form': form, 'query': query, 'results': results}
    return render(request, 'blog/post/search.html', context)
