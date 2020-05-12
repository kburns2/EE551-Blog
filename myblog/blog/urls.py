from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('posts/', views.PostListView.as_view(), name='posts'),
    path('posts/<int:pk>', views.PostDetailView.as_view(), name='post-detail'),
    path('authors/', views.BloggerListView.as_view(), name='authors'),
    path('authors/<int:pk>', views.Sort_by_Author.as_view(), name='posts-by-author'),
    path('authordetail/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
    path('blog/<int:pk>/comment/', views.CommentCreate.as_view(), name='post-comment'),
    path('post/create/', views.PostCreate.as_view(), name='post-create'),
    path('post/<int:pk>/update/', views.PostUpdate.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', views.PostDelete.as_view(), name='post-delete'),

 
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)