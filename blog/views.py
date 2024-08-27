from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post

# Create your views here.


def post_list(request):
    post_list = Post.published.all()
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
    context = {'posts': posts}
    return render(request, 'blog/post/list.html', context)


def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post, status=Post.Status.PUBLISHED, slug=post, publish__year=year, publish__month=month, publish__day=day
    )
    context = {'post': post}
    return render(request, 'blog/post/detail.html', context)


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'
