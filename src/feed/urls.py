from django.urls import path
from . import views
from django.conf.urls.static import static
from HireMe import settings

app_name = 'feeds'

urlpatterns = [
    path(r'posts/<slug:identifier>', views.blog_view, name='blog_url'),
    path(r'images/<slug:identifier>', views.image_view, name='image_url'),
    path(r'images/like/<slug:identifier>', views.photo_ko_like_karo, name='photo_like'),
    path(r'posts/like/<slug:identifier>', views.blog_ko_like_karo, name='blog_like'),
    path(r'add_post/', views.create_post_view, name='create_post'),
    path(r'add_image_post/', views.create_image_post_view, name='add_image_post'),
    path(r'404', views.error404, name='404'),
    path(r'comments/', views.create_comments_view, name='add_comment'),
    path(r'notifications/', views.notification_view, name='notifications'),
    path(r'blog/<slug:username>', views.blog_list_view, name='blog'),
]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)