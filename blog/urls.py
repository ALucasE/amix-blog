from django.urls import path
from .views import post_list, post_detail, PostListView, post_share

app_name = 'blog'

urlpatterns = [
    # post views
    path('', PostListView.as_view(), name='post_list'),
    path('<int:post_id>/share/', post_share, name='post_share'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', post_detail, name='post_detail'),
    path('def/', post_list, name='post_list'),
]
